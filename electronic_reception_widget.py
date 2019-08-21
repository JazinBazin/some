from PyQt5 import QtWidgets, QtCore, QtSql
from request_widget import RequestWidget


class ElectronicReceptionWidget(QtWidgets.QWidget):

    def _btn_add_request_clicked(self):
        request_widget = RequestWidget('Добавить заявку')
        request_widget.signal_save_request.connect(self.slot_add_request)
        request_widget.exec()

    def slot_add_request(self, request_family_name, request_name, request_surname,
                         request_date, request_time, request_reason):
        record = self.table_current_requests.model().record()
        record.setValue('family_name', request_family_name)
        record.setValue('name', request_name)
        record.setValue('surname', request_surname)
        date_time = QtCore.QDateTime(request_date, request_time)
        record.setValue('date_time', date_time.toString('dd-MM-yyyy HH:mm:ss'))
        record.setValue('reason', request_reason)
        record.setValue('status', 'not accepted')
        self.table_current_requests.model().insertRecord(-1, record)
        self.table_current_requests.model().submitAll()

    def remove_request(self, table):
        selected_cells = table.selectedIndexes()
        if len(selected_cells) == 0:
            QtWidgets.QMessageBox.information(self, 'Электронная приёмная', 'Выберите заявку для удаления')
            return

        selected_cell = selected_cells[0]
        table.model().removeRow(selected_cell.row())
        table.model().submitAll()

    def _btn_remove_request_clicked(self):
        self.remove_request(self.table_current_requests)

    def show_request(self, headline, table, selected_cell):
        family_name_index = table.model().createIndex(selected_cell.row(), 1)
        name_index = table.model().createIndex(selected_cell.row(), 2)
        surname_index = table.model().createIndex(selected_cell.row(), 3)
        date_time_index = table.model().createIndex(selected_cell.row(), 4)
        reason_index = table.model().createIndex(selected_cell.row(), 5)

        family_name_init = table.model().data(family_name_index)
        name_init = table.model().data(name_index)
        surname_init = table.model().data(surname_index)
        date_time_init = QtCore.QDateTime.fromString(
            table.model().data(date_time_index),
            'dd-MM-yyyy HH:mm:ss')
        reason_init = table.model().data(reason_index)

        request_widget = RequestWidget(headline, family_name_init, name_init, surname_init,
                                       date_time_init.date(), date_time_init.time(), reason_init)
        request_widget.signal_save_request.connect(slot=self.slot_request_edit)
        request_widget.exec()

    def _btn_edit_request_clicked(self):
        selected_cells = self.table_current_requests.selectedIndexes()
        if len(selected_cells) == 0:
            QtWidgets.QMessageBox.information(self, 'Электронная приёмная', 'Выберите заявку')
            return

        selected_cell = selected_cells[0]
        self.show_request('Редактирование заявки', self.table_current_requests, selected_cell)

    def slot_request_edit(self, request_family_name, request_name, request_surname,
                          request_date, request_time, request_reason):
        selected_cell = self.table_current_requests.selectedIndexes()[0]
        family_name_index = self.table_current_requests.model().createIndex(selected_cell.row(), 1)
        name_index = self.table_current_requests.model().createIndex(selected_cell.row(), 2)
        surname_index = self.table_current_requests.model().createIndex(selected_cell.row(), 3)
        date_time_index = self.table_current_requests.model().createIndex(selected_cell.row(), 4)
        reason_index = self.table_current_requests.model().createIndex(selected_cell.row(), 5)

        date_time = QtCore.QDateTime(request_date, request_time)
        self.table_current_requests.model().setData(family_name_index, request_family_name)
        self.table_current_requests.model().setData(name_index, request_name)
        self.table_current_requests.model().setData(surname_index, request_surname)
        self.table_current_requests.model().setData(date_time_index,
                                                    date_time.toString('dd-MM-yyyy HH:mm:ss'))
        self.table_current_requests.model().setData(reason_index, request_reason)
        self.table_current_requests.model().submitAll()

    def _btn_accept_request_clicked(self):
        selected_cells = self.table_current_requests.selectedIndexes()
        if len(selected_cells) == 0:
            QtWidgets.QMessageBox.information(self, 'Электронная приёмная', 'Выберите заявку')
            return

        selected_cell = selected_cells[0]
        self.table_current_requests.model().setData(
            self.table_current_requests.model().createIndex(selected_cell.row(), 6), 'accepted')
        self.table_current_requests.model().submitAll()
        self.table_accepted_requests.model().submitAll()

    def _btn_refuse_request_clicked(self):
        self._btn_remove_request_clicked()

    def _table_current_requests_double_clicked(self, index):
        self.show_request('Просмотр задачи', self.table_current_requests, index)

    def _table_completed_requests_double_clicked(self, index):
        self.show_request('Просмотр задачи', self.table_accepted_requests, index)

    def _btn_remove_accepted_request_clicked(self):
        self.remove_request(self.table_accepted_requests)

    def _btn_clear_accepted_requests_clicked(self):
        rows_count = self.table_accepted_requests.model().rowCount()
        for row in range(rows_count - 1, -1, -1):
            self.table_accepted_requests.model().removeRow(row)
            self.table_accepted_requests.setRowHidden(row, True)
        self.table_accepted_requests.model().submitAll()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Электронная приёмная')

        column_id = 0
        column_status = 6

        lbl_current_requests = QtWidgets.QLabel('Заявки на приём:')

        model_current_requests = QtSql.QSqlTableModel()
        model_current_requests.setTable('Request')
        model_current_requests.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model_current_requests.setFilter('status = "not accepted" ORDER BY datetime(substr(date_time, 7, 4) || '
                                         '"-" || substr(date_time, 4, 2) || "-" || substr(date_time, 1, 2) || " " || '
                                         'substr(date_time, 12, 8)) ASC')
        model_current_requests.select()

        self.table_current_requests = QtWidgets.QTableView()
        self.table_current_requests.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.table_current_requests.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_current_requests.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.table_current_requests.setModel(model_current_requests)
        self.table_current_requests.horizontalHeader().setMinimumSectionSize(150)
        self.table_current_requests.setHorizontalScrollMode(QtWidgets.QTableView.ScrollPerPixel)
        self.table_current_requests.setVerticalScrollMode(QtWidgets.QTableView.ScrollPerPixel)
        self.table_current_requests.horizontalHeader().setMinimumSectionSize(150)

        model_current_requests.setHeaderData(1, QtCore.Qt.Horizontal, "Фамилия")
        model_current_requests.setHeaderData(2, QtCore.Qt.Horizontal, "Имя")
        model_current_requests.setHeaderData(3, QtCore.Qt.Horizontal, "Отчество")
        model_current_requests.setHeaderData(4, QtCore.Qt.Horizontal, "Дата и время")
        model_current_requests.setHeaderData(5, QtCore.Qt.Horizontal, "Причина")
        self.table_current_requests.setColumnHidden(column_id, True)
        self.table_current_requests.setColumnHidden(column_status, True)
        self.table_current_requests.verticalHeader().setHidden(True)
        self.table_current_requests.horizontalHeader().setStretchLastSection(True)

        self.table_current_requests.doubleClicked.connect(self._table_current_requests_double_clicked)

        btn_add_request = QtWidgets.QPushButton('Добавить')
        btn_remove_request = QtWidgets.QPushButton('Удалить')
        btn_edit_request = QtWidgets.QPushButton('Изменить')
        btn_accept_request = QtWidgets.QPushButton('Принять')
        btn_refuse_request = QtWidgets.QPushButton('Отклонить')
        btn_remove_accepted_request = QtWidgets.QPushButton('Удалить')
        btn_clear_accepted_request = QtWidgets.QPushButton('Очистить')

        btn_add_request.clicked.connect(self._btn_add_request_clicked)
        btn_remove_request.clicked.connect(self._btn_remove_request_clicked)
        btn_edit_request.clicked.connect(self._btn_edit_request_clicked)
        btn_accept_request.clicked.connect(self._btn_accept_request_clicked)
        btn_refuse_request.clicked.connect(self._btn_refuse_request_clicked)
        btn_remove_accepted_request.clicked.connect(self._btn_remove_accepted_request_clicked)
        btn_clear_accepted_request.clicked.connect(self._btn_clear_accepted_requests_clicked)

        layout_current_requests_list_buttons = QtWidgets.QHBoxLayout()
        layout_current_requests_list_buttons.setAlignment(QtCore.Qt.AlignLeft)
        layout_current_requests_list_buttons.addWidget(lbl_current_requests)
        layout_current_requests_list_buttons.addWidget(btn_add_request)
        layout_current_requests_list_buttons.addWidget(btn_remove_request)
        layout_current_requests_list_buttons.addWidget(btn_edit_request)
        layout_current_requests_list_buttons.addWidget(btn_accept_request)
        layout_current_requests_list_buttons.addWidget(btn_refuse_request)

        layout_current_requests = QtWidgets.QVBoxLayout()
        layout_current_requests.addLayout(layout_current_requests_list_buttons)
        layout_current_requests.addWidget(self.table_current_requests)

        lbl_accepted_requests = QtWidgets.QLabel('Принятые заявки:')

        model_accepted_requests = QtSql.QSqlTableModel()
        model_accepted_requests.setTable('Request')
        model_accepted_requests.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model_accepted_requests.setFilter('status = "accepted" ORDER BY datetime(substr(date_time, 7, 4) || '
                                          '"-" || substr(date_time, 4, 2) || "-" || substr(date_time, 1, 2) || " " || '
                                          'substr(date_time, 12, 8)) ASC')
        model_accepted_requests.select()

        self.table_accepted_requests = QtWidgets.QTableView()
        self.table_accepted_requests.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.table_accepted_requests.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_accepted_requests.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.table_accepted_requests.setModel(model_accepted_requests)
        self.table_accepted_requests.horizontalHeader().setMinimumSectionSize(150)
        self.table_accepted_requests.setHorizontalScrollMode(QtWidgets.QTableView.ScrollPerPixel)
        self.table_accepted_requests.setVerticalScrollMode(QtWidgets.QTableView.ScrollPerPixel)
        self.table_accepted_requests.horizontalHeader().setMinimumSectionSize(150)

        model_accepted_requests.setHeaderData(1, QtCore.Qt.Horizontal, "Фамилия")
        model_accepted_requests.setHeaderData(2, QtCore.Qt.Horizontal, "Имя")
        model_accepted_requests.setHeaderData(3, QtCore.Qt.Horizontal, "Отчество")
        model_accepted_requests.setHeaderData(4, QtCore.Qt.Horizontal, "Дата и время")
        model_accepted_requests.setHeaderData(5, QtCore.Qt.Horizontal, "Причина")
        self.table_accepted_requests.setColumnHidden(column_id, True)
        self.table_accepted_requests.setColumnHidden(column_status, True)
        self.table_accepted_requests.verticalHeader().setHidden(True)
        self.table_accepted_requests.horizontalHeader().setStretchLastSection(True)

        layout_accepted_requests_buttons = QtWidgets.QHBoxLayout()
        layout_accepted_requests_buttons.setAlignment(QtCore.Qt.AlignLeft)
        layout_accepted_requests_buttons.addWidget(lbl_accepted_requests)
        layout_accepted_requests_buttons.addWidget(btn_remove_accepted_request)
        layout_accepted_requests_buttons.addWidget(btn_clear_accepted_request)

        layout_accepted_requests = QtWidgets.QVBoxLayout()
        layout_accepted_requests.addLayout(layout_accepted_requests_buttons)
        layout_accepted_requests.addWidget(self.table_accepted_requests)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_current_requests)
        layout_main.addLayout(layout_accepted_requests)

        self.setLayout(layout_main)
