import asyncio
import websockets
import json
import csv
import os

uri = "wss://www.lbkex.net/ws/V2/"
file_path = "lbank_kbars.csv"
header = ["time", "open", "high", "low", "close", "volume", "amount", "trades"]

if not os.path.exists(file_path):
    with open(file_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)

def save_kbar_to_csv(kbar):
    with open(file_path, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            kbar["t"], kbar["o"], kbar["h"], kbar["l"],
            kbar["c"], kbar["v"], kbar["a"], kbar["n"]
        ])

async def listen_to_lbank():
    async with websockets.connect(uri, ping_interval=None) as websocket:
        #  پیام صحیح subscribe برای دریافت kbar
        subscribe_message = {
            "action": "subscribe",
            "subscribe":"kbar",
            "kbar":"1min", 
            "pair": "btc_usdt",
        }

        await websocket.send(json.dumps(subscribe_message))
        print(" Subscription request sent!")

        while True:
            message = await websocket.recv()
            print(" Received message:", message)

            try:
                data = json.loads(message)
                if data.get("type") == "kbar":
                    kbar = data["kbar"]
                    save_kbar_to_csv(kbar)
            except Exception as e:
                print(" Error parsing message:", e)

if __name__ == "__main__":
    asyncio.run(listen_to_lbank())
