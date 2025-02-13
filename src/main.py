from timeit import timeit
import matplotlib.pyplot as plt
import logging
import time
import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
import datetime

tlist = ["AAPL", "MSFT"]
# tlist = ["SPY", "AMZN", "GOOG"]
logger = logging.getLogger(__name__)

DEFAULT_START_DATE = "2025-01-01"

DEFAULT_END_DATE = time.localtime()

FILE_PATH = "./2yearhistorical_data" + "".join(tlist) + ".csv"
interval_xterm = tuple(["1d", "5d", "1m", "3m", "6m", "1y", "2y", "3y", "5y"])
# Refactoring
# Initial Method to Pull Historical Quotes to csv file
# def autocrawl():
#     try:
#         data = yf.download(tlist, group_by="ticker", period="2y", interval="1d")
#         data.columns = pd.MultiIndex.from_tuples([i[::-1] for i in data.columns])
#         return download_csv(data)
#     except Exception as e:
#         logging.error(f"Error in autocrawl: {e}")
#         return "Returned Error On Download: {e}".format(e=e)


def fetch_stock_data(
    ticker: str, start_date: str, end_date: str = None, v="1d"
) -> pd.DataFrame:
    try:
        if interval_xterm.index(v) == None:
            raise Exception(f"{v} not in allowed interval bounds")

        if end_date is None:
            end_date = datetime.date.today().strftime("%Y-%m-%d")
        data = yf.download(ticker, start_date, end_date, interval=v, group_by="ticker")
        return data
    except Exception as e:
        logging.error(f"Error in fetch_stock_data: {e}")
        return


def download_csv(data):
    file_path = f"./{data['Ticker']}_{data['Date'].tail(1)}"
    print(data)
    data.to_csv(file_path, index=False)


from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List


def fetch_multiple_stocks(
    tickers: List[str], start_date: str, end_date: str = None, v: str = "1d"
) -> dict:
    results = {}

    with ThreadPoolExecutor() as executor:
        future_to_ticker = {
            executor.submit(
                fetch_stock_data,
                ticker,
                start_date,
                end_date,
                v,
            ): ticker
            for ticker in tickers
        }

        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                results[ticker] = future.result()
            except Exception as exc:
                print(f"{ticker} generated an exception: {exc}")
    return results


def _options():
    aapl = yf.Ticker("aapl")
    options = aapl.option_chain()
    calls = options.calls
    puts = options.puts
    aapl.insitutional_holders


def plot(df):
    pass
    # plt.figure(figsize=(12, 6))
    # plt.title("20-Day Moving Average")
    # plt.xlabel("Date")
    # plt.ylabel("Price (USD)")
    # plt.plot(df.index, historical_data["Close"], label="Close Price")
    # plt.plot(
    #     df.index,
    #     df["20 Day MA"],
    #     label="20 Day MA",
    #     linestyle="--",
    # )
    # download_csv(historical_data)


if __name__ == "__main__":
    start_time = time.time()
    df = fetch_multiple_stocks(
        ["BBAI", "SOUN"],
        "2024-01-01",
    )
    print(df)
    # df = pd.DataFrame.from_csv(data
    #     columns=["date", "Ticker", "High", "Low", "Close", "20 Day MA"]
    # )

    df.reset_index(True)
    print(df[0])
    print(df[0::10])
    print(
        "Execution Finished: {:.2f} elapsed seconds".format(
            time.time() - start_time, None
        )
    )
