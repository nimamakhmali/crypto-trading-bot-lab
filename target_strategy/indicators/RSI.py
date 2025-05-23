import pandas as pd
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
    rsi_colors = []
    for r in df['rsi']:
        if r >= 70:
            rsi_colors.append('red')
        elif r <= 30:
            rsi_colors.append('green')
        else:
            rsi_colors.append('purple')

    # RSI Panelllll     Siuuuuuu
    apds = [
        mpf.make_addplot(df['rsi'], panel=1, color=rsi_colors, width=1, ylabel='RSI')
    ]

    mpf.plot(df, type='candle', volume=True, style='charles',
             addplot=apds, title='Candlestick + RSI (Colored)',
             panel_ratios=(3,1), figratio=(12,6))

if __name__ == "__main__":
    df = add_rsi_to_csv()
    plot_rsi(df)
