
from target_strategy.strategy_tagger import SimpleTagger
tagger = SimpleTagger("lbank_1min_candles.csv")
tagger.tag_initial_leg()
tagger.export()
              
              
'''
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
                '''
                              