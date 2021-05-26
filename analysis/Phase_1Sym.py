import datetime as dt

# from test import compute_bb
# import numpy as np
import pandas as pd
import pandas_datareader.data as web

from bb_p1 import compute_pctb
from stripper import convert_to_dt

# creating empty lists
ticker = []
Adj_Close = []

# putting in s&p 500 stocks
df = convert_to_dt('constituents_csv.csv')

# for loop to check all stocks
for i in df['Symbol']:
    start = dt.datetime(2020, 1, 1)  # Creating a start date of beg. of 2020 for stock
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
