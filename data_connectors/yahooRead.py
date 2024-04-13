import datetime as dt
import yfinance as yf

if __name__ == "__main__":
    company = 'TATAELXSI.NS'

    # Define a start date and End Date
    start = dt.datetime(2020,1,1)
    end =  dt.datetime(2022,1,1)

    # Read Stock Price Data
    data = yf.download(company, start , end)

    print(data)