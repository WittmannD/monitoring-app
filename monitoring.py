from dispatcher import Dispatcher
from monitor import HttpMonitor

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import traceback, sys
import logging


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = kwargs.pop('controller')
        self._logger = logging.getLogger(self.__class__.__name__)

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)

        except Exception as err:
            traceback.print_exc()
            # exctype, value = sys.exc_info()[:2]
            self._logger.exception('Worker error', exc_info=sys.exc_info()[:2])

        #     self.signals.error.emit((exctype, value, traceback.format_exc()))
        #
        # else:
        #     self.signals.result.emit(result)  # Return the result of the processing
        #
        # finally:
        #     self.signals.finished.emit()  # Done


class Monitoring:
    def __init__(self, monitors: list, controller):
        self._monitors = monitors
        self._controller = controller

        self.dispatcher = Dispatcher(self._monitors)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def start(self):
        # Pass the function to execute
        worker = Worker(self.dispatcher.run, controller=self._controller) # Any other args, kwargs are passed to the run function
        # worker.signals.result.connect(self.print_output)
        # worker.signals.finished.connect(self.thread_complete)

        # Execute
        self.threadpool.start(worker)

    def add_monitor(self, monitor: HttpMonitor):
        self._monitors.append(monitor)

    def stop(self):
        self.dispatcher.stop()
