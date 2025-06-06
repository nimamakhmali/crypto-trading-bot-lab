import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from trendline_Break_dataset import trendline_breakout_dataset
from walkforward import walkforward_model
from concurrent.futures import ThreadPoolExecutor
import os

plt.style.use('dark_background')

def prof_factor(rets):
    return rets[rets > 0].sum() / rets[rets < 0].abs().sum() if rets[rets < 0].abs().sum() != 0 else np.nan

def process_file(file_path):
    try:
        data = pd.read_csv(file_path)
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date')
        data = data.dropna()

        lookback = 72
        trades, data_x, data_y = trendline_breakout_dataset(data, lookback)
        trades = trades.dropna()

        train_size = 10000
        step_size = 5000
        signal, prob = walkforward_model(
            np.log(data['close']).to_numpy(),
            trades, data_x, data_y,
            train_size, step_size
        )

        data['sig'] = signal
        data['dumb_sig'] = prob
        data.loc[data['dumb_sig'] > 0, 'dumb_sig'] = 1
        data['r'] = np.log(data['close']).diff().shift(-1)

        all_r = trades['return']
        mod_r = trades[trades['model_prob'] > 0.5]['return']
        no_filter_rets = data['r'] * data['dumb_sig']
        filter_rets = data['r'] * data['sig']

        results = {
            "file": os.path.basename(file_path),
            "no_filter_rets": no_filter_rets,
            "filter_rets": filter_rets,
            "BuyHold": data['r'],
            "metrics": {
                "all_pf": prof_factor(no_filter_rets),
                "all_avg": all_r.mean(),
                "all_wr": len(all_r[all_r > 0]) / len(all_r),
                "all_time": len(data[data['dumb_sig'] > 0]) / len(data),
                "meta_pf": prof_factor(filter_rets),
                "meta_avg": mod_r.mean(),
                "meta_wr": len(mod_r[mod_r > 0]) / len(mod_r),
                "meta_time": len(data[data['sig'] > 0]) / len(data)
            }
        }
        return results

    except Exception as e:
        return {"file": file_path, "error": str(e)}

def main():
    csv_files = [f for f in os.listdir('.') if f.startswith('lbank_1min_candles') and f.endswith('.csv')]

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_file, csv_files))

    for res in results:
        print(f"\n===== {res['file']} =====")
        if "error" in res:
            print("Error:", res["error"])
            continue
        m = res["metrics"]
        print("All Trades PF:", m["all_pf"])
        print("All Trades Avg:", m["all_avg"])
        print("All Trades Win Rate:", m["all_wr"])
        print("All Trades Time In Market:", m["all_time"])
        print("Meta-Labeled PF:", m["meta_pf"])
        print("Meta-Labeled Avg:", m["meta_avg"])
        print("Meta-Labeled Win Rate:", m["meta_wr"])
        print("Meta-Labeled Time In Market:", m["meta_time"])

        res["filter_rets"].cumsum().plot(label=f'{res["file"]} Meta-Labeled')
        res["no_filter_rets"].cumsum().plot(label=f'{res["file"]} All Trades')
        res["BuyHold"].cumsum().plot(label=f'{res["file"]} Buy & Hold')

    plt.legend()
    plt.title("Cumulative Log Returns (All Files)")
    plt.ylabel("Return")
    plt.show()

if __name__ == "__main__":
    main()
