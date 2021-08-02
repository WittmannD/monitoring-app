import logging

from client import HttpClient
from config import Config
from dispatcher import Dispatcher
from monitor import HttpMonitor
from process import DataProcessing


def test() -> None:
    def cb(title):
        print(title)

    config = Config()
    processing = DataProcessing(cb)
    monitors = [
        HttpMonitor(HttpClient(), config['monitors']['seoji1'], processing.run),
        HttpMonitor(HttpClient(), config['monitors']['seoji2'], processing.run),
        HttpMonitor(HttpClient(), config['monitors']['seoji3'], processing.run),
        HttpMonitor(HttpClient(), config['monitors']['seoji4'], processing.run)
    ]
    dispatcher = Dispatcher(monitors)
    dispatcher.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s')
    test()
