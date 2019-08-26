from PyQt5 import QtWidgets, QtCore, QtSql
from TableView import TableView
from event_info_widget import EventInfoWidget


class EventsWidget(QtWidgets.QWidget):

    def _btn_add_event_clicked(self):
        event_widget = EventInfoWidget('Добавить мероприятие')
        event_widget.signal_save_event.connect(self.slot_add_event)
        event_widget.exec()

    def add_event(self, table, event_name, event_date, event_time, event_responsible, status='current'):
        record = table.model().record()
        record.setValue('description', event_name)
        # set seconds to 00
        event_time.setHMS(event_time.hour(), event_time.minute(), 0)
        date_time = QtCore.QDateTime(event_date, event_time)
        record.setValue('date_time', date_time.toString('dd-MM-yyyy HH:mm:ss'))
        record.setValue('responsible', event_responsible)
        record.setValue('status', status)
        table.model().insertRecord(-1, record)
        table.model().submitAll()

    def slot_add_event(self, event_name, event_date, event_time, event_responsible):
        self.add_event(self.table_events, event_name, event_date, event_time, event_responsible)

    def remove_event(self, table):
        selected_cells = table.selectedIndexes()
        if len(selected_cells) == 0:
            QtWidgets.QMessageBox.information(self, 'Мероприятия',
                                              'Выберите мероприятие для удаления')
            return

        selected_cell = selected_cells[0]
        table.model().removeRow(selected_cell.row())
        table.model().submitAll()

    def _btn_remove_event_clicked(self):
        self.remove_event(self.table_events)

    def show_event(self, headline, table, selected_cell, edit_slot=None, save_button_enabled=True):
        name_index = table.model().createIndex(selected_cell.row(), 1)
        date_time_index = table.model().createIndex(selected_cell.row(), 2)
        responsible_index = table.model().createIndex(selected_cell.row(), 3)

        name_init = table.model().data(name_index)
        date_time_init = QtCore.QDateTime.fromString(
            table.model().data(date_time_index),
            'dd-MM-yyyy HH:mm:ss')
        responsible_init = table.model().data(responsible_index)

        event_widget = EventInfoWidget(headline, name_init, date_time_init.date(),
                                       date_time_init.time(), responsible_init, save_button_enabled)
        if edit_slot is not None:
            event_widget.signal_save_event.connect(slot=edit_slot)
        event_widget.exec()

    def _btn_edit_event_clicked(self):
        selected_cells = self.table_events.selectedIndexes()
        if len(selected_cells) == 0:
            QtWidgets.QMessageBox.information(self, 'Мероприятия', 'Выберите мероприятие')
            return

        selected_cell = selected_cells[0]
        self.show_event('Редактирование мероприятия', self.table_events, selected_cell, self.slot_event_edit)

    def update_table_row(self, table, event_name, event_date, event_time, event_responsible):
        selected_cell = table.selectedIndexes()[0]
        name_index = table.model().createIndex(selected_cell.row(), 1)
        date_time_index = table.model().createIndex(selected_cell.row(), 2)
        responsible_index = table.model().createIndex(selected_cell.row(), 3)

        # set seconds to 00
        event_time.setHMS(event_time.hour(), event_time.minute(), 0)
        date_time = QtCore.QDateTime(event_date, event_time)

        table.model().setData(name_index, event_name)
        table.model().setData(date_time_index,
                              date_time.toString('dd-MM-yyyy HH:mm:ss'))
        table.model().setData(responsible_index, event_responsible)
        table.model().submitAll()

    def slot_event_edit(self, event_name, event_date, event_time, event_responsible):
        self.update_table_row(self.table_events, event_name, event_date, event_time, event_responsible)

    def _btn_add_expected_event_clicked(self):
        event_widget = EventInfoWidget('Добавить мероприятие')
        event_widget.signal_save_event.connect(self.slot_add_expected_event)
        event_widget.exec()

    def slot_add_expected_event(self, event_name, event_date, event_time, event_responsible):
        self.add_event(self.table_expected_events, event_name, event_date, event_time, event_responsible,
                       status='expected')

    def _btn_remove_expected_event_cliced(self):
        self.remove_event(self.table_expected_events)

    def _btn_edit_expected_event_clicked(self):
        selected_cells = self.table_expected_events.selectedIndexes()
        if len(selected_cells) == 0:
            QtWidgets.QMessageBox.information(self, 'Мероприятия', 'Выберите мероприятие')
            return

        selected_cell = selected_cells[0]
        self.show_event('Редактирование мероприятия', self.table_expected_events, selected_cell,
                        self.slot_add_expected_event)

    def slot_expected_event_edit(self, event_name, event_date, event_time, event_responsible):
        self.update_table_row(self.table_expected_events, event_name, event_date, event_time, event_responsible)

    def _btn_accept_expected_event_clicked(self):
        selected_cells = self.table_expected_events.selectedIndexes()
        if len(selected_cells) == 0:
            QtWidgets.QMessageBox.information(self, 'Мероприятия', 'Выберите мероприятие')
            return

        selected_cell = selected_cells[0]
        self.table_expected_events.model().setData(
            self.table_expected_events.model().createIndex(selected_cell.row(), 4), 'current')
        self.table_expected_events.model().submitAll()
        self.table_events.model().submitAll()

    def _table_events_double_clicked(self, index):
        self.show_event('Просмотр мероприятия', self.table_events, index, self.slot_event_edit)

    def _table_expected_events_double_clicked(self, index):
        self.show_event('Просмотр мероприятия', self.table_expected_events, index, self.slot_expected_event_edit)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Мероприятия')

        column_id = 0
        column_status = 4

        lbl_events = QtWidgets.QLabel('Текущие мероприятия:')

        btn_add_event = QtWidgets.QPushButton('Добавить')
        btn_remove_event = QtWidgets.QPushButton('Удалить')
        btn_edit_event = QtWidgets.QPushButton('Изменить')

        btn_add_event.clicked.connect(self._btn_add_event_clicked)
        btn_remove_event.clicked.connect(self._btn_remove_event_clicked)
        btn_edit_event.clicked.connect(self._btn_edit_event_clicked)

        model_events = QtSql.QSqlTableModel()
        model_events.setTable('Event')
        model_events.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model_events.setFilter('status = "current" ORDER BY datetime(substr(date_time, 7, 4) || '
                               '"-" || substr(date_time, 4, 2) || "-" || substr(date_time, 1, 2) || " " || '
                               'substr(date_time, 12, 8)) ASC')
        model_events.select()

        self.table_events = TableView()
        self.table_events.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.table_events.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_events.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.table_events.setModel(model_events)
        self.table_events.horizontalHeader().setMinimumSectionSize(150)
        self.table_events.setColumnWidth(1, 400)
        self.table_events.setHorizontalScrollMode(QtWidgets.QTableView.ScrollPerPixel)
        self.table_events.setVerticalScrollMode(QtWidgets.QTableView.ScrollPerPixel)

        model_events.setHeaderData(1, QtCore.Qt.Horizontal, "Мероприятие")
        model_events.setHeaderData(2, QtCore.Qt.Horizontal, "Дата и время")
        model_events.setHeaderData(3, QtCore.Qt.Horizontal, "Кто привлекается")
        self.table_events.setColumnHidden(column_id, True)
        self.table_events.setColumnHidden(column_status, True)
        self.table_events.verticalHeader().setHidden(True)
        self.table_events.horizontalHeader().setStretchLastSection(True)

        self.table_events.doubleClicked.connect(self._table_events_double_clicked)

        lbl_expected_events = QtWidgets.QLabel('Планируемые мероприятия:')

        btn_add_expected_event = QtWidgets.QPushButton('Добавить')
        btn_remove_expected_event = QtWidgets.QPushButton('Удалить')
        btn_edit_expected_event = QtWidgets.QPushButton('Изменить')
        btn_accept_expected_event = QtWidgets.QPushButton('Утвердить')

        btn_add_expected_event.clicked.connect(self._btn_add_expected_event_clicked)
        btn_remove_expected_event.clicked.connect(self._btn_remove_expected_event_cliced)
        btn_edit_expected_event.clicked.connect(self._btn_edit_expected_event_clicked)
        btn_accept_expected_event.clicked.connect(self._btn_accept_expected_event_clicked)

        model_expected_events = QtSql.QSqlTableModel()
        model_expected_events.setTable('Event')
        model_expected_events.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model_expected_events.setFilter('status = "expected" ORDER BY datetime(substr(date_time, 7, 4) || '
                                        '"-" || substr(date_time, 4, 2) || "-" || substr(date_time, 1, 2) || " " || '
                                        'substr(date_time, 12, 8)) ASC')
        model_expected_events.select()

        self.table_expected_events = TableView()
        self.table_expected_events.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.table_expected_events.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_expected_events.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.table_expected_events.setModel(model_expected_events)
        self.table_expected_events.horizontalHeader().setMinimumSectionSize(150)
        self.table_expected_events.setColumnWidth(1, 400)
        self.table_expected_events.setHorizontalScrollMode(QtWidgets.QTableView.ScrollPerPixel)
        self.table_expected_events.setVerticalScrollMode(QtWidgets.QTableView.ScrollPerPixel)

        model_expected_events.setHeaderData(1, QtCore.Qt.Horizontal, "Мероприятие")
        model_expected_events.setHeaderData(2, QtCore.Qt.Horizontal, "Дата и время")
        model_expected_events.setHeaderData(3, QtCore.Qt.Horizontal, "Кто привлекается")
        self.table_expected_events.setColumnHidden(column_id, True)
        self.table_expected_events.setColumnHidden(column_status, True)
        self.table_expected_events.verticalHeader().setHidden(True)
        self.table_expected_events.horizontalHeader().setStretchLastSection(True)

        self.table_expected_events.doubleClicked.connect(self._table_expected_events_double_clicked)

        layout_events_buttons = QtWidgets.QHBoxLayout()
        layout_events_buttons.setAlignment(QtCore.Qt.AlignLeft)
        layout_events_buttons.addWidget(lbl_events)
        layout_events_buttons.addWidget(btn_add_event)
        layout_events_buttons.addWidget(btn_remove_event)
        layout_events_buttons.addWidget(btn_edit_event)

        layout_events = QtWidgets.QVBoxLayout()
        layout_events.addLayout(layout_events_buttons)
        layout_events.addWidget(self.table_events)

        layout_expected_events_buttons = QtWidgets.QHBoxLayout()
        layout_expected_events_buttons.setAlignment(QtCore.Qt.AlignLeft)
        layout_expected_events_buttons.addWidget(lbl_expected_events)
        layout_expected_events_buttons.addWidget(btn_add_expected_event)
        layout_expected_events_buttons.addWidget(btn_remove_expected_event)
        layout_expected_events_buttons.addWidget(btn_edit_expected_event)
        layout_expected_events_buttons.addWidget(btn_accept_expected_event)

        layout_expected_events = QtWidgets.QVBoxLayout()
        layout_expected_events.addLayout(layout_expected_events_buttons)
        layout_expected_events.addWidget(self.table_expected_events)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_events)
        layout_main.addLayout(layout_expected_events)

        self.setLayout(layout_main)
