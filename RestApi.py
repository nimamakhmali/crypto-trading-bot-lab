import requests
import csv
from datetime import datetime, timezone

def fetch_initial_candles(
    output_file="lbank_1min_candles.csv",
    symbol="btc_usdt",
    type_="minute1",
    size=30
):
    url = f"https://api.lbkex.com/v2/kline.do?symbol={symbol}&type={type_}&size={size}"
    response = requests.get(url)
    json_data = response.json()

    if "data" not in json_data:
        print("Unexpected format:", json_data)
        return

    candle_data = json_data["data"]
    candle_data = sorted(candle_data, key=lambda x: x[0])

    seen = set()
    unique_candles = []
    for c in candle_data:
        if c[0] not in seen:
            unique_candles.append(c)
            seen.add(c[0])

    unique_candles = unique_candles[-30:]

    header = ["time", "open", "high", "low", "close", "volume"]
    with open(output_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for c in unique_candles:
            utc_time = datetime.fromtimestamp(c[0], tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([utc_time, c[1], c[2], c[3], c[4], c[5]])

    print(f"Saved {len(unique_candles)} candles to {output_file}")

if __name__ == "__main__":
    fetch_initial_candles()