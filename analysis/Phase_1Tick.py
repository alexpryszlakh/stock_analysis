from bb_p1 import compute_pctb
# from test import compute_bb
# import numpy as np
import pandas as pd
from stripper import convert_to_dt
import pandas_datareader.data as web
import datetime as dt
from datetime import datetime
from macd_stock import compute_macd


# creating empty lists
ticker = []
Adj_Close = []

# putting in s&p 500 stocks
df = convert_to_dt('First_Screen.csv')

# for loop to check all stocks
for i in df['Ticker']:
    start = dt.datetime(2021, 1, 1)  # Creating a start date of beg. of 2020 for stock
    end = dt.datetime.now()  # Creating an end date
    df = web.DataReader(str(i), 'yahoo', start, end)  # reading data from yf to then store as a df

    # if statement to see if the price is less than 150 USD
    if df['Adj Close'].iloc[-1] < 150:

        # computing pctb
        pctb = compute_pctb(df)

        # checking to see if pctb is low
        if pctb == 1:
            price = df['Adj Close'].iloc[-1]
            ticker.append(i)
            Adj_Close.append(price)
            dict = {'Symbol': ticker, 'Adj Close': Adj_Close}
            symbols = pd.DataFrame(dict)
            print(i, price)
print('complete')

# creating a csv of all the filtered stocks
symbols.to_csv('stocks')