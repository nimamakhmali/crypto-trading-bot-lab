import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

def calculate_rsi(df, period: int = 14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def add_rsi_to_csv(input_file: str = "lbank_1min_candles.csv", output_file: str = None):
    df = pd.read_csv(input_file, parse_dates=['time'], index_col='time')
    df['rsi'] = calculate_rsi(df)

    output_path = output_file if output_file else input_file
    df.to_csv(output_path)
    print(f" RSI added and saved to {output_path}")
    
    return df 

def plot_rsi(df):
    apds = [
        mpf.make_addplot(df['rsi'], panel=1, color='purple', ylabel='RSI')
    ]

    mpf.plot(df, type='candle', volume=True, style='charles',
             addplot=apds, title='Candlestick + RSI',
             panel_ratios=(3, 1))

if __name__ == "__main__":
    df = add_rsi_to_csv()
    plot_rsi(df)
