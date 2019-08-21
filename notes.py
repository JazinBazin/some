# self.model.insertRows(self.model.rowCount(), 1)
# last_row = self.model.rowCount() - 1
# self.model.setData(self.model.createIndex(last_row, 1), description)
# self.model.setData(self.model.createIndex(last_row, 2),
#                    date_time.toString('dd-MM-yyyy HH:mm:ss'))
# self.model.setData(self.model.createIndex(last_row, 3), responsible)
# self.model.setData(self.model.createIndex(last_row - 1, 4), notes)
# self.model.submitAll()

# record = self.model.record()
# record.setValue('description', description)
# record.setValue('period', date_time.toString('dd-MM-yyyy HH:mm:ss'))
# record.setValue('responsible', responsible)
# record.setValue('notes', notes)
# if not self.model.insertRecord(-1, record):
#     QtWidgets.QMessageBox.critical(None, 'Контроль задач',
#                                    'Не удалось добавить запись в базу данных')
# else:
#     last_id = self.model.query().lastInsertId()
#
#     self.model.selectRow(last_id)

# date_time = QtCore.QDateTime(period_date, period_time)
# command = 'insert into Task\n' \
#           '(description, period, responsible, notes)\n' \
#           'values\n' \
#           '("' + description + '", "' \
#           + date_time.toString('dd-MM-yyyy HH:mm:ss') + '", "' \
#           + responsible + '", "' \
#           + notes + '");'
# query = QtSql.QSqlQuery()
# query.exec(command)
# task_id = query.lastInsertId()

# def showEvent(self, event):
#     self.table_current_tasks.resizeRowsToContents()
#     self.table_current_tasks.resizeColumnsToContents()
# self.table_current_tasks.horizontalHeader().setStretchLastSection(True)

# self.table_current_tasks.setWordWrap(True)
# self.table_current_tasks.setTextElideMode(QtCore.Qt.ElideNone)

# self.model.removeRow(selected_cell.row())
# self.model.submitAll()
# self.table_current_tasks.setRowHidden(selected_cell.row(), True)
# self.table_current_tasks.model().removeRow(selected_cell.row())
# self.table_current_tasks.model().submitAll()
# self.table_current_tasks.setRowHidden(selected_cell.row(), True)

# class MultiLineCellDelegate(QtWidgets.QItemDelegate):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.document = QtWidgets.QTextEdit()
#
#     def paint(self, painter, option, index):
#         self.document.setHtml(index.data(QtCore.Qt.DisplayRole))
#         self.document.adjustSize()
#         self.document.drawContents(painter)
#
#     def sizeHint(self, option, index):
#         self.document.setHtml(index.data())
#         self.document.adjustSize()
#         return self.document.size().toSize()


#self.table_current_tasks.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)