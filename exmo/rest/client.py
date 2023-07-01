import json
import backoff
import aiohttp


class Client:
    def __init__(self) -> None:
        self.session = aiohttp.ClientSession()

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=5)
    async def request(self, url: str, method: str = 'GET', headers: dict = None, data: dict = None) -> dict:
        try:
            async with self.session.request(method, url, headers=headers, data=data) as response:
                try:
                    response_obj = await response.json()
                except json.JSONDecodeError:
                    raise ValueError("Invalid JSON object received")
                return response_obj
        except aiohttp.ClientError as e:
            raise ValueError(f'Error fetching {url}: {str(e)}')

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
