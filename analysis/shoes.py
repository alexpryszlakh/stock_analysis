import pandas as pd

def compute_pctb(eow_data: pd.DataFrame,
                 moving_avg_window: int = 21,
                 std_window: int = 21,
                 multiplier: int = 2) -> int:
    eow_data = eow_data.tail(150)  # getting recent stock data

    # getting the moving average and std
    ma_close = eow_data['Adj Close'].rolling(window=moving_avg_window).mean()
    std = eow_data['Adj Close'].rolling(window=std_window).std()

    # upper and lower bands
    bolu = ma_close + (multiplier * std)
    bold = ma_close - (multiplier * std)

    # obtaining percent be and checking if it is low
    # low means opportunity
    pct_b = ((eow_data['Adj Close'] - bold) / (bolu - bold))
    if pct_b.iloc[-1] <= 0.25:
        return 1

