from dispatcher import Dispatcher
from monitor import HttpMonitor
from client import HttpClient
from config import Config

import logging


def test() -> None:
    monitors = [
        HttpMonitor(HttpClient(), Config()['monitors']['seoji1']),
        HttpMonitor(HttpClient(), Config()['monitors']['seoji2']),
        HttpMonitor(HttpClient(), Config()['monitors']['seoji3']),
        HttpMonitor(HttpClient(), Config()['monitors']['seoji4'])
    ]
    dispatcher = Dispatcher(monitors)
    dispatcher.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s')
    test()
