import threading
import time
import subprocess
import target_strategy.indicators 
import target_strategy.pattern

def run_websocket_data():
    subprocess.run(["python", "websockets_data.py"])

def run_analysis_pipeline():
    while True:
        try:
            print(" Updating CSV file with new analysis...")

            # ساخت کندل 1 دقیقه‌ای
            subprocess.run(["python", "change_to_1min.py"])

            # محاسبه SMA
            subprocess.run(["python", "target_strategy/indicators/Sma.py"])

            # محاسبه RSI
            subprocess.run(["python", "target_strategy/indicators/RSI.py"])

            # برچسب‌گذاری 1-2-3
            subprocess.run(["python", "1_2_3_points.py"])
            
            subprocess.run(["python", "target_strategy/pattern/strategy_tagger.py"])

            print(" All analysis steps completed.\n")

        except Exception as e:
            print(f" Error during analysis: {e}")
        
        time.sleep(60)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_websocket_data)
    t2 = threading.Thread(target=run_analysis_pipeline)

    t1.start()
    time.sleep(2)  # فرصت اتصال WebSocket
    t2.start()

    t1.join()
    t2.join()
