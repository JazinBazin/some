from PyQt5 import QtCore, QtSql, QtGui


class ColoredSqlTableModel(QtSql.QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.BackgroundRole:
            date_time_index = index.model().createIndex(index.row(), 2)
            task_date_time = QtCore.QDateTime.fromString(index.model().data(date_time_index), 'dd-MM-yyyy HH:mm:ss')
            current_date_time = QtCore.QDateTime.currentDateTime()
            if current_date_time.daysTo(task_date_time) < 1:
                return QtGui.QBrush(QtGui.QColor(255, 0, 0))
            elif current_date_time.daysTo(task_date_time) < 2:
                return QtGui.QBrush(QtGui.QColor(255, 255, 0))
            else:
                return QtGui.QBrush(QtGui.QColor(255, 255, 255))
        else:
            return super().data(index, role)
