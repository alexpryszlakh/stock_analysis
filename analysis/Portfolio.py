import datetime as dt

import pandas_datareader.data as web

from stripper import convert_to_dt

import pandas as pd

df = convert_to_dt('Porto.csv')

end = dt.datetime.now()
start = dt.datetime.now()

symbols = []
prices = []
close = []
state = []
profit = []
total_profit = []

for ticker, buy_price, share in zip(df['Symbol'], df['Price'], df['Shares']):
    end = dt.datetime.now()
    start = dt.datetime(2020, 1, 1)
    df_ = web.DataReader(str(ticker), 'yahoo', start, end)
    # print(str(ticker) + ' ' + str(buy_price))
    current_close = df_['Adj Close'].iloc[-1]
    difference = current_close - buy_price
    total = difference*share
    status = current_close - buy_price
    # print(status)
    if status >= 0:
        condition = 'Fire'
    else:
        condition = 'Trash'
    symbols.append(ticker)
    prices.append(buy_price)
    close.append(current_close)
    state.append(condition)
    profit.append(difference)
    total_profit.append(total)


final_df = pd.DataFrame(list(zip(symbols, prices, close, profit, total_profit, state)),
                        columns=['Ticker', 'Buy Price', 'Current Close', 'Profit', 'Total Profit', 'Condition'])
print(final_df)
