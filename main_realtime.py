import time
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
from target_strategy.pattern.main_strategy import (
    find_pivots,
    detect_123_patterns_precise,
    generate_trades,
    calculate_rsi,
    FIB_LEVELS,
    PIVOT_WINDOW
)

CSV_PATH = os.path.join(os.path.dirname(__file__), 'Data', 'btc_usdt_1min_candles.csv')
CHECK_INTERVAL = 30  # second 

def plot_last_signal(df, fib_lines, last_trade):
    # فقط آخرین 100 کندل را رسم کن
    df_plot = df.tail(100)
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(16, 8),
        gridspec_kw={'height_ratios': [8, 2]},
        sharex=True
    )
    # چارت قیمت و اندیکاتورها
    ax1.plot(df_plot.index, df_plot['close'], label='Close', color='gray', linewidth=1)
    ax1.plot(df_plot.index, df_plot['SMA_25'], label='SMA 25', color='blue', linewidth=1)
    ax1.plot(df_plot.index, df_plot['SMA_50'], label='SMA 50', color='orange', linewidth=1)
    ax1.bar(df_plot.index, df_plot['volume'], color='lightgray', alpha=0.4, label='Volume', width=0.0008)
    # نقاط ورود (تگ 3)
    ax1.scatter(df_plot.index[df_plot['tag3'] == 1], df_plot['close'][df_plot['tag3'] == 1], color='green', marker='v', s=60, label='Tag 3')
    # خطوط موج و فیبوناچی
    for idx1, idx2, idx3, fibs, direction in fib_lines:
        if df.index[idx3] not in df_plot.index:
            continue
        ax1.plot(df.index[[idx1, idx2, idx3]], df['close'].iloc[[idx1, idx2, idx3]], color='purple', linestyle='--', linewidth=1)
        for i, fib in enumerate(fibs):
            color = 'red' if direction == 'up' else 'blue'
            ax1.hlines(fib, df.index[idx1], df.index[idx3], colors=color, linestyles='dotted', linewidth=1)
            level = FIB_LEVELS[i]
            ax1.text(df.index[idx3], fib, f'{level:.3f}', color=color, fontsize=8, va='bottom', ha='right', alpha=0.8)
    # نمایش معامله آخر
    ax1.scatter(last_trade['entry_time'], last_trade['entry_price'], color='black', marker='*', s=120, label='Entry')
    ax1.hlines(last_trade['target_price'], last_trade['entry_time'], last_trade['target_time'], colors='green', linestyles='dashdot', linewidth=1, label='Target')
    ax1.hlines(last_trade['stop_price'], last_trade['entry_time'], last_trade['target_time'], colors='red', linestyles='dashdot', linewidth=1, label='Stop Loss')
    ax1.set_title("Real-Time Signal & Chart")
    ax1.set_ylabel("Price")
    ax1.legend()
    ax1.grid(True)
    # RSI
    ax2.plot(df_plot.index, df_plot['RSI'], color='purple', label='RSI')
    ax2.axhline(y=70, color='red', linestyle='--', linewidth=1, label='Overbought (70)')
    ax2.axhline(y=30, color='green', linestyle='--', linewidth=1, label='Oversold (30)')
    ax2.set_ylabel('RSI')
    ax2.legend()
    ax2.grid(True)
    plt.tight_layout()
    plt.show()

def run_realtime_strategy():
    last_signal_time = None
    print("Real-time strategy started. Press Ctrl+C to stop.")
    while True:
        try:
            df = pd.read_csv(CSV_PATH, parse_dates=['time'])
            df.set_index('time', inplace=True)
            close = df['close'].values
            df['SMA_25'] = df['close'].rolling(window=25).mean()
            df['SMA_50'] = df['close'].rolling(window=50).mean()
            df['RSI'] = calculate_rsi(df)
            pivots = find_pivots(close, PIVOT_WINDOW)
            df, fib_lines = detect_123_patterns_precise(df, pivots, FIB_LEVELS)
            trades = generate_trades(df, fib_lines)
            if trades:
                last_trade = trades[-1]
                if last_signal_time is None or last_trade['entry_time'] > last_signal_time:
                    last_signal_time = last_trade['entry_time']
                    print(f"\n[NEW SIGNAL] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"Entry: {last_trade['entry_time']} | Price: {last_trade['entry_price']} | "
                          f"Target: {last_trade['target_price']} | Stop: {last_trade['stop_price']} | "
                          f"Direction: {last_trade['direction']}")
                    plot_last_signal(df, fib_lines, last_trade)
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No new signal.")
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("Stopped by user.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_realtime_strategy()