import pandas_datareader.data as web
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging
import datetime, time


data_sources = ['GOOGL', 'AAPL', 'MSFT']

tickers = [yf.Ticker(ticker) for ticker in data_sources]
def get_stock_prices(tickers):
    data = yf.download(list(tickers), group_by='column', period="1000d", interval='1d')
    return data[['Open', 'Close', 'High', 'Low', 'Volume']]

def get_multiple_financials(tickers):
    # tickers = [yf.Ticker(ticker) for ticker in tickers]
    dfs = [] # list for each ticker's dataframe
    print('Called financials %s' % (tickers.length))
    for ticker in tickers:
        # get each financial statement
        pnl = ticker.financials
        bs = ticker.balancesheet
        cf = ticker.cashflow
        print("t.financials: %s, t.balancesheet: %d, t.cashflow: %d" % (pnl.info(), bs.info(), cf))
        # concatenate into one dataframe
        fs = pd.concat([pnl, bs, cf])

        options = ticker.options
        print("options.info: %s, ' [Calls]: %s , [Puts]: %d" %(options.info, options.calls, options.puts))
        # make dataframe format nicer
        # Swap dates and columns
        data = fs.T
        # reset index (date) into a column
        data = data.reset_index()
        # Rename old index from '' to Date
        data.columns = ['Date', *data.columns[1:]]
        # Add ticker to dataframe
        data['Ticker'] = ticker.ticker
        dfs.append(data)
    df = pd.concat(dfs, ignore_index=True)
    df = df.T.drop_duplicates().T
    df = df.set_index(['Ticker','Date'])
    return df

def get_calls(ticker):
    tck = yf.Ticker(ticker)
    options = tck.option_chain()
    return options.calls

def get_puts(ticker):
    tck = yf.Ticker(ticker)
    options = tck.option_chain()
    return options.puts

def get_institutional_holders(ticker):
    tck = yf.Ticker(ticker)
    return tck.institutional_holders

data = {}
def run():
    for source in data_sources:
        try:
            # Fetch data
            data[source] = get_stock_prices(tickers)
            print('data: ' + data)
            print(tickers)
            # Pause for 1 seconds
            time.sleep(4)
        except Exception as e:
            print(f"Error fetching {source}: {e}")
            
    return get_multiple_financials(tickers)

