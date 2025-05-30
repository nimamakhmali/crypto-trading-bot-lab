import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- main ceiling ---
def rw_top(data: np.array, curr_index: int, order: int) -> bool:
    if curr_index < order * 2 + 1:
        return False
    k = curr_index - order
    v = data[k]
    for i in range(1, order + 1):
        if data[k + i] > v or data[k - i] > v:
            return False
    return True

# --- main floor ---
def rw_bottom(data: np.array, curr_index: int, order: int) -> bool:
    if curr_index < order * 2 + 1:
        return False
    k = curr_index - order
    v = data[k]
    for i in range(1, order + 1):
        if data[k + i] < v or data[k - i] < v:
            return False
    return True

# --- ceiling and floor ---
def rw_extremes(data: np.array, order: int):
    tops = []
    bottoms = []
    for i in range(len(data)):
        if rw_top(data, i, order):
            tops.append([i, i - order, data[i - order]])
        if rw_bottom(data, i, order):
            bottoms.append([i, i - order, data[i - order]])
    return tops, bottoms

# --- main---
if __name__ == "__main__":
    
    df = pd.read_csv('lbank_1min_candles.csv')
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    order = 10
    close_prices = df['close'].to_numpy()
    tops, bottoms = rw_extremes(close_prices, order)
    df['close'].plot(figsize=(15, 5), title="Local Tops & Bottoms - LBank 1min Data")
    idx = df.index
    for top in tops:
        plt.plot(idx[top[1]], top[2], marker='o', color='green', label='Top' if top == tops[0] else "")
    for bottom in bottoms:
        plt.plot(idx[bottom[1]], bottom[2], marker='o', color='red', label='Bottom' if bottom == bottoms[0] else "")

    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
