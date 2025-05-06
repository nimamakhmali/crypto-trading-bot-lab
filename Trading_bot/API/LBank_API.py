import time
import hmac
import hashlib
import requests
from config.settings import get_api_key, get_api_secret
from API.interface_exchange_api import IEXchangeAPI

class LBankAPI(IEXchangeAPI):
    BASE_URL = "https://api.lbank.info"
    
    def __init__(self):
        self.api_key = get_api_key()
        self.api_secret = get_api_secret()
    
    def _sgn_params(self, params):
        sorted_params = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
        return hmac.new(self.api_secret.encode(), sorted_params.encode(), hashlib.md5).hexdigest()

    def _post(self, endpoint, params):
        params["sign"] = self._sgn_params(params)
        response = requests.post(self.BASE_URL + endpoint, data=params)
        return response.json()
    
    def get_account_info(self):
        params = {
            "api_key": self.api_key,
            "req_time": int(time.time() * 1000),
        }
        return self._post("/v1/user_info.do", params)
    
    def get_ticker(self, symbol: str):
        response = requests.get(self.BASE_URL + "/v1/ticker.do", params={"symbol": symbol})
        return response.json()
    
    def place_order(self, symbol: str, type_: str, price: float, amount: float):
        params = {
            "api_key": self.api_key,
            "req_time": int(time.time() * 1000),
            "symbol": symbol,
            "type": type_,
            "price": price,
            "amount": amount,
        }
        return self._post("/v1/create_order.do", params)

    def cancel_order(self, order_id: str, symbol: str):
        params = {
            "api_key": self.api_key,
            "req_time": int(time.time() * 1000),
            "symbol": symbol,
            "order_id": order_id,
        }
        return self._post("/v1/cancel_order.do", params)
    
        