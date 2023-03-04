import time
import hashlib
import hmac
import base64
import websockets
from typing import Dict, Any, Callable


class Client:
    def __init__(self, response_handler: Callable[[str], None]) -> None:
        self.response_handler = response_handler

    async def listen(self, data: Dict[str, Any]) -> None:
        async with websockets.connect(data['url']) as websocket:
            for message in data['init_messages']:
                await websocket.send(message)

            while True:
                try:
                    response = await websocket.recv()
                except websockets.exceptions.ConnectionClosed as e:
                    raise Exception("WebSocket connection closed unexpectedly") from e
                except Exception as e:
                    raise Exception("WebSocket error occurred") from e

                await self.response_handler(response)

    @staticmethod
    def create_login_message(api_key: str, secret_key: str) -> str:
        nonce = str(time.time_ns())
        sign = hmac.new(secret_key.encode('utf8'), (api_key + nonce).encode('utf8'), hashlib.sha512).digest()
        sign = base64.b64encode(sign).decode('utf8')
        return '{"id":1,"method":"login","api_key":"%s","sign":"%s","nonce":%s}' % (api_key, sign, nonce)

