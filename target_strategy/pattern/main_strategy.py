import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'btc_usdt_1min_candles.csv')
FIB_LEVELS = [0.236, 0.382, 0.50, 0.618, 0.786]
PIVOT_WINDOW = 8

def is_pivot_low(data, i, w):
    if i < w or i > len(data) - w - 1:
        return False
    return all(data[i] < data[i-j] and data[i] < data[i+j] for j in range(1, w+1))

def is_pivot_high(data, i, w):
    if i < w or i > len(data) - w - 1:
        return False
    return all(data[i] > data[i-j] and data[i] > data[i+j] for j in range(1, w+1))

def find_pivots(close, window):
    pivots = []
    for i in range(len(close)):
        if is_pivot_low(close, i, window):
            pivots.append((i, 'low'))
        elif is_pivot_high(close, i, window):
            pivots.append((i, 'high'))
    return pivots

def calculate_rsi(df, period: int = 14):
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def detect_123_patterns_precise(df, pivots, fib_levels):
    tags = {i: [] for i in range(len(df))}
    fib_lines = []
    i = 0
    while i < len(pivots) - 2:
        idx1, t1 = pivots[i]
        j = i + 1
        while j < len(pivots) and pivots[j][1] == t1:
            j += 1
        if j >= len(pivots) - 1:
            break
        idx2, t2 = pivots[j]
        k = j + 1
        while k < len(pivots) and pivots[k][1] != t1:
            k += 1
        if k >= len(pivots):
            break
        idx3, t3 = pivots[k]
        p1, p2, p3 = df['close'].iloc[idx1], df['close'].iloc[idx2], df['close'].iloc[idx3]

        if t1 == 'low' and t2 == 'high' and t3 == 'low' and p3 > p1:
            fibs = [p2 - (p2 - p1) * level for level in fib_levels]
            if any(abs(p3 - fib) / (p2 - p1) < 0.07 for fib in fibs):
                tags[idx1].append(1)
                tags[idx2].append(2)
                tags[idx3].append(3)
                fib_lines.append((idx1, idx2, idx3, fibs, 'up'))
                i = k - 1
        elif t1 == 'high' and t2 == 'low' and t3 == 'high' and p3 < p1:
            fibs = [p2 + (p1 - p2) * level for level in fib_levels]
            if any(abs(p3 - fib) / (p1 - p2) < 0.07 for fib in fibs):
                tags[idx1].append(1)
                tags[idx2].append(2)
                tags[idx3].append(3)
                fib_lines.append((idx1, idx2, idx3, fibs, 'down'))
                i = k - 1
        i += 1

    tag1 = np.zeros(len(df), dtype=int)
    tag2 = np.zeros(len(df), dtype=int)
    tag3 = np.zeros(len(df), dtype=int)
    for idx, tlist in tags.items():
        if 1 in tlist:
            tag1[idx] = 1
        if 2 in tlist:
            tag2[idx] = 1
        if 3 in tlist:
            tag3[idx] = 1
    df['tag1'] = tag1
    df['tag2'] = tag2
    df['tag3'] = tag3
    return df, fib_lines

def generate_trades(df, fib_lines):
    trades = []
    for idx, (idx1, idx2, idx3, fibs, direction) in enumerate(fib_lines):
        entry_time = df.index[idx3]
        entry_price = df['close'].iloc[idx3]
        target_time = df.index[idx2]
        target_price = df['close'].iloc[idx2]
        # 
        fibs_sorted = sorted(fibs, reverse=(direction == 'down'))
        stop_price = None
        for i, fib in enumerate(fibs_sorted):
            if (direction == 'up' and entry_price > fib) or (direction == 'down' and entry_price < fib):
                # siuuuuuuuuuuu
                if i + 1 < len(fibs_sorted):
                    stop_price = fibs_sorted[i + 1]
                else:
                    stop_price = fibs_sorted[-1]
                break
        if stop_price is None:

            stop_price = fibs_sorted[-1]  # Siuuuuuuuuu

        trades.append({
            'entry_time': entry_time,
            'entry_price': entry_price,
            'target_time': target_time,
            'target_price': target_price,
            'stop_price': stop_price,
            'direction': direction
        })
    return trades

if __name__ == "__main__":
    df = pd.read_csv(CSV_PATH, parse_dates=['time'])
    df.set_index('time', inplace=True)
    close = df['close'].values

    # indicator
    df['SMA_25'] = df['close'].rolling(window=25).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['RSI'] = calculate_rsi(df)

    # pattern
    pivots = find_pivots(close, PIVOT_WINDOW)
    df, fib_lines = detect_123_patterns_precise(df, pivots, FIB_LEVELS)

    # positions
    trades = generate_trades(df, fib_lines)
    for trade in trades:
        print(f"Entry: {trade['entry_time']} | Price: {trade['entry_price']} | "
              f"Target: {trade['target_price']} | Stop: {trade['stop_price']} | Direction: {trade['direction']}")

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(18, 10),
        gridspec_kw={'height_ratios': [7, 3]},
        sharex=True
    )

    # chart
    ax1.plot(df.index, df['close'], label='Close', color='gray', linewidth=1)
    ax1.plot(df.index, df['SMA_25'], label='SMA 25', color='blue', linewidth=1)
    ax1.plot(df.index, df['SMA_50'], label='SMA 50', color='orange', linewidth=1)
    #ax1.bar(df.index, df['volume'], color='lightgray', alpha=0.4, label='Volume', width=0.0008)
    ax1.scatter(df.index[df['tag1'] == 1], df['close'][df['tag1'] == 1], color='blue', marker='o', s=60, label='Tag 1')
    ax1.scatter(df.index[df['tag2'] == 1], df['close'][df['tag2'] == 1], color='orange', marker='^', s=60, label='Tag 2')
    ax1.scatter(df.index[df['tag3'] == 1], df['close'][df['tag3'] == 1], color='green', marker='v', s=60, label='Tag 3')

    for idx1, idx2, idx3, fibs, direction in fib_lines:
        ax1.plot(df.index[[idx1, idx2, idx3]], df['close'].iloc[[idx1, idx2, idx3]], color='purple', linestyle='--', linewidth=1)
        for i, fib in enumerate(fibs):
            color = 'red' if direction == 'up' else 'blue'
            ax1.hlines(fib, df.index[idx1], df.index[idx3], colors=color, linestyles='dotted', linewidth=1)
            level = FIB_LEVELS[i]
            ax1.text(df.index[idx3], fib, f'{level:.3f}', color=color, fontsize=9, va='bottom', ha='right', alpha=0.5)

    # show Position on chart
    for trade in trades:
        # Entry
        ax1.scatter(trade['entry_time'], trade['entry_price'], color='black', marker='*', s=120, label='Entry' if trade == trades[0] else "")
        # Tp
        ax1.hlines(trade['target_price'], trade['entry_time'], trade['target_time'], colors='green', linestyles='dashdot', linewidth=1, label='Target' if trade == trades[0] else "")
        # Sl
        ax1.hlines(trade['stop_price'], trade['entry_time'], trade['target_time'], colors='red', linestyles='dashdot', linewidth=1, label='Stop Loss' if trade == trades[0] else "")

    ax1.set_title("123 Pattern Detection with SMA, Volume, Fibonacci & Trades")
    ax1.set_ylabel("Price")
    ax1.legend()
    ax1.grid(True)

    # RSI
    ax2.plot(df.index, df['RSI'], color='purple', label='RSI')
    ax2.axhline(y=70, color='red', linestyle='--', linewidth=1, label='Overbought (70)')
    ax2.axhline(y=30, color='green', linestyle='--', linewidth=1, label='Oversold (30)')
    ax2.set_ylabel('RSI')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()