import numpy as np
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
from trendline_automation import fit_trendlines_single
import mplfinance as mpf


def trendline_breakout_dataset(
        ohlcv: pd.DataFrame, lookback: int,
        hold_period: int = 12, tp_mult: float = 3.0, sl_mult: float = 3.0,
        atr_lookback: int = 168
):
    ohlcv = ohlcv.dropna(subset=['high', 'low', 'close', 'volume'])

    min_rows = atr_lookback + lookback + hold_period
    if len(ohlcv) < min_rows:
        raise ValueError(f"Not enough rows: need at least {min_rows}, but got {len(ohlcv)}")

    close = np.log(ohlcv['close'].to_numpy())

    atr = ta.atr(np.log(ohlcv['high']), np.log(ohlcv['low']), np.log(ohlcv['close']), atr_lookback)
    if atr is None or atr.isna().all():
        raise ValueError("ATR calculation failed.")
    atr_arr = atr.bfill().to_numpy()  # ← اصلاح هشدار


    vol_arr = (ohlcv['volume'] / ohlcv['volume'].rolling(atr_lookback).median()).fillna(1.0).to_numpy()

    adx = ta.adx(ohlcv['high'], ohlcv['low'], ohlcv['close'], lookback)
    adx_col = f"ADX_{lookback}"
    if adx is None or adx_col not in adx:
        raise ValueError("ADX calculation failed.")
    adx_arr = adx[adx_col].fillna(0).to_numpy()

    trades = pd.DataFrame()
    trade_i = 0
    in_trade = False
    tp_price = None
    sl_price = None
    hp_i = None

    for i in range(atr_lookback, len(ohlcv)):
        window = close[i - lookback:i]
        s_coefs, r_coefs = fit_trendlines_single(window)
        r_val = r_coefs[1] + lookback * r_coefs[0]

        if not in_trade and close[i] > r_val:
            tp_price = close[i] + atr_arr[i] * tp_mult
            sl_price = close[i] - atr_arr[i] * sl_mult
            hp_i = i + hold_period
            in_trade = True

            trades.loc[trade_i, 'entry_i'] = i
            trades.loc[trade_i, 'entry_p'] = close[i]
            trades.loc[trade_i, 'atr'] = atr_arr[i]
            trades.loc[trade_i, 'sl'] = sl_price
            trades.loc[trade_i, 'tp'] = tp_price
            trades.loc[trade_i, 'hp_i'] = hp_i
            trades.loc[trade_i, 'slope'] = r_coefs[0]
            trades.loc[trade_i, 'intercept'] = r_coefs[1]
            trades.loc[trade_i, 'resist_s'] = r_coefs[0] / atr_arr[i]

            line_vals = (r_coefs[1] + np.arange(lookback) * r_coefs[0])
            err = np.sum(line_vals - window) / lookback / atr_arr[i]
            trades.loc[trade_i, 'tl_err'] = err
            trades.loc[trade_i, 'max_dist'] = (line_vals - window).max() / atr_arr[i]
            trades.loc[trade_i, 'vol'] = vol_arr[i]
            trades.loc[trade_i, 'adx'] = adx_arr[i]

        if in_trade:
            if close[i] >= tp_price or close[i] <= sl_price or i >= hp_i:
                trades.loc[trade_i, 'exit_i'] = i
                trades.loc[trade_i, 'exit_p'] = close[i]
                in_trade = False
                trade_i += 1

    trades = trades.dropna()
    trades['return'] = trades['exit_p'] - trades['entry_p']
    data_x = trades[['resist_s', 'tl_err', 'vol', 'max_dist', 'adx']]
    data_y = pd.Series(0, index=trades.index)
    data_y.loc[trades['return'] > 0] = 1

    return trades, data_x, data_y


if __name__ == '__main__':
    data = pd.read_csv('lbank_1min_candles.csv')
    print("Dataset loaded. Total rows:", len(data))

    time_col = 'time' if 'time' in data.columns else 'date'
    data[time_col] = pd.to_datetime(data[time_col])
    data = data.set_index(time_col)
    data = data.dropna()

    LOOKBACK = 48
    HOLD_PERIOD = 6
    ATR_LOOKBACK = 96

    try:
        trades, data_x, data_y = trendline_breakout_dataset(
            data, lookback=LOOKBACK,
            hold_period=HOLD_PERIOD,
            atr_lookback=ATR_LOOKBACK
        )
    except ValueError as e:
        print("Error:", e)
        exit()

    signal = np.zeros(len(data))
    for i in range(len(trades)):
        trade = trades.iloc[i]
        signal[int(trade['entry_i']):int(trade['exit_i'])] = 1.0

    data['r'] = np.log(data['close']).diff().shift(-1)
    data['sig'] = signal
    returns = data['r'] * data['sig']

    print("Profit Factor:", returns[returns > 0].sum() / returns[returns < 0].abs().sum())
    print("Win Rate:", len(trades[trades['return'] > 0]) / len(trades))
    print("Average Trade:", trades['return'].mean())

    returns.cumsum().plot()
    plt.title("Trendline Breakout Backtest")
    plt.ylabel("Cumulative Log Return")
    plt.xlabel("Time")
    plt.show()
