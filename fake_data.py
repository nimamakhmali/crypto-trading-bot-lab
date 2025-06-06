import pandas as pd
import numpy as np

num_rows = 3000
start_price = 10000
start_time = pd.Timestamp('2025-06-05 00:00:00')

timestamps = pd.date_range(start=start_time, periods=num_rows, freq='T')

price_open = [start_price]
for _ in range(1, num_rows):
    change = np.random.normal(loc=0, scale=5)
    price_open.append(price_open[-1] + change)

price_open = np.array(price_open)

price_high = price_open + np.random.uniform(0, 10, size=num_rows)
price_low = price_open - np.random.uniform(0, 10, size=num_rows)
price_close = price_low + np.random.uniform(0, (price_high - price_low), size=num_rows)
volume = np.random.randint(50, 300, size=num_rows)

df = pd.DataFrame({
    'time': timestamps,
    'open': np.round(price_open, 2),
    'high': np.round(price_high, 2),
    'low': np.round(price_low, 2),
    'close': np.round(price_close, 2),
    'volume': volume
})

df.to_csv('fake_market_data.csv', index=False)
print("داده‌ها در فایل fake_market_data.csv ذخیره شدند.")
