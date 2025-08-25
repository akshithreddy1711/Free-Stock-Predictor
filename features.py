import sqlite3
import pandas as pd
import ta
from utils import DB_PATH

FEATURES_SCHEMA = """
CREATE TABLE IF NOT EXISTS features (
  ticker TEXT NOT NULL,
  date   TEXT NOT NULL,
  close  REAL,
  sma_5  REAL,
  sma_10 REAL,
  rsi_14 REAL,
  macd   REAL,
  macd_signal REAL,
  macd_hist REAL,
  PRIMARY KEY (ticker, date)
);
"""

UPSERT_FEATURES = """
INSERT INTO features (ticker, date, close, sma_5, sma_10, rsi_14, macd, macd_signal, macd_hist)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(ticker, date) DO UPDATE SET
  close=excluded.close,
  sma_5=excluded.sma_5,
  sma_10=excluded.sma_10,
  rsi_14=excluded.rsi_14,
  macd=excluded.macd,
  macd_signal=excluded.macd_signal,
  macd_hist=excluded.macd_hist;
"""

def build_features():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(FEATURES_SCHEMA)

    prices = pd.read_sql_query("SELECT * FROM prices ORDER BY ticker, date", conn, parse_dates=["date"])
    for tck, df in prices.groupby("ticker"):
        df = df.sort_values("date").reset_index(drop=True)
        df["sma_5"]  = df["close"].rolling(5).mean()
        df["sma_10"] = df["close"].rolling(10).mean()
        rsi = ta.momentum.RSIIndicator(df["close"], window=14)
        df["rsi_14"] = rsi.rsi()
        macd = ta.trend.MACD(close=df["close"], window_slow=26, window_fast=12, window_sign=9)
        df["macd"] = macd.macd()
        df["macd_signal"] = macd.macd_signal()
        df["macd_hist"] = macd.macd_diff()

        out = df.dropna(subset=["sma_5","sma_10","rsi_14","macd","macd_signal","macd_hist"]).copy()
        recs = [
            (
                tck,
                d.date().isoformat(),
                float(c), float(s5), float(s10), float(rsi14), float(m), float(ms), float(mh)
            )
            for d, c, s5, s10, rsi14, m, ms, mh in zip(
                out["date"], out["close"], out["sma_5"], out["sma_10"], out["rsi_14"], out["macd"], out["macd_signal"], out["macd_hist"]
            )
        ]
        cur.executemany(UPSERT_FEATURES, recs)
        conn.commit()

    conn.close()
    print("Features updated.")

if __name__ == "__main__":
    build_features()
