import os
from pathlib import Path

DB_PATH = os.getenv("DB_PATH", "stock_data.db")
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_TICKERS = os.getenv("TICKERS", "MSFT,AAPL").split(",")

def get_api_key() -> str:
    return os.getenv("ALPHAVANTAGE_API_KEY", "")
