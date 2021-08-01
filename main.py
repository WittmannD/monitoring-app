from process import DataProcessing
from dispatcher import Dispatcher
from monitor import HttpMonitor
from client import HttpClient
from config import Config
from monitoring import Monitoring


def callback_placeholder(*args, **kwargs):
    print(args, kwargs)


if __name__ == '__main__':
    config = Config()
    http_client = HttpClient()
    processing = DataProcessing(callback_placeholder, http_client=http_client)

    monitors = [
        HttpMonitor(http_client, config)
    ]

    monitoring = Monitoring(config, processing, monitors)

