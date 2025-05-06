from API.LBank_API import LBankAPI

class TradingBot:
    def __init__(self):
        self.api = LBankAPI()
     
    def show_balance(self):
        info = self.api.get_account_info()
        print("ACCOUNT INFO:", info)
        
    def print_ticker(self, symbol: str):
        ticker = self.api.get_ticker(symbol)
        print(f"Ticker for {symbol}:", ticker)       