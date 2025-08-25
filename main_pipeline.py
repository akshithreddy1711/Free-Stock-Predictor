import argparse
from fetch_data import fetch_and_store
from features import build_features
from train_model import train_all
from utils import DEFAULT_TICKERS

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tickers", type=str, default=",".join(DEFAULT_TICKERS))
    parser.add_argument("--fetch", action="store_true")
    parser.add_argument("--features", action="store_true")
    parser.add_argument("--train", action="store_true")
    args = parser.parse_args()

    tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]

    if args.fetch:
        fetch_and_store(tickers)
    if args.features or args.train:
        build_features()
    if args.train:
        train_all()

    if not (args.fetch or args.features or args.train):
        fetch_and_store(tickers)
        build_features()
