# backend/api_stub.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

app = FastAPI(title="Stock Picker API Stub")

class AnalysisResponse(BaseModel):
    symbol: str
    last_price: float
    indicators: Dict[str, Any]
    signals: list
    entry_recommendation: Dict[str, Any]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/quote")
def quote(symbol: str = "AAPL"):
    # Minimal quote response for frontend testing
    return {"symbol": symbol.upper(), "last_price": 150.00}

@app.get("/api/analyze", response_model=AnalysisResponse)
def analyze(symbol: str = "AAPL", range: str = "1y"):
    # Return a deterministic, mock analysis payload the frontend expects
    mock = {
        "symbol": symbol.upper(),
        "last_price": 150.00,
        "indicators": {
            "sma50": 148.5,
            "sma200": 140.2,
            "rsi14": 55.3,
            "macd": {"macd": 1.2, "signal": 0.8, "hist": 0.4},
            "bb_upper": 160.0,
            "bb_middle": 150.0,
            "bb_lower": 140.0,
            "volume_avg20": 120000000
        },
        "signals": ["sma50_above_sma200", "rsi_neutral"],
        "entry_recommendation": {"type": "conservative", "price": 149.0, "stop": 144.0, "confidence": 0.62}
    }
    return mock

if __name__ == "__main__":
    uvicorn.run("backend.api_stub:app", host="0.0.0.0", port=8000, reload=True)
