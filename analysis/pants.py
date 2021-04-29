from typing import Union
import pandas as pd


def compute_macd(eod_data: pd.DataFrame,
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
    if eod_data['MACD'].iloc[-2] <= eod_data['MACD_MA'].iloc[-2] and \
            eod_data['MACD'].iloc[-1] >= eod_data['MACD_MA'].iloc[-1]:
        success = 1
        return success
    if eod_data['MACD'].iloc[-2] <= eod_data['MACD_MA'].iloc[-2] and \
            eod_data['MACD'].iloc[-1] <= eod_data['MACD_MA'].iloc[-1]:
        success = 0
        return success
    if eod_data['MACD'].iloc[-2] >= eod_data['MACD_MA'].iloc[-2] and \
            eod_data['MACD'].iloc[-1] <= eod_data['MACD_MA'].iloc[-1]:
        success = .5
        return success
    if eod_data['MACD'].iloc[-2] >= eod_data['MACD_MA'].iloc[-2] and \
            eod_data['MACD'].iloc[-1] >= eod_data['MACD_MA'].iloc[-1]:
        success = -1
        return success
