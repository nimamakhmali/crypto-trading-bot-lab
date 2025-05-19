import pandas as pd
import mplfinance as mpf

# خواندن فایل CSV
df = pd.read_csv("lbank_kbars.csv")
df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)

# تبدیل به کندل 1 دقیقه‌ای
candles = df.resample('1T').agg({
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum'
}).dropna()

# افزودن ستون tag با مقدار پیش‌فرض 0
candles['tag'] = 0

# تگ 1 → اولین کندل
candles.iloc[0, candles.columns.get_loc('tag')] = 1

# انتخاب کندل‌ها بعد از کندل اول
remaining = candles.iloc[1:]

# پیدا کردن کف یا سقف بعد از اولین کندل
lowest_idx = remaining['low'].idxmin()
highest_idx = remaining['high'].idxmax()

lowest_val = remaining.loc[lowest_idx, 'low']
highest_val = remaining.loc[highest_idx, 'high']

# تصمیم: کدوم اول اتفاق افتاده؟ سقف یا کف؟
if lowest_idx < highest_idx:
    candles.loc[lowest_idx, 'tag'] = 2  # تگ 2 به کف
else:
    candles.loc[highest_idx, 'tag'] = 2  # تگ 2 به سقف

# ذخیره در فایل جدید
candles.to_csv("lbank_1min_candles.csv")
print(" Saved lbank_1min_candles.csv with tags")

# رسم نمودار
mpf.plot(candles, type='candle', volume=True, style='charles', title='LBank 1-Min Candles')
