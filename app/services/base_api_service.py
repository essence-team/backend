from typing import Any, Dict

import aiohttp


# Basic service using aiohttp
class BaseService:
    def __init__(self, host: str, port: int, api_key: str = None):
        self.session = aiohttp.ClientSession()

        self.base_url = f"http://{host}:{port}"
        self.headers = {"Authorization": f"{api_key}"} if api_key else None

    async def get(self, url: str, params: Dict[str, Any] = None):
        async with self.session.get(url, params=params, headers=self.headers) as response:
            response.raise_for_status()  # Raise exception for HTTP errors
            return await response.json()

    async def post(self, url: str, data: Dict[str, Any] = None):
        async with self.session.post(url, json=data, headers=self.headers) as response:
            response.raise_for_status()
            return await response.json()

    async def close(self):
        await self.session.close()
