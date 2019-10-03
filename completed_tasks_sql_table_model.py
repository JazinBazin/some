from PyQt5 import QtCore, QtSql, QtGui


class CompletedTasksSqlTableModel(QtSql.QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.BackgroundRole:
            return QtGui.QBrush(QtGui.QColor(13, 194, 67))
        else:
            return super().data(index, role)
