# Import the yfinance. If you get module not found error the run !pip install yfinance from your Jupyter notebook
import yfinance as yf
import pandas as pd
import datetime
from curl_cffi import requests
import argparse

#Function for making conversion
def convert_usd(row,usdmyr):
    if row['Country'] == 'US':
        price_myr = format(float(row['LastPrice'])*float(usdmyr),".2f")
    elif row['Country'] != 'US':
        price_myr = row['LastPrice']
    return price_myr

def get_price(ticker, strtDate, endDate):

    tickerinfo = yf.Ticker(ticker,session=session)
    ticker_historydata = tickerinfo.history(start = strtDate, end = endDate)
    ticker_historydata = ticker_historydata.reset_index()

    ticker_historydata['Date'] = pd.to_datetime(ticker_historydata['Date']).dt.date
    ticker_historydata['Ticker'] = ticker
    ticker_historydata = ticker_historydata[['Ticker','Date','Close']]

    ticker_historydata['Date'] = pd.to_datetime(ticker_historydata['Date'])
    ticker_historydata = ticker_historydata.resample('W', on='Date').last().reset_index()

    # Calculate percentage change over the previous row
    ticker_historydata['Change%'] = ticker_historydata['Close'].pct_change() * 100

    # Format 'Close' and 'Change%' to 3 decimal points
    ticker_historydata['Close'] = ticker_historydata['Close'].round(3)
    ticker_historydata['Change%'] = ticker_historydata['Change%'].round(3)

    return ticker_historydata

def main():
    parser = argparse.ArgumentParser(description="Fetch historical stock data.")
    parser.add_argument("--ticker", type=str, help="Stock ticker symbol")
    parser.add_argument("--startdate", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--enddate", type=str, help="End date in YYYY-MM-DD format")

    args = parser.parse_args()

    ticker = args.ticker
    tickers = ticker.split(',')
    startdate = datetime.datetime.strptime(args.startdate, "%Y-%m-%d").date()
    enddate = datetime.datetime.strptime(args.enddate, "%Y-%m-%d").date()

    # Example usage of the parsed arguments
    for ticker1 in tickers:
        print(f"Fetching data for ticker: {ticker1}, from {startdate} to {enddate}")
        ticker_historydata = get_price(ticker1, startdate, enddate)
        ticker_historydata.to_csv(f"{ticker1}_historical_data.csv", index=False)
        print(f"{ticker1} historical data saved to {ticker1}_historical_data.csv")

if __name__ == "__main__":
    session = requests.Session(impersonate="chrome")

    main()
