import pandas as pd
import mplfinance as mpf
import time
import matplotlib.pyplot as plt

plt.ion()  # مد تعاملی برای نمایش زنده

file_path = "lbank_kbars.csv"

while True:
    try:
        df = pd.read_csv(file_path)
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

        candles = df.resample('1T').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna()

        plt.clf()
        mpf.plot(candles, type='candle', volume=True, style='charles', title='Live LBank 1-Min Candles', block=False)
        plt.pause(1)

        print(" Chart updated.")
        time.sleep(60)

    except Exception as e:
        print(f" Error updating chart: {e}")
        time.sleep(10)
