import asyncio
import websockets
import requests
import pandas as pd
import json
import os

CSV_FILE = "btc_usdt_1min.csv"

# گرفتن 1000 کندل از REST API
def fetch_initial_data():
    url = "https://api.lbkex.com/v2/kline.do"
    params = {
        "symbol": "btc_usdt",
        "size": 1000,
        "type": "1min"
    }
    response = requests.get(url, params=params)
    data = response.json()["data"]

    # مرتب‌سازی بر اساس زمان
    data.sort(key=lambda x: x[0])

    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "turnover"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')

    df.to_csv(CSV_FILE, index=False)
    print("✅ Initial 1000 candles saved to CSV.")


# دریافت کندل‌های لایو از WebSocket
async def listen_to_lbank():
    uri = "wss://www.lbkex.net/ws/V2/"
    async with websockets.connect(uri) as websocket:
        request_message = {
            "action": "subscribe",
            "subscribe": "kbar",
            "kbar": "1min",
            "pair": "btc_usdt"
        }

        await websocket.send(json.dumps(request_message))
        print("✅ Subscribed to live BTC/USDT kbar")

        while True:
            response = await websocket.recv()
            data = json.loads(response)

            if data.get("action") == "push" and "kbar" in data:
                k = data["kbar"]["data"]
                kline = {
                    "timestamp": pd.to_datetime(k["time"], unit='s'),
                    "open": float(k["open"]),
                    "high": float(k["high"]),
                    "low": float(k["low"]),
                    "close": float(k["close"]),
                    "volume": float(k["vol"]),
                    "turnover": float(k["turnover"])
                }

                print(f"🟢 New Candle: {kline['timestamp']} - Close: {kline['close']}")

                # ذخیره به CSV
                df = pd.DataFrame([kline])
                df.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False)


# اجرای همه چیز
if __name__ == "__main__":
    fetch_initial_data()
    asyncio.run(listen_to_lbank())
