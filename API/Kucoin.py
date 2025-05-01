import time
import base64
import hmac
import hashlib
import requests

API_KEY = 'YOUR_API_KEY'
API_SECRET = 'YOUR_API_SECRET'
API_PASSPHRASE = 'YOUR_API_PASSPHRASE'
BASE_URL = 'https://api.kucoin.com'

def generate_signature(endpoint, method='GET', body=''):
    now = int(time.time() * 1000)
    str_to_sign = f'{now}{method}{endpoint}{body}'
    signature = base64.b64encode(
        hmac.new(API_SECRET.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest()
    )
    passphrase = base64.b64encode(
        hmac.new(API_SECRET.encode('utf-8'), API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest()
    )
    headers = {
        "KC-API-KEY": API_KEY,
        "KC-API-SIGN": signature.decode(),
        "KC-API-TIMESTAMP": str(now),
        "KC-API-PASSPHRASE": passphrase.decode(),
        "KC-API-KEY-VERSION": "2",
        "Content-Type": "application/json"
    }
    return headers

def get_account_balance():
    endpoint = '/api/v1/accounts'
    url = BASE_URL + endpoint
    headers = generate_signature(endpoint)
    response = requests.get(url, headers=headers)
    return response.json()


if __name__ == '__main__':
    balance = get_account_balance()
    print(balance)
