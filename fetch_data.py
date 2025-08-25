import time
import requests
import sqlite3
import pandas as pd
from utils import DB_PATH, get_api_key

ALPHA_URL = "https://www.alphavantage.co/query"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS prices (
  ticker TEXT NOT NULL,
  date   TEXT NOT NULL,
  open   REAL,
  high   REAL,
  low    REAL,
  close  REAL,
  volume INTEGER,
  PRIMARY KEY (ticker, date)
);
"""

UPSERT_SQL = """
INSERT INTO prices (ticker, date, open, high, low, close, volume)
VALUES (?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(ticker, date) DO UPDATE SET
  open=excluded.open,
  high=excluded.high,
  low=excluded.low,
  close=excluded.close,
  volume=excluded.volume;
"""

def _json_to_df(ticker: str, js: dict) -> pd.DataFrame:
    ts = js.get("Time Series (Daily)") or js.get("Time Series (Daily) ")
    if not ts:
        keys = list(js.keys())[:5]
        raise ValueError(f"Unexpected API response for {ticker}: {keys}")
    rows = []
    for d, vals in ts.items():
        rows.append({
            "ticker": ticker,
            "date": d,
            "open": float(vals["1. open"]),
            "high": float(vals["2. high"]),
            "low": float(vals["3. low"]),
            "close": float(vals["4. close"]),
            "volume": int(float(vals["5. volume"]))
        })
    df = pd.DataFrame(rows)
    df.sort_values("date", inplace=True)
    return df

def fetch_and_store(tickers, sleep_sec: int = 15):
    api_key = get_api_key()
    assert api_key, "ALPHAVANTAGE_API_KEY is missing"

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(SCHEMA_SQL)

    for i, t in enumerate(tickers):
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": t,
            "outputsize": "compact",
            "apikey": api_key,
        }
        r = requests.get(ALPHA_URL, params=params, timeout=30)
        js = r.json()
        if "Note" in js:
            time.sleep(60)
            r = requests.get(ALPHA_URL, params=params, timeout=30)
            js = r.json()
        df = _json_to_df(t, js)
        cur.executemany(UPSERT_SQL, df.to_records(index=False))
        conn.commit()
        if i < len(tickers) - 1:
            time.sleep(sleep_sec)

    conn.close()
    print(f"Fetched & stored: {tickers}")

if __name__ == "__main__":
    fetch_and_store(["MSFT", "AAPL"])
