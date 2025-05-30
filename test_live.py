import asyncio
import websockets
import ssl
import json
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from datetime import datetime
from collections import deque
from matplotlib.animation import FuncAnimation

uri = "wss://www.lbkex.net/ws/V2/"
ssl_context = ssl._create_unverified_context()
live_data = deque(maxlen=5000)  # داده‌های زنده در حافظه

# این تابع هر کندل رو در حافظه ذخیره می‌کنه
def process_kbar(kbar):
    time_value = kbar["t"]
    utc_time = datetime.utcfromtimestamp(int(time_value) / 1000)
    live_data.append({
        'time': utc_time,
        'open': float(kbar["o"]),
        'high': float(kbar["h"]),
        'low': float(kbar["l"]),
        'close': float(kbar["c"]),
        'volume': float(kbar["v"]),
    })

# گرفتن داده از WebSocket
async def kbar_handler():
    async with websockets.connect(uri, ssl=ssl_context) as ws:
        await ws.send(json.dumps({
            "action": "subscribe",
            "subscribe": "kbar",
            "kbar": "1min",
            "pair": "btc_usdt"
        }))
        while True:
            message = await ws.recv()
            data = json.loads(message)
            if data.get("type") == "kbar":
                process_kbar(data["kbar"])

# تابعی برای آپدیت نمودار
def update_chart(frame):
    if len(live_data) < 3:
        return
    df = pd.DataFrame(list(live_data))
    df.set_index("time", inplace=True)
    df = df.resample("1T").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum"
    }).dropna()
    
    ax.clear()
    mpf.plot(df, type='candle', volume=True, ax=ax, style='charles')

# شروع رسم با انیمیشن
fig, ax = plt.subplots()
ani = FuncAnimation(fig, update_chart, interval=5000)  # هر ۵ ثانیه آپدیت

# اجرای همزمان WebSocket و نمودار
async def main():
    task = asyncio.create_task(kbar_handler())
    plt.show()
    await task

if __name__ == "__main__":
    asyncio.run(main())
