import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from trendline_Break_dataset import trendline_breakout_dataset
from walkforward import walkforward_model

plt.style.use('dark_background')

def prof_factor(rets):
    return rets[rets > 0].sum() / rets[rets < 0].abs().sum()

def main():
    # 1. Load Data
    data = pd.read_csv('lbank_1min_candles.csv')
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')
    data = data.dropna()

    # 2. Extract trades and features
    lookback = 72
    trades, data_x, data_y = trendline_breakout_dataset(data, lookback)
    trades = trades.dropna()

    # 3. Walk-forward prediction
    train_size = 10000
    step_size = 5000
    signal, prob = walkforward_model(
        np.log(data['close']).to_numpy(),
        trades, data_x, data_y,
        train_size, step_size
    )

    # 4. Signal assignment
    data['sig'] = signal
    data['dumb_sig'] = prob
    data.loc[data['dumb_sig'] > 0, 'dumb_sig'] = 1
    data['r'] = np.log(data['close']).diff().shift(-1)

    # 5. Performance Analysis
    all_r = trades['return']
    mod_r = trades[trades['model_prob'] > 0.5]['return']
    no_filter_rets = data['r'] * data['dumb_sig']
    filter_rets = data['r'] * data['sig']

    print("\n---------- Performance Metrics ----------")
    print("All Trades PF:", prof_factor(no_filter_rets))
    print("All Trades Avg:", all_r.mean())
    print("All Trades Win Rate:", len(all_r[all_r > 0]) / len(all_r))
    print("All Trades Time In Market:", len(data[data['dumb_sig'] > 0]) / len(data))

    print("\nMeta-Label Trades PF:", prof_factor(filter_rets))
    print("Meta-Label Trades Avg:", mod_r.mean())
    print("Meta-Label Trades Win Rate:", len(mod_r[mod_r > 0]) / len(mod_r))
    print("Meta-Label Time In Market:", len(data[data['sig'] > 0]) / len(data))

    # 6. Plotting
    (filter_rets).cumsum().plot(label='Meta-Labeled')
    (no_filter_rets).cumsum().plot(label='All Trades')
    (data['r']).cumsum().plot(label='Buy & Hold')
    plt.legend()
    plt.title("Cumulative Log Returns")
    plt.ylabel("Return")
    plt.show()

if __name__ == "__main__":
    main()
