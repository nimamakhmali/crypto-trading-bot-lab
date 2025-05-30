import pandas as pd 

df = pd.read_csv("lbank_1min_candles.csv", parse_dates=['time'], index_col='time')

df['SMA_25'] = df['close'].rolling(window=25).mean()
df['SMA_50'] = df['close'].rolling(window=50).mean()
df.to_csv("lbank_1min_candles.csv")
print("SMAs accepted")