"""
Moving average convergence divergence (MACD) is a trend-following momentum
    indicator that shows the relationship between two moving averages of a security’s
    price. The MACD is calculated by subtracting the 26-period exponential moving
    average (EMA) from the 12-period EMA.
"""
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from progiler import time_this
from typing import Union


# @time_this
def compute_macd(eod_data: pd.DataFrame,
                 sm_window: int = 12,
                 lg_window: int = 26) -> pd.DataFrame:
    sm_exp = eod_data['Adj Close'].ewm(span=sm_window,
                                       adjust=False).mean()  # getting the exp. moving average of the first period
    lg_exp = eod_data['Adj Close'].ewm(span=lg_window,
                                       adjust=False).mean()  # getting the exp. moving average of the second period

    macd_calc = sm_exp - lg_exp  # obtaining the MACD from subtracting the EMA's
    eod_data['MACD'] = macd_calc  # putting MACD into the dataframe

    eod_data['MACD_MA'] = macd_calc.rolling(window=9).mean()  # obtaining the moving average of the MACD
    eod_data.loc[:, :].fillna(0, inplace=True)

    return eod_data


# @time_this
def graph_macd(data_frame: pd.DataFrame) -> None:

    # macd_data = data_frame[['open', 'close', 'low', 'high']]
    fig, axs = plt.subplots(3, 1, figsize=(20, 10), gridspec_kw={'height_ratios': [3, 1, 2]})
    plt.subplots_adjust(top=0.947, bottom=0.087, left=0.071, right=0.989, hspace=0.918, wspace=0.2)

    # added formatting for axis labels
    locator = mdates.AutoDateLocator(minticks=5, maxticks=30)

    axs[0].set_title('MACD')
    axs[0].plot(data_frame[['MACD']], label="MACD")
    axs[0].plot(data_frame[['MACD_MA']], label="Signal Line")
    axs[0].legend()
    axs[0].xaxis.set_major_locator(locator)
    axs[0].set_ylabel('MACD')
    axs[0].grid(True)

    # histogram with moving average Subplot
    axs[1].set_title('MACD')
    axs[1].bar(data_frame.index, data_frame['MACD'])
    axs[1].plot(data_frame.index, data_frame['MACD_MA'], color='black')
    axs[1].xaxis.set_major_locator(locator)
    axs[1].set_ylabel('MACD')
    axs[1].grid(True)

    # price Subplot
    axs[2].set_title('Price')
    axs[2].plot(data_frame.index, data_frame['Close'], color='black')
    axs[2].xaxis.set_major_locator(locator)
    axs[2].set_xlabel('Date')
    axs[2].set_ylabel('Price')
    axs[2].grid(True)

    return plt.show()


def compute_mcd(eod_data: pd.DataFrame,
                 sm_window: int = 12,
                 lg_window: int = 26) -> Union[int, float]:
    sm_exp = eod_data['Adj Close'].ewm(span=sm_window,
                                       adjust=False).mean()  # getting the exp. moving average of the first period
    lg_exp = eod_data['Adj Close'].ewm(span=lg_window,
                                       adjust=False).mean()  # getting the exp. moving average of the second period

    macd_calc = sm_exp - lg_exp  # obtaining the MACD from subtracting the EMA's
    eod_data['MACD'] = macd_calc  # putting MACD into the dataframe

    eod_data['MACD_MA'] = macd_calc.rolling(window=9).mean()  # obtaining the moving average of the MACD

    # determining where the macd is in relation to signal line
    # returns a buy oppurtunity when macd passes signal line on present day with past lower than signal
    if eod_data['MACD'].iloc[-2] <= eod_data['MACD_MA'].iloc[-2] and \
            eod_data['MACD'].iloc[-1] >= eod_data['MACD_MA'].iloc[-1]:
        success = 1
        return success
    # return value is if both present and past is below signal line
    if eod_data['MACD'].iloc[-2] <= eod_data['MACD_MA'].iloc[-2] and \
            eod_data['MACD'].iloc[-1] <= eod_data['MACD_MA'].iloc[-1]:
        success = 0
        return success
    # return value is if past is above signal but then goes down again in present
    if eod_data['MACD'].iloc[-2] >= eod_data['MACD_MA'].iloc[-2] and \
            eod_data['MACD'].iloc[-1] <= eod_data['MACD_MA'].iloc[-1]:
        success = .5
        return success
    # both present and pass are above signal, potential buy
    if eod_data['MACD'].iloc[-2] >= eod_data['MACD_MA'].iloc[-2] and \
            eod_data['MACD'].iloc[-1] >= eod_data['MACD_MA'].iloc[-1]:
        success = -1
        return success
