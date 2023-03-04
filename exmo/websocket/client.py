import asyncio
import time
import base64
import hashlib
import hmac
import logging

import websockets

from typing import Dict, Any, Callable, Coroutine


class Client:
    def __init__(self, response_handler: Callable[[str], Coroutine]) -> None:
        self.response_handler = response_handler
        self.logger = logging.getLogger(__name__)

    async def listen(self, data: Dict[str, Any]) -> None:
        reconnect_delay = 5
        while True:
            try:
                async with websockets.connect(data['url']) as websocket:
                    for message in data.get('init_messages', []):
                        await websocket.send(message)

                    while True:
                        response = await websocket.recv()
                        await self.response_handler(response)
            except websockets.exceptions.ConnectionClosed as e:
                error_msg = f"Connection closed: {e}. Reconnecting in {reconnect_delay} seconds..."
                self.logger.error(error_msg, exc_info=True)
                await asyncio.sleep(reconnect_delay)
                reconnect_delay *= 2  # увеличиваем время между попытками вдвое

    @staticmethod
    def create_login_message(api_key: str, secret_key: str) -> str:
        nonce = str(time.time_ns())
        sign = hmac.new(secret_key.encode('utf8'), (api_key + nonce).encode('utf8'), hashlib.sha512).digest()
        sign = base64.b64encode(sign).decode('utf8')
        return '{"id":1,"method":"login","api_key":"%s","sign":"%s","nonce":%s}' % (api_key, sign, nonce)
