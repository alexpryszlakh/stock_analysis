import pandas as pd
from stripper import convert_to_dt
import pandas_datareader.data as web
import datetime as dt
from pants import compute_macd

# creating empty lists
ticker = []
Adj_Close = []
status = []

# putting in filtered stocks
df = convert_to_dt('stocks')

# for loop to check all stocks
for i in df['Symbol']:
    start = dt.datetime(2021, 2, 1)  # Creating a start date of beg. of 2020 for stock
    end = dt.datetime.now()  # Creating an end date
    df = web.DataReader(str(i), 'yahoo', start, end)  # reading data from yf to then store as a df
    price = df['Adj Close'].iloc[-1]
    ticker.append(i)
    Adj_Close.append(price)
    result = compute_macd(df)

    # determinig what is the state of each stock in relation to MACD
    if result == 1:
        verdict = 'Buy'
        status.append(verdict)
    if result == .5:
        verdict = 'Second Wind'
        status.append(verdict)
    if result == 0:
        verdict = 'En camino'
        status.append(verdict)
    if result == -1:
        verdict = 'Look Now'
        status.append(verdict)

# creating a dictionary to turn into a pd.df
dict = {'Status': status, 'Symbol': ticker, 'Adj Close': Adj_Close}
symbols = pd.DataFrame(dict)

# printing complete and creating a csv
print('complete')
symbols.to_csv('Status')
