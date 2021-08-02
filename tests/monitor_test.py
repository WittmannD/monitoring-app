import asyncio
import logging

from client import HttpClient
from config import Config
from monitor import HttpMonitor


async def test() -> None:
    http_client = HttpClient()
    config = Config()
    monitor = HttpMonitor(http_client, config['monitors']['seoji'])

    await monitor.check()


if __name__ == '__main__':
    logging.basicConfig(filename='monitor_test.log', level=logging.INFO,
                        format='[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s')
    asyncio.run(test(), debug=True)
