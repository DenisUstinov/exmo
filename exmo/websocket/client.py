import json

import backoff
import websockets
import websockets.exceptions

from typing import Dict, Any, Callable, Coroutine


class Client:
    def __init__(self, response_handler: Callable[[dict], Coroutine]) -> None:
        self.response_handler = response_handler

    @backoff.on_exception(backoff.expo, websockets.exceptions.WebSocketException, max_tries=5)
    async def subscribe_and_listen(self, data: Dict[str, Any]) -> None:
        async with websockets.connect(data['url']) as websocket:
            for message in data.get('init_messages', []):
                await websocket.send(message)

            while True:
                response = await websocket.recv()
                try:
                    response_obj = json.loads(response)
                except json.JSONDecodeError:
                    raise ValueError("Invalid JSON object received")
                await self.response_handler(response_obj)
