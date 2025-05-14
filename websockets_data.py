import asyncio
import websockets
import json
import csv
import os
from datetime import datetime

uri = "wss://www.lbkex.net/ws/V2/"
file_path = "lbank_kbars.csv"
header = ["time", "open", "high", "low", "close", "volume", "amount", "trades"]


if not os.path.exists(file_path):
    with open(file_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)

def save_kbar_to_csv(kbar):
    try:
        time_value = kbar["t"]
        if isinstance(time_value, int) or time_value.isdigit():
            utc_time = datetime.utcfromtimestamp(int(time_value) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        else:
            utc_time = datetime.strptime(time_value, "%Y-%m-%dT%H:%M:%S.%f").strftime('%Y-%m-%d %H:%M:%S')
        
        with open(file_path, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                utc_time, kbar["o"], kbar["h"], kbar["l"],
                kbar["c"], kbar["v"], kbar["a"], kbar["n"]
            ])
        print(f" Saved 1min candle at {utc_time}")
    except Exception as e:
        print(f" Error saving kbar to CSV: {e}")


async def kbar_handler():
    while True:
        try:
            async with websockets.connect(uri, ping_interval=None) as ws:
                subscribe_msg = {
                    "action": "subscribe",
                    "subscribe": "kbar",
                    "kbar": "1min",
                    "pair": "btc_usdt",
                }
                await ws.send(json.dumps(subscribe_msg))
                print(" Subscribed to 1min KBAR")

                while True:
                    message = await ws.recv()
                    data = json.loads(message)
                    if data.get("type") == "kbar":
                        kbar = data["kbar"]
                        save_kbar_to_csv(kbar)
        except Exception as e:
            print(f" Error in kbar_handler: {e}")
            await asyncio.sleep(5)


async def live_ticker():
    while True:
        try:
            async with websockets.connect(uri, ping_interval=None) as ws:
                subscribe_msg = {
                    "action": "subscribe",
                    "subscribe": "ticker",
                    "pair": "btc_usdt",
                }
                await ws.send(json.dumps(subscribe_msg))
                print(" Subscribed to Ticker (Live Data)")

                while True:
                    message = await ws.recv()
                    data = json.loads(message)
                    if data.get("type") == "ticker":
                        tick = data["ticker"]
                        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"[{now} UTC] Price: {tick['latest']}")
        except Exception as e:
            print(f" Error in live_ticker: {e}")
            await asyncio.sleep(1)


async def main():
    await asyncio.gather(kbar_handler(), live_ticker())

if __name__ == "__main__":
    asyncio.run(main())
