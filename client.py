"""Http client module."""

from aiohttp import ClientSession, ClientTimeout, ClientResponse
from typing import Tuple


class HttpClient:

    @staticmethod
    async def request(url: str, payload: dict, timeout: int) -> Tuple[ClientResponse, dict]:
        async with ClientSession(timeout=ClientTimeout(timeout)) as session:
            async with session.post(url, data=payload) as response:
                json = await response.json()
                return response, json
