from dispatcher import Dispatcher
from monitor import HttpMonitor


class Monitoring:
    def __init__(self, config, processing, monitors: list):
        self._monitors = monitors
        self.processing = processing
        self.config = config

        self.dispatcher = Dispatcher(self._monitors)

    def start(self):
        self.dispatcher.run()

    def add_monitor(self, monitor: HttpMonitor):
        self._monitors.append(monitor)

    def stop(self):
        self.dispatcher.stop()

