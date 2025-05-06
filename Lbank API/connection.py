import time
import hmac
import hashlib
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class LBankAPI:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        self.base_url = "https://api.lbank.info"
    
    def sign_parameters(self, params):
        sorted_params = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
        sign = hmac.new(self.api_secret.encode(), sorted_params.encode(), hashlib.md5).hexdigest()
        return sign
    
    def get_account_info(self):
            endpoint = "/v1/user_info.do"
            params = {
                "api_key": self.api_key,
                "req_time": int(time.time() * 1000),
            }
            params["sign"] = self.sign_params(params)
            res = requests.post(self.base_url + endpoint, data=params)
            return res.json()
        
api = LBankAPI()
print(api.get_account_info())
        