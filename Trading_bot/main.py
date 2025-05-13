# main.py

from webSocket.LBank_WS_Client import LBankWebSocketClient
import time

if __name__ == "__main__":
    ws_client = LBankWebSocketClient(symbol="btc_usdt", csv_file="btc_usdt_data.csv")
    ws_client.connect()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(" Stopping...")
        ws_client.disconnect()
