'''import pandas as pd

class SimpleTagger:
    def __init__(self, candle_file: str):
        self.candle_file = candle_file
        self.df = pd.read_csv(candle_file, index_col=0, parse_dates=True)
        self._prepare_data()
        
    def _prepare_data(self):
        if 'tag' not in self.df.columns:
            self.df['tag'] = 0 
    
    def tag_initial_leg(self):
        if len(self.df) < 3:
            print("Not enough data.")
            return

        self.df.iloc[0, self.df.columns.get_loc('tag')] = 1  # Tag 1 → اولین کندل

        lowest_idx = self.df.index[0]
        lowest_low = self.df.iloc[0]['low']

        # از کندل دوم شروع کن، روند رو دنبال کن
        trend_started = False
        for i in range(1, len(self.df)):
            curr_close = self.df.iloc[i]['close']
            prev_close = self.df.iloc[i - 1]['close']

            if curr_close < prev_close:
                trend_started = True  # روند نزولی شروع شد
                if self.df.iloc[i]['low'] < lowest_low:
                    lowest_low = self.df.iloc[i]['low']
                    lowest_idx = self.df.index[i]
            elif trend_started:
                # اولین نشونه برگشت روند → پایان لگ نزولی
                break

        if trend_started:
            self.df.loc[lowest_idx, 'tag'] = 2
            print(f"Downtrend identified. Candle with bottom {lowest_low} --> tag=2")

        else:
            print(" No clear downward trend was identified.")

    def export(self, out_file: str = None):
        out_path = out_file if out_file else self.candle_file
        self.df.to_csv(out_path)
        print(f"Tagged data saved to {out_path}") 
    
    def get_dataFrame(self):
        return self.df                      
'''        
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

THRESHOLD = 0.01

df = pd.read_csv("lbank_1min_candles.csv", parse_dates=['time'], index_col='time')

pivots = []
last_pivot_price = df.iloc[0]['close']
last_pivot_index = df.index[0]
direction = None  # up - down
tags = [1]

for i in range(1, len(df)):
    current_price = df.iloc[i]['close']
    current_index = df.index[i]
    price_change = (current_price - last_pivot_price) / last_pivot_price

    if direction is None:
        if abs(price_change) >= THRESHOLD:
            direction = 'up' if price_change > 0 else 'down'
            pivots.append((last_pivot_index, last_pivot_price))

            last_pivot_price = current_price
            last_pivot_index = current_index
            tags.append(2)
        else:
            tags.append(0)
    elif direction == 'up':
        if  current_price > last_pivot_price:
            last_pivot_price = current_price
            last_pivot_index = current_index
            tags.append(0)
        elif(last_pivot_price - current_price) / last_pivot_price >= THRESHOLD:
            pivots.append((last_pivot_index, last_pivot_price))
            direction = 'down'
            last_pivot_price = current_price
            last_pivot_index = current_index    
            tags.append(2)
        else:
            tags.append(0)

df['tag'] = tags

df.to_csv("lbank_1min_candles.csv")

zz_lines = [(pivots[i][0], pivots[i+1][0]) for i in range(len(pivots)-1)]
zz_prices = [(pivots[i][1], pivots[i+1][1]) for i in range(len(pivots)-1)]

ap_lines = []
for(start, end), (p1, p2) in zip(zz_lines, zz_prices):
    ap_lines.append(mpf.make_addplot(
        [p1, p2],
        panel = 0,
        secondry_y = False,
        type = 'line',
        linestyle= 'dashed',
        linewidth = 1.5,
        color = 'red',
        yvalues = [p1, p2],
        x = [start, end]
    ))

mpf.plot(df, type='candle', volume=True, style='charles',
         title='LBank 1-Min Candles with ZigZag',
         addplot=ap_lines)    


