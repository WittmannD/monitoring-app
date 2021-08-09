import logging.config
import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication

from client import HttpClient
from config import Config
from gui.controller import Controller
from gui.main import MainWindow
from monitoring import Monitoring
from process import DataProcessing

if __name__ == '__main__':
    config = Config()

    logging.config.dictConfig(config.get('logging'))

    app = QApplication(sys.argv)

    QCoreApplication.setOrganizationName('mushokutensei')
    QCoreApplication.setOrganizationDomain('mushokutensei.herokuapp.com')
    QCoreApplication.setApplicationName('Monitoring Bot')

    main_window = MainWindow(config.get('monitoring'))
    http_client = HttpClient()

    controller = Controller(main_window)
    processing = DataProcessing(controller, http_client=http_client)

    monitoring = Monitoring(controller, processing, http_client=http_client)

    main_window.show()
    app.exec()

    monitoring.stop()
