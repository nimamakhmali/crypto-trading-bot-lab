import tkinter as tk
from tkinter import ttk
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import tempfile
import webbrowser
import os

# --- مرحله 1: خواندن داده‌ها ---
df = pd.read_csv("lbank_kbars.csv")
df['time'] = pd.to_datetime(df['time'])

# --- مرحله 2: ساخت چارت کندل‌استیک ---
fig = go.Figure(data=[go.Candlestick(
    x=df['time'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
)])
fig.update_layout(
    title='BTC/USDT Candlestick Chart',
    xaxis_title='Time',
    yaxis_title='Price',
    xaxis_rangeslider_visible=False,
    template='plotly_dark'
)

# --- مرحله 3: ذخیره به صورت فایل HTML ---
temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
plot(fig, filename=temp_file.name, auto_open=False)

# --- مرحله 4: ساخت داشبورد با tkinter ---
root = tk.Tk()
root.title("📈 داشبورد شخصی کریپتو")
root.geometry("400x300")
root.configure(bg="#1e1e1e")

# عنوان
label = ttk.Label(root, text="BTC/USDT", font=("Helvetica", 20, "bold"))
label.pack(pady=20)

# اطلاعات خلاصه
latest = df.iloc[-1]
price_text = f"آخرین قیمت: {latest['close']}"

price_label = ttk.Label(root, text=price_text, font=("Helvetica", 14))
price_label.pack()

# دکمه نمایش چارت
def open_chart():
    webbrowser.open('file://' + os.path.realpath(temp_file.name))

btn = ttk.Button(root, text="📊 نمایش نمودار کندل", command=open_chart)
btn.pack(pady=30)

# اجرای پنجره
root.mainloop()
