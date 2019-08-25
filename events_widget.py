from PyQt5 import QtWidgets, QtCore, QtSql
from TableView import TableView


class EventsWidget(QtWidgets.QWidget):

    def _btn_add_event_clicked(self):
        pass

    def _btn_remove_event_cliced(self):
        pass

    def _btn_edit_event_clicked(self):
        pass

    def _btn_add_expected_event_clicked(self):
        pass

    def _btn_remove_expected_event_cliced(self):
        pass

    def _btn_edit_expected_event_clicked(self):
        pass

    def _btn_accept_expected_event_clicked(self):
        pass

    def _table_events_double_clicked(self):
        pass

    def _table_expected_events_double_clicked(self):
        pass

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
        btn_remove_event.clicked.connect(self._btn_remove_event_cliced)
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
