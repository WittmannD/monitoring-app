from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt

from models import PreparedTitleModel


class Controller(QObject):
    title_transfer = pyqtSignal(PreparedTitleModel)
    titles_found = pyqtSignal(list)
    start_monitoring = pyqtSignal(list)

    def __init__(self, ui, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)

        self.ui = ui

        self.ui.top_bar_widget.close_button.clicked.connect(self.close_window)
        self.ui.top_bar_widget.maximize_button.clicked.connect(self.maximize_window)
        self.ui.top_bar_widget.minimize_button.clicked.connect(self.minimize_window)

        self.ui.add_monitor_button.clicked.connect(self.add_monitor_slot)
        self.ui.monitor_remove_button.clicked.connect(self.monitor_remove_slot)
        self.ui.monitor_reload_button.clicked.connect(self.reload_monitors_slot)

        self.title_transfer.connect(self.title_transfer_slot)
        self.titles_found.connect(self.titles_found_slot)

        self.ui.fill_form.connect(self.fill_form_slot)
        self.ui.delete_item.connect(self.ui.delete_item_slot)

    def title_transfer_slot(self, data: PreparedTitleModel):
        self.ui.add_item(data)

    def titles_found_slot(self, data):
        self.ui.notify(data)

    def fill_form_slot(self, data: PreparedTitleModel):
        self.ui.right_container_tab_widget.setCurrentIndex(1)

        if not self.ui.form_filler.view.loaded:

            def _loadFinished(ok):
                self.ui.form_filler.view.loaded = True
                self.ui.form_filler.start(data)

            self.ui.form_filler.view.loadFinished.connect(_loadFinished)

        else:
            self.ui.form_filler.start(data)

    @pyqtSlot()
    def reload_monitors_slot(self):
        monitors = []
        for i in range(self.ui.monitor_list.count()):
            item = self.ui.monitor_list.item(i)
            widget = self.ui.monitor_list.itemWidget(item)

            widget.icon_widget.hide()

            name = item.data(Qt.UserRole + 1)

            monitors.append(self.ui.config.get('monitors').get(name))

        self.start_monitoring.emit(monitors)

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
    def add_monitor_slot(self):
        self.ui.left_container_tab_widget.setCurrentIndex(1)

    @pyqtSlot()
    def monitor_remove_slot(self):
        monitors_for_delete = []
        for item in self.ui.monitor_list.selectedItems():
            data = item.data(Qt.UserRole)
            # self.ui.monitor_list.removeItemWidget(item)
            self.ui.monitor_list.takeItem(self.ui.monitor_list.row(item))

            monitors_for_delete.append(data)

        self.ui.stored_monitors = set(filter(lambda o: o.timestamp not in monitors_for_delete, self.ui.stored_monitors))
