from bb_stock import compute_bb
from bb_stock import graph_bb
from macd_stock import compute_macd
from macd_stock import graph_macd
import pandas_datareader.data as web
import datetime as dt

ticker = ''  # place ticker symbol

# gathering the data
start = dt.datetime(2021, 2, 1)  # Creating a start date of beg. of 2020 for stock
end = dt.datetime.now()  # Creating an end date
df = web.DataReader(ticker, 'yahoo', start, end)  # reading data from yf to then store as a df

# computing bb info
bb = compute_bb(df)
print(bb)
graph_bb(bb)

# computing macd info
macd = compute_macd(df)
graph_macd(macd)
