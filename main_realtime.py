import threading
import time
import subprocess

def run_websocket_data():
    subprocess.run(["python", "websockets_data.py"])

def run_candle_plot():
    while True:
        subprocess.run(["python", "change_to_1min.py"])
        time.sleep(60)  # هر ۶۰ ثانیه چارت جدید رو رسم کنه

if __name__ == "__main__":
    t1 = threading.Thread(target=run_websocket_data)
    t2 = threading.Thread(target=run_candle_plot)

    t1.start()
    time.sleep(2)
    t2.start()

    t1.join()
    t2.join()
