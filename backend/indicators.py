# indicators.py
import pandas as pd
import numpy as np

def sma(series: pd.Series, window: int):
    return series.rolling(window).mean()

def ema(series: pd.Series, window: int):
    return series.ewm(span=window, adjust=False).mean()

def rsi(series: pd.Series, window: int = 14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.ewm(alpha=1/window, adjust=False).mean()
    ma_down = down.ewm(alpha=1/window, adjust=False).mean()
    rs = ma_up / ma_down
    return 100 - (100 / (1 + rs))

def bollinger(series: pd.Series, window: int = 20, n_std: int = 2):
    ma = series.rolling(window).mean()
    std = series.rolling(window).std()
    upper = ma + n_std * std
    lower = ma - n_std * std
    return upper, ma, lower

def compute_indicators(df: pd.DataFrame):
    close = df['Close']
    indicators = {}
    indicators['sma50'] = sma(close, 50)
    indicators['sma200'] = sma(close, 200)
    indicators['rsi14'] = rsi(close, 14)
    macd_line = ema(close, 12) - ema(close, 26)
    signal = macd_line.ewm(span=9, adjust=False).mean()
    indicators['macd'] = macd_line
    indicators['macd_signal'] = signal
    upper, middle, lower = bollinger(close)
    indicators['bb_upper'] = upper
    indicators['bb_middle'] = middle
    indicators['bb_lower'] = lower
    indicators['volume_avg20'] = df['Volume'].rolling(20).mean()
    return indicators

def compute_score(indicators: dict):
    # Simple example scoring logic
    latest = {}
    latest['sma50'] = indicators['sma50'].iloc[-1] if indicators['sma50'].notna().any() else None
    latest['sma200'] = indicators['sma200'].iloc[-1] if indicators['sma200'].notna().any() else None
    latest['rsi'] = indicators['rsi14'].iloc[-1] if indicators['rsi14'].notna().any() else None
    score = 0.5
    recommendation = "No Entry"
    entry = float(latest['sma50']) if latest['sma50'] else 0.0
    # Trend boost
    if latest['sma50'] and latest['sma200'] and latest['sma50'] > latest['sma200']:
        score += 0.25
    # RSI check
    if latest['rsi'] and latest['rsi'] < 30:
        score += 0.15
    if score > 0.75:
        recommendation = "Aggressive Buy"
    elif score > 0.55:
        recommendation = "Consider Buy"
    return {"confidence": score, "recommendation": recommendation, "entry": entry}
