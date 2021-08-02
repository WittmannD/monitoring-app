import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from gui.ui import Ui_MainWindow
from setting import APP_SETTINGS


def receive_stored_data():
    setting = APP_SETTINGS
    titles = setting.value('titles', [], type=list)
    monitors = setting.value('monitors', [], type=list)

    return titles, monitors


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.stored_data = receive_stored_data()

        with open('./assets/style.qss', encoding='utf-8') as f:
            QApplication.instance().setStyleSheet(f.read())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()

