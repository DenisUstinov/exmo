import json
import time
import base64
import hashlib
import hmac


def create_login_message(api_key: str, secret_key: str) -> str:
    nonce = str(time.time_ns())
    message = api_key + nonce
    sign = hmac.new(secret_key.encode('utf8'), message.encode('utf8'), hashlib.sha512).digest()
    sign = base64.b64encode(sign).decode('utf8')
    return json.dumps({
        "id": 1,
        "method": "login",
        "api_key": api_key,
        "sign": sign,
        "nonce": nonce
    })
