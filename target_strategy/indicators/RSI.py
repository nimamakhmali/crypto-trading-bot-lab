import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import os

def calculate_rsi(df, period: int = 14):
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def process_data(input_file="lbank_1min_candles.csv", output_file=None):
    # Load data
    df = pd.read_csv(input_file, parse_dates=['time'], index_col='time')
    df.sort_index(inplace=True)

    # Calculate RSI
    df['RSI'] = calculate_rsi(df)
    df.dropna(inplace=True)

    # Save updated CSV
    output_path = output_file if output_file else input_file
    df.to_csv(output_path)
    print(f" RSI added and saved to: {output_path}")

    return df

def plot_chart_with_rsi(df):
    apds = [
        mpf.make_addplot(df['RSI'], panel=1, color='purple', width=1.0, ylabel='RSI')
    ]

    fig, axes = mpf.plot(
        df,
        type='candle',
        style='yahoo',
        volume=True,
        addplot=apds,
        panel_ratios=(3, 1),
        figratio=(16, 8),
        figscale=1.2,
        title='Candlestick Chart with RSI (Styled like Divergence)',
        returnfig=True
    )

    # Add overbought/oversold lines to RSI panel
    rsi_ax = axes[2]
    rsi_ax.axhline(y=70, color='red', linestyle='--', linewidth=1, label='Overbought (70)')
    rsi_ax.axhline(y=30, color='green', linestyle='--', linewidth=1, label='Oversold (30)')
    rsi_ax.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = process_data()
    plot_chart_with_rsi(df)
