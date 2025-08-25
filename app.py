import sqlite3
import joblib
import pandas as pd
import plotly.express as px
import streamlit as st
from utils import DB_PATH, MODELS_DIR, DEFAULT_TICKERS

st.set_page_config(page_title="Free Stock Predictor", layout="wide")
st.title("📈 Free Stock Market Predictor")

# Sidebar
tickers = st.sidebar.text_input("Tickers (comma-separated)", ",".join(DEFAULT_TICKERS))
selected = st.sidebar.selectbox("Select ticker", [t.strip().upper() for t in tickers.split(",") if t.strip()])

# Load data
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query(
    "SELECT * FROM prices WHERE ticker = ? ORDER BY date", conn, params=(selected,), parse_dates=["date"]
)
fe = pd.read_sql_query(
    "SELECT * FROM features WHERE ticker = ? ORDER BY date", conn, params=(selected,), parse_dates=["date"]
)
conn.close()

if df.empty:
    st.warning("No data yet. Run the pipeline or wait for the next fetch job.")
else:
    fig = px.line(df, x="date", y="close", title=f"{selected} Close Price")
    st.plotly_chart(fig, use_container_width=True)

    # Try to load model
    model_path = MODELS_DIR / f"{selected}_rf.pkl"

    if model_path.exists() and not fe.empty:
        bundle = joblib.load(model_path)
        model = bundle["model"]
        feat_cols = bundle["features"]
        latest_row = fe.dropna().iloc[-1]
        X_latest = latest_row[feat_cols].values.reshape(1, -1)
        pred = float(model.predict(X_latest)[0])
        st.success(f"Next day predicted close for **{selected}**: **{pred:.2f}**")
    else:
        st.info("Model not found yet. Showing simple SMA(5) as a baseline.")
        if len(df) >= 5:
            sma5 = df["close"].tail(5).mean()
            st.write(f"Baseline SMA(5): {sma5:.2f}")

    st.subheader("Recent Data")
    st.dataframe(df.tail(20).iloc[::-1], use_container_width=True)
