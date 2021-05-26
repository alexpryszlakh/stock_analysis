from datetime import datetime
import pandas as pd
import numpy as np
import os
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


def _fillinValues(dataframe: pd.DataFrame) -> pd.DataFrame:
    '''
    Fill in NaN values
    '''
    dataframe.fillna(method='ffill', inplace=True)
    dataframe.fillna(method='bfill', inplace=True)
    return dataframe


def compute_net_returns(series: pd.Series) -> pd.Series:
    '''
    Net return(t) = Price(t)/Price(t-1) - 1
    from: page 13, Machine Trading by Chan, E.P.
    returns an instrument's net return
    dataframe is a dataframe that needs to be in the following format:
    index        0    1     2   3    4
    YYYY-MM-DD   open close low high volume
    '''
    price = series
    rets = price / price.shift(1) - 1
    # fill in NaN values
    rets = _fillinValues(rets)
    return rets


def compute_rsi(series: pd.Series, window=14) -> pd.Series:
    '''
    rsi: Relative Strength Index
        rsi = 100 - (100/(1+RS))
        RS = (avg of x days' up closes)/(avg of x days' down closes)
        avg of x days' up closes = total points gained on up days/weeks divide by x days/weeks
        avg of x days' down closes = total points lost on down days/weeks divide by x days/weeks
        from: page 239 Technical Analysis of the Financial Markets, 1st ed. by Murphy, John J.
        rets are the net returns. use function compute_net_returns() to calculate.
        window is x days for the moving average calculation
    returns a series of rsi values
    Completed rsi in 4.283 milliseconds
    '''
    # rsi algorithm validated against Excel: 2021-01-17v3

    # calculate daily net returns
    rets = compute_net_returns(series)
    # date_range is used to reindex after separating days up from days down
    date_range = rets.index
    up = rets.loc[rets.iloc[:] >= 0.0]
    up = up.reindex(date_range, fill_value=0.0)
    # _save_data('up', up)

    up_avg = up.rolling(window=window).mean()

    up_avg = up_avg.fillna(value=0.0)
    # _save_data('up_avg', up_avg)
    down = rets.loc[rets.iloc[:] < 0.0]
    down = down.reindex(date_range, fill_value=0.0)
    # _save_data('down', down)

    down_avg = down.rolling(window=window).mean() * -1

    down_avg = down_avg.fillna(value=0.0)
    # replace 0s with 1s
    down_avg.replace(to_replace=0.0, value=1.0)
    # _save_data('down_avg', down_avg)
    # calculate rsi
    rs = up_avg / down_avg
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.rename('rsi')
    rsi.fillna(value=1.0, inplace=True)
    return rsi


def graph_rsi(data_frame: pd.Series) -> None:
    plt.plot(data_frame)
    plt.ylabel('RSI')
    plt.xlabel('Date')
    return plt.show()
