import pandas as pd
import numpy as np

num_rows = 3000
start_price = 10000
start_time = pd.Timestamp('2025-06-05 00:00:00')

timestamps = pd.date_range(start=start_time, periods=num_rows, freq='T')

# افزایش نوسان قیمت با scale بالا
price_open = [start_price]
for _ in range(1, num_rows):
    change = np.random.normal(loc=0, scale=np.random.uniform(10, 50))  # نوسان بالا
    price_open.append(price_open[-1] + change)

price_open = np.array(price_open)

# high و low نوسانی‌تر
price_high = price_open + np.random.uniform(5, 30, size=num_rows)
price_low = price_open - np.random.uniform(5, 30, size=num_rows)
price_close = price_low + np.random.uniform(0, (price_high - price_low), size=num_rows)

# حجم نوسانی با اسپایک
volume_base = np.random.randint(100, 500, size=num_rows)
volume_spike_indices = np.random.choice(num_rows, size=num_rows // 20, replace=False)
volume_base[volume_spike_indices] *= np.random.randint(3, 10, size=len(volume_spike_indices))

df = pd.DataFrame({
    'time': timestamps,
    'open': np.round(price_open, 2),
    'high': np.round(price_high, 2),
    'low': np.round(price_low, 2),
    'close': np.round(price_close, 2),
    'volume': volume_base
})

df.to_csv('fake_market_data_volatile.csv', index=False)
print("✅ داده‌های پرنوسان در فایل fake_market_data_volatile.csv ذخیره شدند.")
