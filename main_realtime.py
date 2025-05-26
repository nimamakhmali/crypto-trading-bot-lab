import threading
import time
import subprocess

def run_websocket_data():
    subprocess.run(["python", "websockets_data.py"])

def run_candle_plot():
    subprocess.run(["python", "change_to_1min.py"])

if __name__ == "__main__":
    # ایجاد ترد برای دریافت داده‌های لایو
    t1 = threading.Thread(target=run_websocket_data)
    # ایجاد ترد برای تبدیل به کندل و رسم
    t2 = threading.Thread(target=run_candle_plot)

    t1.start()
    time.sleep(2)  # تاخیر جزئی برای اینکه اول داده بیاد بعد نمودار رسم بشه
    t2.start()

    t1.join()
    t2.join()
