# Free Real‑Time Stock Predictor

An end‑to‑end, zero‑cost pipeline: Alpha Vantage → SQLite → TA features → Random Forest → Streamlit dashboard. Automated with GitHub Actions.

## Stack
- Data: Alpha Vantage (free tier)
- Storage: SQLite
- Modeling: scikit‑learn (RandomForestRegressor)
- Dashboard: Streamlit
- CI/CD: GitHub Actions

## Quickstart
```bash
pip install -r requirements.txt
export ALPHAVANTAGE_API_KEY="YOUR_KEY"   # Windows: set ALPHAVANTAGE_API_KEY=YOUR_KEY
python main_pipeline.py --fetch --tickers MSFT,AAPL
python main_pipeline.py --train  --tickers MSFT,AAPL
streamlit run app.py
```

## Deploy Free
- **Streamlit Community Cloud**: Connect this repo; set `ALPHAVANTAGE_API_KEY` in Secrets; main file: `app.py`.
- **Hugging Face Spaces (Gradio/Streamlit)**: similar steps.

## Automations
- `.github/workflows/fetch.yml`: refresh data on weekdays and commit `stock_data.db`.
- `.github/workflows/retrain.yml`: weekly model retrain; commits models to `models/`.

> Note: Committing a SQLite DB increases repo size over time; rotate or prune if needed.

## Disclaimer
Educational project; not financial advice. Past performance ≠ future results.
