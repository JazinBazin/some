from PyQt5 import QtWidgets, QtSql, QtCore
from task_widget import TaskWidget
from colored_sql_table_model import ColoredSqlTableModel


class TasksControlWidget(QtWidgets.QWidget):

    def _btn_add_task_clicked(self):
        task_widget = TaskWidget('Добавить задачу')
        task_widget.signal_save_task.connect(slot=self.slot_add_task)
        task_widget.exec()

    def slot_add_task(self, period_date, period_time, responsible,
                      description, notes):
        record = self.table_current_tasks.model().record()
        record.setValue('description', description)
        date_time = QtCore.QDateTime(period_date, period_time)
        record.setValue('period', date_time.toString('dd-MM-yyyy HH:mm:ss'))
        record.setValue('responsible', responsible)
        record.setValue('notes', notes)
        record.setValue('status', 'not completed')
        self.table_current_tasks.model().insertRecord(-1, record)
        self.table_current_tasks.model().submitAll()

    def remove_task(self, table):
        selected_cells = table.selectedIndexes()
        if len(selected_cells) == 0:
            QtWidgets.QMessageBox.information(self, 'Контроль задач', 'Выберите задачу для удаления')
            return

        selected_cell = selected_cells[0]
        table.model().removeRow(selected_cell.row())
        table.model().submitAll()

    def _btn_remove_task_clicked(self):
        self.remove_task(self.table_current_tasks)

    def show_task(self, headline, table, selected_cell):
        description_index = table.model().createIndex(selected_cell.row(), 1)
        date_time_index = table.model().createIndex(selected_cell.row(), 2)
        responsible_index = table.model().createIndex(selected_cell.row(), 3)
        notes_index = table.model().createIndex(selected_cell.row(), 4)

        description_init = table.model().data(description_index)
        date_time = QtCore.QDateTime.fromString(
            table.model().data(date_time_index),
            'dd-MM-yyyy HH:mm:ss')
        responsible_init = table.model().data(responsible_index)
        notes_init = table.model().data(notes_index)

        task_widget = TaskWidget(headline, date_time.date(), date_time.time(),
                                 responsible_init, description_init, notes_init)
        task_widget.signal_save_task.connect(slot=self.slot_task_edit)
        task_widget.exec()

    def _btn_edit_task_clicked(self):
        selected_cells = self.table_current_tasks.selectedIndexes()
        if len(selected_cells) == 0:
            QtWidgets.QMessageBox.information(self, 'Контроль задач', 'Выберите задачу')
            return

        selected_cell = selected_cells[0]
        self.show_task('Редактирование задачи', self.table_current_tasks, selected_cell)

    def slot_task_edit(self, period_date, period_time, responsible,
                       description, notes):
        selected_cell = self.table_current_tasks.selectedIndexes()[0]
        description_index = self.table_current_tasks.model().createIndex(selected_cell.row(), 1)
        date_time_index = self.table_current_tasks.model().createIndex(selected_cell.row(), 2)
        responsible_index = self.table_current_tasks.model().createIndex(selected_cell.row(), 3)
        notes_index = self.table_current_tasks.model().createIndex(selected_cell.row(), 4)

        date_time = QtCore.QDateTime(period_date, period_time)
        self.table_current_tasks.model().setData(description_index, description)
        self.table_current_tasks.model().setData(date_time_index, date_time.toString('dd-MM-yyyy HH:mm:ss'))
        self.table_current_tasks.model().setData(responsible_index, responsible)
        self.table_current_tasks.model().setData(notes_index, notes)
        self.table_current_tasks.model().submitAll()

    def _btn_complete_task_clicked(self):
        selected_cells = self.table_current_tasks.selectedIndexes()
        if len(selected_cells) == 0:
            QtWidgets.QMessageBox.information(self, 'Контроль задач', 'Выберите задачу')
            return

        selected_cell = selected_cells[0]
        self.table_current_tasks.model().setData(
            self.table_current_tasks.model().createIndex(selected_cell.row(), 5), 'completed')
        self.table_current_tasks.model().submitAll()
        self.table_completed_tasks.model().submitAll()

    def _table_current_tasks_double_clicked(self, index):
        self.show_task('Просмотр задачи', self.table_current_tasks, index)

    def _table_completed_tasks_double_clicked(self, index):
        self.show_task('Просмотр задачи', self.table_completed_tasks, index)

    def _btn_remove_completed_task_clicked(self):
        self.remove_task(self.table_completed_tasks)

    def _btn_clear_completed_tasks_clicked(self):
        rows_count = self.table_completed_tasks.model().rowCount()
        for row in range(rows_count - 1, -1, -1):
            self.table_completed_tasks.model().removeRow(row)
            self.table_completed_tasks.setRowHidden(row, True)
        self.table_completed_tasks.model().submitAll()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Контроль задач')

        column_id = 0
        column_status = 5

        lbl_current_tasks = QtWidgets.QLabel('Текущие задачи:')

        model_current_tasks = ColoredSqlTableModel()
        model_current_tasks.setTable('Task')
        model_current_tasks.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model_current_tasks.setFilter('status = "not completed" '
                                      'ORDER BY datetime(substr(period, 7, 4) || "-" || substr(period, 4, 2) '
                                      '|| "-" || substr(period, 1, 2) || " " || substr(period, 12, 8)) ASC')
        model_current_tasks.select()

        self.table_current_tasks = QtWidgets.QTableView()
        self.table_current_tasks.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.table_current_tasks.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_current_tasks.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.table_current_tasks.setModel(model_current_tasks)
        self.table_current_tasks.horizontalHeader().setMinimumSectionSize(150)
        self.table_current_tasks.setColumnWidth(1, 400)
        self.table_current_tasks.setHorizontalScrollMode(QtWidgets.QTableView.ScrollPerPixel)
        self.table_current_tasks.setVerticalScrollMode(QtWidgets.QTableView.ScrollPerPixel)

        self.table_current_tasks.doubleClicked.connect(self._table_current_tasks_double_clicked)

        model_current_tasks.setHeaderData(1, QtCore.Qt.Horizontal, "Задача")
        model_current_tasks.setHeaderData(2, QtCore.Qt.Horizontal, "Срок")
        model_current_tasks.setHeaderData(3, QtCore.Qt.Horizontal, "Ответственный")
        model_current_tasks.setHeaderData(4, QtCore.Qt.Horizontal, "Примечания")
        self.table_current_tasks.setColumnHidden(column_id, True)
        self.table_current_tasks.setColumnHidden(column_status, True)
        self.table_current_tasks.verticalHeader().setHidden(True)
        self.table_current_tasks.horizontalHeader().setStretchLastSection(True)

        btn_add_task = QtWidgets.QPushButton('Добавить')
        btn_remove_task = QtWidgets.QPushButton('Удалить')
        btn_edit_task = QtWidgets.QPushButton('Изменить')
        btn_complete_task = QtWidgets.QPushButton('Выполнено')
        btn_remove_completed_task = QtWidgets.QPushButton('Удалить')
        btn_clear_completed_tasks = QtWidgets.QPushButton('Очистить')

        btn_add_task.clicked.connect(self._btn_add_task_clicked)
        btn_remove_task.clicked.connect(self._btn_remove_task_clicked)
        btn_edit_task.clicked.connect(self._btn_edit_task_clicked)
        btn_complete_task.clicked.connect(self._btn_complete_task_clicked)
        btn_remove_completed_task.clicked.connect(self._btn_remove_completed_task_clicked)
        btn_clear_completed_tasks.clicked.connect(self._btn_clear_completed_tasks_clicked)

        layout_current_tasks_buttons = QtWidgets.QHBoxLayout()
        layout_current_tasks_buttons.setAlignment(QtCore.Qt.AlignLeft)
        layout_current_tasks_buttons.addWidget(lbl_current_tasks)
        layout_current_tasks_buttons.addWidget(btn_add_task)
        layout_current_tasks_buttons.addWidget(btn_remove_task)
        layout_current_tasks_buttons.addWidget(btn_edit_task)
        layout_current_tasks_buttons.addWidget(btn_complete_task)

        layout_current_tasks = QtWidgets.QVBoxLayout()
        layout_current_tasks.addLayout(layout_current_tasks_buttons)
        layout_current_tasks.addWidget(self.table_current_tasks)

        lbl_completed_tasks = QtWidgets.QLabel('Выполненные задачи:')

        model_completed_tasks = QtSql.QSqlTableModel()
        model_completed_tasks.setTable('Task')
        model_completed_tasks.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model_completed_tasks.setFilter('status = "completed" '
                                        'ORDER BY datetime(substr(period, 7, 4) || "-" || substr(period, 4, 2) '
                                        '|| "-" || substr(period, 1, 2) || " " || substr(period, 12, 8)) DESC')
        model_completed_tasks.select()

        self.table_completed_tasks = QtWidgets.QTableView()
        self.table_completed_tasks.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.table_completed_tasks.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_completed_tasks.setModel(model_completed_tasks)
        self.table_completed_tasks.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.table_completed_tasks.horizontalHeader().setMinimumSectionSize(150)
        self.table_completed_tasks.setColumnWidth(1, 400)
        self.table_completed_tasks.horizontalHeader().setStretchLastSection(True)
        self.table_completed_tasks.verticalHeader().setHidden(True)
        self.table_completed_tasks.setHorizontalScrollMode(QtWidgets.QTableView.ScrollPerPixel)
        self.table_completed_tasks.setVerticalScrollMode(QtWidgets.QTableView.ScrollPerPixel)

        self.table_completed_tasks.doubleClicked.connect(self._table_completed_tasks_double_clicked)

        model_completed_tasks.setHeaderData(1, QtCore.Qt.Horizontal, "Задача")
        model_completed_tasks.setHeaderData(2, QtCore.Qt.Horizontal, "Срок")
        model_completed_tasks.setHeaderData(3, QtCore.Qt.Horizontal, "Ответственный")
        model_completed_tasks.setHeaderData(4, QtCore.Qt.Horizontal, "Примечания")
        self.table_completed_tasks.setColumnHidden(column_id, True)
        self.table_completed_tasks.setColumnHidden(column_status, True)

        layout_completed_tasks_buttons = QtWidgets.QHBoxLayout()
        layout_completed_tasks_buttons.setAlignment(QtCore.Qt.AlignLeft)
        layout_completed_tasks_buttons.addWidget(lbl_completed_tasks)
        layout_completed_tasks_buttons.addWidget(btn_remove_completed_task)
        layout_completed_tasks_buttons.addWidget(btn_clear_completed_tasks)

        layout_completed_tasks = QtWidgets.QVBoxLayout()
        layout_completed_tasks.addLayout(layout_completed_tasks_buttons)
        layout_completed_tasks.addWidget(self.table_completed_tasks)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_current_tasks)
        layout_main.addLayout(layout_completed_tasks)

        self.setLayout(layout_main)
