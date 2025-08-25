# Free Real-Time Stock Predictor

[![Fetch Daily Prices](https://github.com/akshithreddy1711/Free-Stock-Predictor/actions/workflows/fetch.yml/badge.svg)](https://github.com/akshithreddy1711/Free-Stock-Predictor/actions/workflows/fetch.yml)
[![Weekly Retrain](https://github.com/akshithreddy1711/Free-Stock-Predictor/actions/workflows/retrain.yml/badge.svg)](https://github.com/akshithreddy1711/Free-Stock-Predictor/actions/workflows/retrain.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-brightgreen)](https://free-stock-predictor.streamlit.app/)

**Live app:** 👉 https://free-stock-predictor.streamlit.app/

> **CI/CD schedule (UTC → IST):**  
> – Fetch (data & features): Weekdays at **10:05 UTC** → **15:35 IST**  
> – Retrain (models): Saturdays at **10:15 UTC** → **15:45 IST**

---

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
