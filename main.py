import sys
from PyQt5 import QtWidgets, QtSql
from main_window_widget import MainWindowWidget


def main():
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('era.db')
    db.open()
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    main_window = MainWindowWidget()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
