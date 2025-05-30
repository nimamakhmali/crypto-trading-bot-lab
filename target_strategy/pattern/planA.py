import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = "lbank_1min_candles.csv"
Window = 5
def is_pivot_high(data, i, w):
    return all(data[i] > data[i-j] and data[i] > data[i+j] for j in range(1, w+1))

def is_pivot_low(data, i, w):
    return all(data[i] < data[i-j] and data[i] < data[i+j] for j in range(1, w+1))

df = pd.read_csv(file_path, parse_dates=['time'])
df.set_index('time', inplace=True)

df['wave_tag'] = 0
close = df['close'].values

pivot_points = []
for i in range(Window, len(df) - Window):
    if is_pivot_low(close, i, Window):
        pivot_points.append((i, 'low'))
    elif is_pivot_high(close, i, Window):
        pivot_points.append((i, 'high')) 

i = 0
while i < len(pivot_points) - 2:
    i1, t1 = pivot_points[i]
    i2, t2 = pivot_points[i+1]
    i3, t3 = pivot_points[i+2]

    p1, p2, p3 = close[i1], close[i2], close[i3]

    if t1 == 'low' and t2 == 'high' and t3 == 'low' and p3 > p1:
        df.iloc[i1, df.columns.get_loc('wave_tag')] = 1
        df.iloc[i2, df.columns.get_loc('wave_tag')] = 2
        df.iloc[i3, df.columns.get_loc('wave_tag')] = 3
        i += 2
    
    elif t1 == 'high' and t2 == 'low' and t3 == 'high' and p3 < p1:
  
        df.iloc[i1, df.columns.get_loc('wave_tag')] = 1
        df.iloc[i2, df.columns.get_loc('wave_tag')] = 2
        df.iloc[i3, df.columns.get_loc('wave_tag')] = 3
        i += 2  
    else:
        i += 1

df.to_csv("lbank_1min_candles.csv")
print("WaveTags accepted")


# Load data
df = pd.read_csv("lbank_1min_candles.csv", parse_dates=['time'])
df.set_index('time', inplace=True)

# فیلتر نقاط موج
p1 = df[df['wave_tag'] == 1]
p2 = df[df['wave_tag'] == 2]
p3 = df[df['wave_tag'] == 3]

# رسم قیمت
plt.figure(figsize=(15, 6))
plt.plot(df['close'], label='Close Price', color='gray', linewidth=1)

# رسم نقاط موج
plt.scatter(p1.index, p1['close'], color='blue', label='Wave 1 (Low)', marker='o', s=50)
plt.scatter(p2.index, p2['close'], color='orange', label='Wave 2 (High)', marker='^', s=50)
plt.scatter(p3.index, p3['close'], color='green', label='Wave 3 (Correction)', marker='v', s=50)

# خطوط اتصال بین موج‌ها (اختیاری)
for i in range(min(len(p1), len(p2), len(p3))):
    try:
        x_vals = [p1.index[i], p2.index[i], p3.index[i]]
        y_vals = [p1['close'].iloc[i], p2['close'].iloc[i], p3['close'].iloc[i]]
        plt.plot(x_vals, y_vals, color='purple', linestyle='--', linewidth=1)
    except:
        continue

# تنظیمات نهایی
plt.title("Wave 1-2-3 Pattern Detection")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
    