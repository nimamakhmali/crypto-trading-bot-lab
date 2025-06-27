import os
import pandas as pd
import mplfinance as mpf
from config import symbol

data_dir = "Data"
df = pd.read_csv(os.path.join(data_dir, "kbars.csv"))
output_file = os.path.join(data_dir, f"{symbol}_1min_candles.csv")

df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)

candles = df.resample('1T').agg({
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum'
}).dropna()

candles.to_csv(output_file)
# print(f" Read {symbol}_1min_candles.csv")

# mpf.plot(candles, type='candle', volume=True, style='charles', title=f'{symbol} 1-Min Candles')
#indexing