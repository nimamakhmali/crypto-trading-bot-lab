import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

def draw_chart():
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

    # قبل از رسم جدید، تمام پنجره‌های قبلی رو ببند
    plt.close("all")
    mpf.plot(candles, type='candle', volume=True, style='charles', title='LBank 1-Min Candles')
    print("✅ Chart plotted")

if __name__ == "__main__":
    draw_chart()
