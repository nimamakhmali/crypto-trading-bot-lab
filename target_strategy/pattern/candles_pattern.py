import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# parameter
ORDER = 5 # pivot

# === Pivot Detection functions ===
def rw_top(data, curr_index, order):
    if curr_index < order * 2 + 1:
        return False
    k = curr_index - order
    v = data[k]
    for i in range(1, order + 1):
        if data[k + i] > v or data[k - i] > v:
            return False
    return True

def rw_bottom(data, curr_index, order):
    if curr_index < order * 2 + 1:
        return False
    k = curr_index - order
    v = data[k]
    for i in range(1, order + 1):
        if data[k + i] < v or data[k - i] < v:
            return False
    return True

def rw_extremes(data, order):
    tops, bottoms = [], []
    for i in range(len(data)):
        if rw_top(data, i, order):
            tops.append([i, i - order, data[i - order]])
        if rw_bottom(data, i, order):
            bottoms.append([i, i - order, data[i - order]])
    return tops, bottoms

# === signal ===
def detect_combined_signals(df, order=10):
    close = df['close'].values
    open_ = df['open'].values

    tops, bottoms = rw_extremes(close, order)

    df['strategy_signal'] = 0  # 0 1 2

    for i in range(order * 2, len(df)):
        if i - 2 < 0:
            continue

        c1, c2, c3 = close[i - 2], close[i - 1], close[i]
        o1, o2, o3 = open_[i - 2], open_[i - 1], open_[i]

    # Bullish Signal
    if (
        c3 > o3 and c2 < o2 and c3 > o2 and
        any(abs(b[1] - (i - 2)) <= 2 for b in bottoms) and
        df['RSI'].iloc[i] < 65 and
        df['close'].iloc[i] > df['SMA_25'].iloc[i]
    ):
        df.iloc[i, df.columns.get_loc('strategy_signal')] = 2

    # Bearish Signal
    if (
        c3 < o3 and c2 > o2 and c3 < o2 and
        any(abs(t[1] - (i - 2)) <= 2 for t in tops) and
        df['RSI'].iloc[i] > 40 and
        df['close'].iloc[i] < df['SMA_25'].iloc[i]
    ):
        df.iloc[i, df.columns.get_loc('strategy_signal')] = 1

    return df, tops, bottoms

# === strategy ===
def run_strategy(csv_path: str, plot_range: int = 300):
    df = pd.read_csv(csv_path)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    df, tops, bottoms = detect_combined_signals(df, ORDER)

    # plot
    plt.figure(figsize=(15, 6))
    plt.plot(df['close'], label='Close Price', color='gray')

    for top in tops:
        plt.plot(df.index[top[1]], top[2], marker='o', color='green', label='Top' if top == tops[0] else "")
    for bottom in bottoms:
        plt.plot(df.index[bottom[1]], bottom[2], marker='o', color='red', label='Bottom' if bottom == bottoms[0] else "")

    buy_signals = df[df['strategy_signal'] == 2]
    sell_signals = df[df['strategy_signal'] == 1]
    plt.scatter(buy_signals.index, buy_signals['close'], marker='^', color='blue', s=100, label='Buy Signal')
    plt.scatter(sell_signals.index, sell_signals['close'], marker='v', color='black', s=100, label='Sell Signal')

    plt.title('Combined Strategy: Pivot + Engulfing Signal')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    start_index = df.index[-plot_range] if len(df) > plot_range else df.index[0]
    plt.xlim(start_index, df.index[-1])

    plt.show()

    return df


if __name__ == "__main__":
    df_result = run_strategy("lbank_1min_candles.csv")
    df_result.to_csv("lbank_1min_candles.csv")