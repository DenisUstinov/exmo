# client.py
import asyncio
import time
import hashlib
import hmac
import base64
import websockets
import json


class Client:
    def __init__(self, response_handler):
        self.response_handler = response_handler

    async def listen(self, data):
        async with websockets.connect(data['url']) as websocket:
            for message in data['init_messages']:
                await websocket.send(message)

            while True:
                string = await websocket.recv()
                response = json.loads(string)
                await self.response_handler(response)

    @staticmethod
    async def create_login_message(api_key, secret_key):
        nonce = str(time.time_ns())
        sign = hmac.new(secret_key.encode('utf8'), (api_key + nonce).encode('utf8'), hashlib.sha512).digest()
        sign = base64.b64encode(sign).decode('utf8')
        return '{"id":1,"method":"login","api_key":"%s","sign":"%s","nonce":%s}' % (api_key, sign, nonce)
