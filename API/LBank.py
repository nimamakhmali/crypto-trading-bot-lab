import time
import hashlib
import hmac
import requests

API_KEY = 'your_api_key'
SECRET_KEY = 'your_secret_key'
BASE_URL = 'https://api.lbkex.com'


def sign(params, secret_key):
    sorted_params = sorted(params.items())
    sign_str = '&'.join([f"{k}={v}" for k, v in sorted_params])
    sign_str += f"&secret_key={secret_key}"
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()

def get_price(symbol='btc_usdt'):
    url = f'{BASE_URL}/v2/ticker/24hr.do'
    response = requests.get(url, params={'symbol': symbol})
    data = response.json()
    if data.get("result") == "true":
        price = data["data"][0]["latest"]
        print(f"Current price of {symbol}: {price}")
        return float(price)
    else:
        print("Error:", data)
        return None


def place_order(symbol='btc_usdt', price='20000', amount='0.001', side='buy'):
    endpoint = '/v2/order.place'
    url = BASE_URL + endpoint

    params = {
        'api_key': API_KEY,
        'symbol': symbol,
        'price': price,
        'amount': amount,
        'type': side,
        'timestamp': int(time.time() * 1000)
    }

    params['sign'] = sign(params, SECRET_KEY)
    response = requests.post(url, data=params)
    print(response.json())


if __name__ == '__main__':
    get_price()

    place_order(price='20000', amount='0.001')
