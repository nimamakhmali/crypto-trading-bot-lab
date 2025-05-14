import tkinter as tk
from tkinter import ttk
import pandas as pd
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def prepare_candles(symbol):
    df = pd.read_csv("lbank_kbars.csv")
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

   
    candles = df.resample('1min').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()

    return candles

def draw_chart(canvas_frame, symbol):
    for widget in canvas_frame.winfo_children():
        widget.destroy() 

    candles = prepare_candles(symbol)

    fig = mpf.figure(style='charles', figsize=(8, 5))
    ax_price = fig.add_subplot(2, 1, 1)
    ax_vol = fig.add_subplot(2, 1, 2, sharex=ax_price)

    mpf.plot(
        candles,
        type='candle',
        ax=ax_price,
        volume=ax_vol,
        show_nontrading=True
    )

    chart_widget = FigureCanvasTkAgg(fig, master=canvas_frame)
    chart_widget.draw()
    chart_widget.get_tk_widget().pack(fill=tk.BOTH, expand=1)


def create_dashboard():
    root = tk.Tk()
    root.title(" LBank Crypto Dashboard")
    root.geometry("950x650")
    root.configure(bg="#f0f2f5")


    title = ttk.Label(root, text="LBank Candlestick Dashboard", font=("Segoe UI", 18, "bold"))
    title.pack(pady=10)

    symbol_frame = ttk.Frame(root)
    symbol_frame.pack(pady=5)

    ttk.Label(symbol_frame, text="COIN:").pack(side=tk.LEFT, padx=5)
    selected_symbol = tk.StringVar(value="BTC/USDT")
    symbol_entry = ttk.Entry(symbol_frame, textvariable=selected_symbol, width=15)
    symbol_entry.pack(side=tk.LEFT)

    chart_frame = ttk.Frame(root)
    chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    draw_btn = ttk.Button(root, text="نمایش چارت", command=lambda: draw_chart(chart_frame, selected_symbol.get()))
    draw_btn.pack(pady=10)


    exit_btn = ttk.Button(root, text="خروج", command=root.quit)
    exit_btn.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_dashboard()
