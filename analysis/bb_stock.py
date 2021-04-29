"""
A Bollinger Band® is a technical analysis tool defined by a set of trendlines plotted two standard deviations
    positively and negatively) away from a simple moving average (SMA) of a security's price, but which
    can be adjusted to user preferences.

This Module outputs a stacked graph featuring:
  Bollinger Bands with candlestick close prices
  Volume
  %b
  Bandwidth

"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


# @time_this
def compute_bb(eod_data: pd.DataFrame,
               moving_avg_window: int = 21,
               std_window: int = 21,
               volume_window: [int] = 21,
               multiplier: int = 2) -> pd.DataFrame:
    # Calculating a 21 day moving average
    eod_data['MA_Close'] = eod_data['Adj Close'].rolling(window=moving_avg_window).mean()

    # Calculating the standard deviation of the adjusted close
    eod_data['std'] = eod_data['Adj Close'].rolling(window=std_window).std()

    # This is calculating the upper band
    eod_data['BOLU'] = eod_data['MA_Close'] + (multiplier * eod_data['std'])

    # This is calculating the lower band
    eod_data['BOLD'] = eod_data['MA_Close'] - (multiplier * eod_data['std'])

    # Calculating the 50 day average volume
    eod_data['MA_Volume'] = eod_data['Volume'] \
        .rolling(window=volume_window) \
        .mean()

    # Calculating %b
    eod_data['pct_b'] = ((eod_data['Adj Close'] - eod_data['BOLD']) / (eod_data['BOLU'] - eod_data['BOLD']))

    # Calculating the bandwidth
    eod_data['Bandwidth'] = (eod_data['BOLU'] - eod_data['BOLD']) / eod_data['MA_Close']
    eod_data.loc[:, :].fillna(0, inplace=True)

    return eod_data


def graph_bb(data_frame: pd.DataFrame) -> None:
    # bb_data = data_frame[['open', 'close', 'low', 'high']]
    fig, axs = plt.subplots(4, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [3, 1, 1, 1]})
    plt.subplots_adjust(top=0.947, bottom=0.087, left=0.071, right=0.989, hspace=0.918, wspace=0.2)
    plt.tight_layout()

    # added formatting for axis labels
    locator = mdates.AutoDateLocator(minticks=5, maxticks=30)

    axs[0].set_title('Bollinger Bands')
    # axs[0].boxplot(bb_data.T, whis=[0,100])
    axs[0].plot(data_frame[['MA_Close', 'BOLU', 'BOLD']])

    axs[0].scatter(data_frame.index, data_frame[['Adj Close']], s=1.0, c='k', marker=',')
    axs[0].xaxis.set_major_locator(locator)
    axs[0].set_ylabel('Price')
    axs[0].grid(True)

    # x day Moving Average Volume Subplot
    axs[1].set_title('Volume')
    axs[1].bar(data_frame.index, data_frame['Volume'])
    axs[1].plot(data_frame.index, data_frame['MA_Volume'], color='black')
    axs[1].xaxis.set_major_locator(locator)
    axs[1].set_ylabel('Volume')
    axs[1].grid(True)

    # %b Subplot
    axs[2].set_title('%B')
    axs[2].plot(data_frame.index, data_frame['pct_b'], color='black')
    axs[2].xaxis.set_major_locator(locator)
    axs[2].set_ylabel('%B')
    axs[2].grid(True)

    # bandwidth Subplot
    axs[3].set_title('Bandwidth')
    axs[3].plot(data_frame.index, data_frame['Bandwidth'], color='black')
    axs[3].xaxis.set_major_locator(locator)
    axs[3].set_xlabel('Date')
    axs[3].set_ylabel('Bandwidth')
    axs[3].grid(True)
    plt.show()
