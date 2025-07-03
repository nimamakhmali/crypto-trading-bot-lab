import csv
from datetime import datetime
import os


DATA_DIR = "Data"
LOG_PATH = os.path.join(DATA_DIR, "signals_log.csv")

def log_signal(event_type, trade, pnl=None):
    log_exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline='') as f:
        writer = csv.writer(f)
        if not log_exists:
            writer.writerow([
                "datetime", "event", "entry_time", "entry_price", "target_price",
                "stop_price", "direction", "exit_price", "pnl"
            ])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            event_type,
            trade.get('entry_time'),
            trade.get('entry_price'),
            trade.get('target_price'),
            trade.get('stop_price'),
            trade.get('direction'),
            trade.get('exit_price', ''),
            pnl if pnl is not None else ''
        ])