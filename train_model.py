import sqlite3
import joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from utils import DB_PATH, MODELS_DIR

FEATURE_COLS = ["sma_5","sma_10","rsi_14","macd","macd_signal","macd_hist"]

def _load_features(conn):
    df = pd.read_sql_query("SELECT * FROM features ORDER BY ticker, date", conn, parse_dates=["date"])
    return df

def train_all():
    conn = sqlite3.connect(DB_PATH)
    feats = _load_features(conn)
    conn.close()

    results = {}
    for tck, df in feats.groupby("ticker"):
        df = df.sort_values("date").reset_index(drop=True)
        df["y_next"] = df["close"].shift(-1)
        df = df.dropna(subset=FEATURE_COLS + ["y_next"]).copy()
        if len(df) < 60:
            continue
        split = int(len(df) * 0.8)
        X_train, y_train = df.loc[:split-1, FEATURE_COLS], df.loc[:split-1, "y_next"]
        X_val,   y_val   = df.loc[split:, FEATURE_COLS],   df.loc[split:, "y_next"]

        model = RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        pred = model.predict(X_val)
        mae = float(mean_absolute_error(y_val, pred))

        out_path = MODELS_DIR / f"{tck}_rf.pkl"
        joblib.dump({"model": model, "features": FEATURE_COLS}, out_path)
        results[tck] = {"mae": mae, "n_train": len(X_train), "n_val": len(X_val)}
        print(f"{tck}: MAE={mae:.3f} | saved {out_path}")

    return results

if __name__ == "__main__":
    train_all()
