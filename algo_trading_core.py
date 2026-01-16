
"""
algo_trading_core.py

Production-style core module for:
- Market data fetching (Yahoo Finance)
- Technical indicators (RSI, VWAP, MFI, ADX, ROC)

Safe for public GitHub repositories (no strategies, no API keys).
"""

import pandas as pd
import numpy as np
import yfinance as yf
from abc import ABC, abstractmethod


# ==============================
# Market Data Layer
# ==============================

class MarketDataProvider(ABC):
    @abstractmethod
    def fetch_ohlcv(self, symbol: str, interval: str, start: str = None, end: str = None) -> pd.DataFrame:
        pass


class YahooFinanceProvider(MarketDataProvider):
    def fetch_ohlcv(self, symbol: str, interval: str = "1d", start: str = None, end: str = None) -> pd.DataFrame:
        df = yf.download(
            tickers=symbol,
            interval=interval,
            start=start,
            end=end,
            progress=False
        )

        if df.empty:
            raise ValueError("No data returned from Yahoo Finance")

        df.columns = df.columns.str.lower()
        return df.reset_index()


# ==============================
# Indicator Engine
# ==============================

def rsi(close: pd.Series, length: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/length, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/length, adjust=False).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def vwap(df: pd.DataFrame) -> pd.Series:
    tp = (df["high"] + df["low"] + df["close"]) / 3
    return (tp * df["volume"]).cumsum() / df["volume"].cumsum()


def mfi(df: pd.DataFrame, length: int = 14) -> pd.Series:
    tp = (df["high"] + df["low"] + df["close"]) / 3
    rmf = tp * df["volume"]

    direction = np.sign(tp.diff())
    pos_mf = rmf.where(direction > 0, 0.0)
    neg_mf = rmf.where(direction < 0, 0.0)

    mfr = pos_mf.rolling(length).sum() / neg_mf.rolling(length).sum()
    return 100 - (100 / (1 + mfr))


def roc(close: pd.Series, length: int = 9) -> pd.Series:
    return ((close - close.shift(length)) / close.shift(length)) * 100


def adx(df: pd.DataFrame, length: int = 14) -> pd.Series:
    high, low, close = df["high"], df["low"], df["close"]

    plus_dm = high.diff()
    minus_dm = low.diff().abs()

    plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0.0)
    minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0.0)

    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(length).mean()

    plus_di = 100 * (plus_dm.rolling(length).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(length).mean() / atr)

    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    return dx.rolling(length).mean()


# ==============================
# Demo Runner
# ==============================

if __name__ == "__main__":
    provider = YahooFinanceProvider()
    df = provider.fetch_ohlcv("AAPL", start="2023-01-01")

    df["RSI"] = rsi(df["close"])
    df["VWAP"] = vwap(df)
    df["MFI"] = mfi(df)
    df["ROC"] = roc(df["close"])
    df["ADX"] = adx(df)

    print(df.tail())
