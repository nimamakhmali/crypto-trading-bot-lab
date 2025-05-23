import pandas as pd


def calculate_rsi(df, period: int = 14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rsi))
    return rsi

def add_rsi_to_csv(input_file: str = "lbank_1min_candles.csv", output_file: str = None):
    df = pd.read_csv(input_file, parse_dates=['time'])
    df['rsi'] = calculate_rsi(df)

    output_path = output_file if output_file else input_file
    df.to_csv(output_path, index=False)
    print(f"RSI added and saved to {output_path}")

#def plot_rsi():
#    apds

if __name__ == "__main__":
    add_rsi_to_csv()     