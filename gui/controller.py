from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from typing import NamedTuple
from models import PreparedTitleModel


class Controller(QObject):
    tilted_listener = pyqtSignal(PreparedTitleModel)

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)

    def __init__(self, ui, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)

        self.ui = ui

        self.ui.top_bar_widget.close_button.clicked.connect(self.close_window)
        self.ui.top_bar_widget.maximize_button.clicked.connect(self.maximize_window)
        self.ui.top_bar_widget.minimize_button.clicked.connect(self.minimize_window)

        self.ui.add_monitor_button.clicked.connect(self.add_monitor_popup)

        self.tilted_listener.connect(self.tilted_listener_slot)

        self.finished.connect(self.finished_slot)
        self.error.connect(self.error_slot)
        self.result.connect(self.result_slot)

    def tilted_listener_slot(self, data: PreparedTitleModel):
        self.ui.add_item(data)

    def error_slot(self, data):
        print(data)

    def result_slot(self, data):
        print(data)

    def finished_slot(self, data):
        print(data)

    @pyqtSlot()
    def close_window(self):
        self.ui.close()

    @pyqtSlot()
    def maximize_window(self):
        self.ui.showMaximized()

    @pyqtSlot()
    def minimize_window(self):
        self.ui.showMinimized()

    @pyqtSlot()
    def add_monitor_popup(self):
        self.ui.left_container_tab_widget.setCurrentIndex(1)
