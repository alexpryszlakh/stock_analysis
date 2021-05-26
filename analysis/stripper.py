import pandas as pd


def convert_to_df(ticker_csv: str) -> pd.DataFrame:
    df = pd.read_csv(ticker_csv)
    df.set_index('Date', inplace=True)
    #df.index = pd.to_datetime(df.index, format='%Y-%m-%d').strftime('%m-%d')
    return df


#convert_to_df('AWU.csv')
def convert_to_dt(ticker_csv: str) -> pd.DataFrame:
    df = pd.read_csv(ticker_csv)
    #df.index = pd.to_datetime(df.index, format='%Y-%m-%d').strftime('%m-%d')
    return df