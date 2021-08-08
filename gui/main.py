from datetime import datetime
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QSettings

from gui.browser.form_filler import FormFiller
from gui.ui import Ui_MainWindow

from models import PreparedTitleModel, MonitorModel


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, config):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.config = config
        self.settings = QSettings()

        self.stored_titles.update(self.settings.value('titles', set(), set))
        self.stored_monitors.update(self.settings.value('monitors', set(), set))

        self.init_stored_data()

        self.form_filler = FormFiller(self.browser_page)

        with open('./assets/style.qss', encoding='utf-8') as f:
            QApplication.instance().setStyleSheet(f.read())

        self.load_monitors(self.config.get('monitors'))

    def load_monitors(self, monitors: dict):
        monitors = list(map(
            lambda monitor_name:
                MonitorModel(
                    name=monitor_name,
                    keyword=monitors[monitor_name]['payload']['q'],
                    description=monitors[monitor_name]['description'],
                    timestamp=None
                ),
            monitors
        ))
        super(MainWindow, self).load_monitors(monitors)

    def init_stored_data(self):
        for title in sorted(self.stored_titles, key=lambda o: o.timestamp):
            self.add_item(title)

        for monitor in sorted(self.stored_monitors, key=lambda o: o.timestamp):
            self.add_monitor(monitor)

    def closeEvent(self, a0) -> None:
        self.settings.setValue('titles', self.stored_titles)
        self.settings.setValue('monitors', self.stored_monitors)
        
        super(MainWindow, self).closeEvent(a0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()

