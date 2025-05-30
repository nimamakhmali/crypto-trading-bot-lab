import pandas as pd
import numpy as np

# CSV
file_path = 'lbank_1min_candles.csv'

# read csv
df = pd.read_csv(file_path)


if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

# 
df['tag'] = 0

# Recieve price
data = df['close'].to_numpy()
order = 10

# High
def rw_top(data, curr_index, order):
    if curr_index < order * 2 + 1:
        return False
    k = curr_index - order
    v = data[k]
    for i in range(1, order + 1):
        if data[k + i] > v or data[k - i] > v:
            return False
    return True

# Low
def rw_bottom(data, curr_index, order):
    if curr_index < order * 2 + 1:
        return False
    k = curr_index - order
    v = data[k]
    for i in range(1, order + 1):
        if data[k + i] < v or data[k - i] < v:
            return False
    return True

# 
def rw_extremes(data, order):
    tops = []
    bottoms = []
    for i in range(len(data)):
        if rw_top(data, i, order):
            tops.append(i - order)
        if rw_bottom(data, i, order):
            bottoms.append(i - order)
    return tops, bottoms

tops, bottoms = rw_extremes(data, order)
extrema = sorted(tops + bottoms)

# 1 2 3 
for i in range(len(extrema) - 2):
    i1, i2, i3 = extrema[i], extrema[i+1], extrema[i+2]
    p1, p2, p3 = data[i1], data[i2], data[i3]

    # Higher Higher 
    if i1 in bottoms and i2 in tops and i3 in bottoms and p3 > p1:
        df.iloc[i1, df.columns.get_loc('tag')] = 1
        df.iloc[i2, df.columns.get_loc('tag')] = 2
        df.iloc[i3, df.columns.get_loc('tag')] = 3

    # Lower Lower
    elif i1 in tops and i2 in bottoms and i3 in tops and p3 < p1:
        df.iloc[i1, df.columns.get_loc('tag')] = 1
        df.iloc[i2, df.columns.get_loc('tag')] = 2
        df.iloc[i3, df.columns.get_loc('tag')] = 3

#  Niga
df.to_csv(file_path)
print("tags saved")
