import matplotlib.pyplot as plt
import logging
import time
import yfinance as yf
import pandas as pd

tlist = ["AAPL", "MSFT"]
# tlist = ["SPY", "AMZN", "GOOG"]

DEFAULT_START_DATE = "2025-01-01"

DEFAULT_END_DATE = time.localtime()

FILE_PATH = "./2yearhistorical_data" + "".join(tlist) + ".csv"


# Initial Method to Pull Historical Quotes to csv file
def autocrawl():
    try:
        data = yf.download(tlist, group_by="ticker", period="2y", interval="1d")
        data.columns = pd.MultiIndex.from_tuples([i[::-1] for i in data.columns])
        return download_csv(data)
    except Exception as e:
        logging.error(f"Error in autocrawl: {e}")
        return "Returned Error On Download: {e}".format(e=e)


def download_csv(data):
    print(data)
    data.to_csv(FILE_PATH)


def _options():
    aapl = yf.Ticker("aapl")
    options = aapl.option_chain()
    calls = options.calls
    puts = options.puts
    aapl.insitutional_holders


if __name__ == "__main__":
    data = autocrawl()
    print(data)
