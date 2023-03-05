import time
import base64
import hashlib
import hmac

import backoff
import websockets
import websockets.exceptions

from typing import Dict, Any, Callable, Coroutine


class Client:
    def __init__(self, response_handler: Callable[[str], Coroutine]) -> None:
        self.response_handler = response_handler

    @backoff.on_exception(backoff.expo, websockets.exceptions.WebSocketException, max_tries=5, interval=1)
    async def listen(self, data: Dict[str, Any]) -> None:
        async with websockets.connect(data['url']) as websocket:
            for message in data.get('init_messages', []):
                await websocket.send(message)

            while True:
                response = await websocket.recv()
                await self.response_handler(response)

    @staticmethod
    def create_login_message(api_key: str, secret_key: str) -> str:
        nonce = str(time.time_ns())
        sign = hmac.new(secret_key.encode('utf8'), (api_key + nonce).encode('utf8'), hashlib.sha512).digest()
        sign = base64.b64encode(sign).decode('utf8')
        return f'{{"id":1,"method":"login","api_key":"{api_key}","sign":"{sign}","nonce":{nonce}}}'

