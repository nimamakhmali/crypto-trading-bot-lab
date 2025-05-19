import multiprocessing
import subprocess
import time

def run_websockets_data():
    subprocess.run(["python", "websockets_data.py"])
    
def run_candle_updater():
    while True:
        subprocess.run(["python", "change_to_1min.py"])
        time.sleep(5)

if __name__ == "main":
    
    p1 = multiprocessing.Process(target=run_websockets_data)
    p2 = multiprocessing.Process(target=run_candle_updater)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
                