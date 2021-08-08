"""Monitors module."""

import logging
import time
from typing import Dict, Any

from aiohttp import ClientResponse

from client import HttpClient
from setting import *


class Monitor:

    def __init__(self, check_every: int) -> None:
        self.check_every = check_every
        self.logger = logging.getLogger(self.__class__.__name__)

    async def check(self) -> None:
        raise NotImplementedError()


class HttpMonitor(Monitor):

    def __init__(
            self,
            http_client: HttpClient,
            options: Dict[str, Any],
            callback: Any
    ) -> None:
        self._client = http_client
        self._url = options.pop('url')
        self._timeout = options.pop('timeout')
        self._payload = options.pop('payload')
        self._description = options.pop('description')
        self._method = options.pop('method')

        self.callback = callback

        super().__init__(check_every=options.pop('check_every'))

    async def check(self) -> None:
        time_start = time.time()

        response_json = {}
        async def request_callback(response: ClientResponse):
            response_json.update(await response.json())
            return response

        response = await self._client.request(
            url=self._url,
            timeout=self._timeout,
            payload=self._payload,
            method=self._method,
            cb=request_callback
        )

        time_end = time.time()
        time_took = time_end - time_start

        self.logger.info(
            'Check\n'
            '    %s %s\n'
            '    response code: %s\n'
            '    content length: %s\n'
            '    request took: %s seconds',
            self._description,
            self._url,
            response.status,
            response.content_length,
            round(time_took, 3)
        )

        self.callback(response_json)
