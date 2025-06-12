import pandas as pd
import pandas_ta as ta

df = pd.read_csv("lbank_1min_candles.csv")
df = df[df['volume'] != 0]
df.reset_index(drop=True, inplace=True)
df.isna().sum()
df['RSI'] = ta.rsi(df.close, length=12)
df['EMA'] = ta.ema(df.close, length=150)
df.tail()

df = df[0:2000]

EMAsignal = [0]*len(df)
backcandles = 15
for row in range(backcandles, len(df)):
    upt = 1
    dnt = 1
    for i in range(row-backcandles, row+1):
        if max(df.open[i], df.close[i]) >= df.EMA[i]:
            dnt = 0
        if min(df.open[i], df.close[i]) <= df.EMA[i]:
            upt = 0
    if upt == 1 and dnt == 1:
        EMAsignal[row] = 3
    elif upt == 1:
        EMAsignal[row] = 2
    elif dnt == 1:
        EMAsignal[row] = 1

df['EMAsignal'] = EMAsignal

def generate_signal(df, l, backcandles, gap, zone_threshold, price_diff_threshold):
    max_price = df.high[l-backcandles:l-gap].max()
    min_price = df.low[l-backcandles:l-gap].min()
    index_max = df.high[l-backcandles:l-gap].idxmax()
    index_min = df.low[l-backcandles:l-gap].idxmin()
    price_diff = max_price - min_price

    if (df.EMAsignal[l] == 2
        and (index_min < index_max)
        and price_diff > price_diff_threshold):
        l1 = max_price - 0.62 * price_diff
        l2 = max_price - 0.78 * price_diff
        l3 = max_price - 0.   * price_diff
        if abs(df.close[l]-l1) < zone_threshold and df.high[l-gap:l].min() > l1:
            return (2, l2, l3, index_min, index_max)
        else:
            return (0, 0, 0, 0, 0)
        
    elif(df.EMAsignal[l] == 1
         and (index_min > index_max)
         and price_diff > price_diff_threshold):
        l1 = min_price + 0.62 * price_diff # position entry 0.62
        l2 = min_price + 0.78 * price_diff # SL 0.78
        l3 = min_price + 0. * price_diff # TP
        if abs(df.close[l]-l1) < zone_threshold and df.low[l-gap:l].max()<l1:
            return (1, l2, l3, index_min, index_max)
        else:
            return (0,0,0,0,0)
    
    else:
        return (0,0,0,0,0)   
    
    gap_candle = 5
    backcandles = 40
    signal = [0 for i in range(len(df))]
    TP = [0 for i in range(len(df))]
    SL = [0 for i in range(len(df))]
    MinSwing = [0 for i in range(len(df))]
    MaxSwing = [0 for i in range(len(df))]

    for row in range(backcandles, len(df)):
       # gen_sig = generate_signal(df, row, )