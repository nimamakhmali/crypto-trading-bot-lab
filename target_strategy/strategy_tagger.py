import pandas as pd

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
        