from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
import sys
import asyncio
import logging
import logging.config

from client import HttpClient
from config import Config
from monitor import HttpMonitor
from monitoring import Monitoring
from process import DataProcessing

from gui.main import MainWindow
from gui.controller import Controller


if __name__ == '__main__':
    config = Config()

    logging.config.dictConfig(config.get('logging'))

    app = QApplication(sys.argv)
    QCoreApplication.setOrganizationName('mushokutensei')
    QCoreApplication.setOrganizationDomain('mushokutensei.herokuapp.com')
    QCoreApplication.setApplicationName('Monitoring Bot')

    main_window = MainWindow()
    http_client = HttpClient()

    controller = Controller(main_window)
    processing = DataProcessing(controller, http_client=http_client)

    monitors = [
        HttpMonitor(http_client, config.get('monitoring')['monitors']['seoji1'], processing.run)
    ]

    monitoring = Monitoring(monitors, controller)

    monitoring.start()

    main_window.show()
    app.exec()
    monitoring.stop()
