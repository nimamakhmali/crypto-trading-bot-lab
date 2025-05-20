import pandas as pd
import mplfinance as mpf


df = pd.read_csv("lbank_kbars.csv")

df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)

candles = df.resample('1T').agg({
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum'
}).dropna()


candles.to_csv("lbank_1min_candles.csv")
print(" Read lbank_1min_candles.csv")

mpf.plot(candles, type='candle', volume=True, style='charles', title='LBank 1-Min Candles')


#indexing 

