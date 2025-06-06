import pandas as pd
import numpy as np
import pandas_ta as ta
import matplotlib.pyplot as plt
from trendline_automation import fit_trendline_single
import mplfinance as mpf

def trendline_breakout(close: np.array, lookback:int):
    s_t1 = np.zeros(len(close))
    s_t1[:] = np.nan
    r_t1 = np.zeros(len(close))
    r_t1[:] = np.nan
    sig = np.zeros(len(close))
    for i in range(lookback, len(close)):
        window = close[i - lookback: i]
        s_coefs, r_coefs = fit_trendline_single(window)
        s_val = s_coefs[1] + lookback * s_coefs[0]
        r_val = r_coefs[1] + lookback * r_coefs[0]
        s_t1[i] = s_val
        r_t1[i] = r_val
        if close[i] > r_val:
            sig[i] = 1.0
        elif close[i] < s_val:
            sig[i] = -1.0
        else:
            sig[i] = sig[i - 1]
    return s_t1, r_t1, sig       

if __name__ == "__main__":
    data = pd.read_csv("lbank_1min_candles.csv")
    data['time'] = data['time'].astype('datetime64[s]')
    data = data.set_index('time')
    data = data.dropna()
    
    lookback = 72
    support, resist, signal = trendline_breakout(data['close'].to_numpy(), lookback)
    data['support'] = support
    data['resist'] = resist
    data['signal'] = signal

    plt.style.use('dark_background')
    data['close'].plot(label='Close')
    data['resist'].plot(label='Resistance', color='green')
    data['support'].plot(label='Support', color='red')
    plt.show()

    data['r'] = np.log(data['close']).diff().shift(-1)
    strat_r = data['signal'] * data['r']

    pf = strat_r[strat_r > 0].sum() / strat_r[strat_r < 0].abs().sum() 
    print("Profit Factor", lookback,  pf)

    strat_r.cumsum().plot()
    plt.ylabel("Cumulative Log Return")
    plt.show()
    