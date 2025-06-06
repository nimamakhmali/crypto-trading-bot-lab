import requests
import csv
from datetime import datetime, timezone
import time

# -----------------------
# تنظیمات
symbol = "btc_usdt"
type_ = "minute1"
size = 1000
timestamp = int(time.time())

# -----------------------
# ساخت URL
url = f"https://api.lbkex.com/v2/kline.do?symbol={symbol}&type={type_}&size={size}&time={1500}"

# -----------------------
# گرفتن داده
response = requests.get(url, verify=True)
json_data = response.json()

# -----------------------
# بررسی نتیجه
if "data" not in json_data:
    print(" Unexpected format:", json_data)
    exit()

candle_data = json_data["data"]

# -----------------------
# ذخیره در CSV
file_name = "lbank_1min_candles.csv"
header = ["time", "open", "high", "low", "close", "volume"]

with open(file_name, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for c in candle_data:
        # 👇 نسخه اصلاح‌شده
        utc_time = datetime.fromtimestamp(c[0], tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([utc_time, c[1], c[2], c[3], c[4], c[5]])

print(f" Saved {len(candle_data)} candles to {file_name}")
