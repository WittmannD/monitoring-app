"""Http client module."""

from aiohttp import ClientSession, ClientTimeout, ClientResponse
from typing import Tuple, Any


class HttpClient:

    @staticmethod
    async def request(
            url: str,
            timeout: int,
            payload: dict = None,
            method: str = 'POST',
            cb: Any = None
    ) -> ClientResponse:

        async with ClientSession(timeout=ClientTimeout(timeout)) as session:
            async with session.request(method=method, url=url, data=payload) as response:
                return await cb(response)

    @staticmethod
    async def session(
            timeout: int,
            cb: Any = None
    ) -> ClientResponse:
        async with ClientSession(timeout=ClientTimeout(timeout)) as session:
            return await cb(session)
