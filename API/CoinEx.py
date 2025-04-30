import time
import requests
import hmac
import hashlib

base_url = 'https://api.coinex.com'
request_path = '/v2/account/info'
timestamp = int(time.time()* 1000)
access_id = 'id'
secret_key = 'key'
string_to_sign = f'GET{request_path}{timestamp}'
signature = hmac.new(secret_key.encode(), string_to_sign.encode(), hashlib.sha256).hexdigest()

headers = {
    'X-COINEX-KEY': access_id,
    'X-COINEX-SIGN': signature,
    'X-COINEX-TIMESTAMP': str(timestamp)
}

response = requests.get(base_url + request_path, headers=headers)
print(response.json())