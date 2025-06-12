import pandas as pd
import pandas_ta as ta
import numpy as np
import plotly.graph_objects as go
from backtesting import Strategy, Backtest


def preprocess(df):
    df = df[df['volume'] != 0]
    df.reset_index(drop=True, inplace=True)
    df['RSI'] = ta.rsi(df['close'], length=12)
    df['EMA'] = ta.ema(df['close'], length=150)
    df = df[:2000]

    EMAsignal = [0] * len(df)
    backcandles = 15
    for row in range(backcandles, len(df)):
        upt, dnt = 1, 1
        for i in range(row - backcandles, row + 1):
            if max(df['open'][i], df['close'][i]) >= df['EMA'][i]:
                dnt = 0
            if min(df['open'][i], df['close'][i]) <= df['EMA'][i]:
                upt = 0
        if upt and dnt:
            EMAsignal[row] = 3
        elif upt:
            EMAsignal[row] = 2
        elif dnt:
            EMAsignal[row] = 1

    df['EMAsignal'] = EMAsignal
    return df


def generate_signal(df, l, backcandles, gap, zone_threshold, price_diff_threshold):
    max_price = df.high[l - backcandles:l - gap].max()
    min_price = df.low[l - backcandles:l - gap].min()
    index_max = df.high[l - backcandles:l - gap].idxmax()
    index_min = df.low[l - backcandles:l - gap].idxmin()
    price_diff = max_price - min_price

    if df.EMAsignal[l] == 2 and index_min < index_max and price_diff > price_diff_threshold:
        l1 = max_price - 0.62 * price_diff
        l2 = max_price - 0.78 * price_diff
        l3 = max_price
        if abs(df.close[l] - l1) < zone_threshold and df.high[l - gap:l].min() > l1:
            return 2, l2, l3, index_min, index_max
    elif df.EMAsignal[l] == 1 and index_min > index_max and price_diff > price_diff_threshold:
        l1 = min_price + 0.62 * price_diff
        l2 = min_price + 0.78 * price_diff
        l3 = min_price
        if abs(df.close[l] - l1) < zone_threshold and df.low[l - gap:l].max() < l1:
            return 1, l2, l3, index_min, index_max
            
    return 0, 0, 0, 0, 0


def apply_signals(df):
    gap_candle = 5
    backcandles = 40
    signal, TP, SL, MinSwing, MaxSwing = [], [], [], [], []

    for row in range(backcandles, len(df)):
        sig, sl, tp, min_sw, max_sw = generate_signal(
            df, row, backcandles, gap_candle, 0.001, 0.01)
        signal.append(sig)
        SL.append(sl)
        TP.append(tp)
        MinSwing.append(min_sw)
        MaxSwing.append(max_sw)

    # پر کردن ابتدای دیتا با مقدار صفر
    pad = [0] * backcandles
    df['signal'] = pad + signal
    df['SL'] = pad + SL
    df['TP'] = pad + TP
    df['MinSwing'] = pad + MinSwing
    df['MaxSwing'] = pad + MaxSwing

    return df


def SIGNAL():
    return df.signal.values


class MyStrat(Strategy):
    mysize = 0.99

    def init(self):
        self.signal1 = self.I(SIGNAL)

    def next(self):
        sig = self.signal1[-1]
        if sig == 2 and not self.trades:
            sl1 = self.data.SL[-1]
            tp1 = self.data.TP[-1]
            tp2 = tp1 - (tp1 - self.data.Close[-1]) / 2
            self.buy(sl=sl1, tp=tp1, size=self.mysize)
            self.buy(sl=sl1, tp=tp2, size=self.mysize)
        elif sig == 1 and not self.trades:
            sl1 = self.data.SL[-1]
            tp1 = self.data.TP[-1]
            tp2 = tp1 + (self.data.Close[-1] - tp1) / 2
            self.sell(sl=sl1, tp=tp1, size=self.mysize)
            self.sell(sl=sl1, tp=tp2, size=self.mysize)


def main():
    global df
    df = pd.read_csv("lbank_1min_candles.csv")
    df = preprocess(df)
    df = apply_signals(df)

    df.rename(columns={"open": "Open", "high": "High", "low": "Low",
                       "close": "Close", "volume": "Volume"}, inplace=True)

    bt = Backtest(df, MyStrat, cash=1000, margin=1/100, commission=0.000)
    stats = bt.run()
    print(stats)
    bt.plot()
    

if __name__ == "__main__":
    main()
