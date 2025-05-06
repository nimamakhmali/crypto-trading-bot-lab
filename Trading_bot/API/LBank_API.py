import os
import time
import hashlib
import hmac
import requests
from dotenv import load_dotenv
from API.interface_exchange_api import IExchangeAPI

load_dotenv()

class LBankAPI(IExchangeAPI):
    BASE_URL = "https://api.lbkex.com"

    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")

    def _sign(self, params: dict) -> dict:

        params['api_key'] = self.api_key
        sorted_params = sorted(params.items())
        sign_str = '&'.join([f"{k}={v}" for k, v in sorted_params])
        sign_str += f"&secret_key={self.api_secret}"
        sign = hashlib.md5(sign_str.encode()).hexdigest().upper()
        params['sign'] = sign
        return params

    def get_account_info(self):
        url = f"{self.BASE_URL}/v1/user_info.do"
        data = self._sign({})
        response = requests.post(url, data=data)
        return response.json()

    def get_ticker(self, symbol: str):
        url = f"{self.BASE_URL}/v1/ticker.do"
        params = {'symbol': symbol}
        response = requests.get(url, params=params)
        return response.json()

    def place_order(self, symbol: str, type_: str, price: float, amount: float):
        url = f"{self.BASE_URL}/v1/create_order.do"
        data = {
            'symbol': symbol,
            'type': type_,
            'price': price,
            'amount': amount
        }
        data = self._sign(data)
        response = requests.post(url, data=data)
        return response.json()

    def cancel_order(self, order_id: str, symbol: str):
        url = f"{self.BASE_URL}/v1/cancel_order.do"
        data = {
            'symbol': symbol,
            'order_id': order_id
        }
        data = self._sign(data)
        response = requests.post(url, data=data)
        return response.json()
