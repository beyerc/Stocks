# data_fetch.py
import yfinance as yf
import pandas as pd

def get_history(symbol: str, period: str = "1y") -> pd.DataFrame:
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, auto_adjust=False)
        if df.empty:
            return None
        df.index = pd.to_datetime(df.index)
        return df[['Open','High','Low','Close','Volume']]
    except Exception:
        return None
