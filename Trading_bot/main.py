from API.LBank_API import LBankAPI

def main():
    lbank = LBankAPI()

    print(" Getting account info...")
    account_info = lbank.get_account_info()
    print(account_info)

    print("\n Getting ticker for btc_usdt...")
    ticker = lbank.get_ticker("btc_usdt")
    print(ticker)

    # print("\n Placing order...")
    # order = lbank.place_order("btc_usdt", "buy", price=20000, amount=0.001)
    # print(order)

if __name__ == "__main__":
    main() 