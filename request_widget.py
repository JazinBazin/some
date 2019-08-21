from PyQt5 import QtWidgets, QtGui, QtCore


class RequestWidget(QtWidgets.QDialog):
    signal_save_request = QtCore.pyqtSignal(str, str, str, QtCore.QDate, QtCore.QTime, str)

    def _btn_save_request_clicked(self):
        if len(self.line_family_name.text()) == 0:
            QtWidgets.QMessageBox.information(self, 'Электронная приёмная', 'Заполните поле "Фамилия"')
            return
        if self.date_request.date() < QtCore.QDate.currentDate():
            QtWidgets.QMessageBox.information(self, 'Электронная приёмная', 'Дата не может быть меньше текущей')
            return
        if self.date_request.date() == QtCore.QDate.currentDate() and \
                self.time_request.time() < QtCore.QTime.currentTime():
            QtWidgets.QMessageBox.information(self, 'Электронная приёмная', 'Время не может быть меньше текущего')
            return
        self.signal_save_request.emit(self.line_family_name.text(), self.line_name.text(),
                                      self.line_surname.text(), self.date_request.date(),
                                      self.time_request.time(), self.text_reason.toPlainText())
        self.close()

    def _btn_cancel_request_clicked(self):
        self.close()

    def __init__(self, headline, family_name_init='', name_init='', surname_init='',
                 date_request_init=QtCore.QDate.currentDate(),
                 time_request_init=QtCore.QTime.currentTime(),
                 reason_init='', parent=None):
        super().__init__(parent)
        self.setWindowTitle(headline)
        self.setWindowIcon(QtGui.QIcon('logo_era.png'))

        lbl_family_name = QtWidgets.QLabel('Фамилия:')
        lbl_name = QtWidgets.QLabel('Имя:')
        lbl_surname = QtWidgets.QLabel('Отчество:')
        lbl_request_date = QtWidgets.QLabel('Дата визита:')
        lbl_request_time = QtWidgets.QLabel('Время визита:')
        lbl_reason = QtWidgets.QLabel('Причина визита:')

        self.line_family_name = QtWidgets.QLineEdit()
        self.line_name = QtWidgets.QLineEdit()
        self.line_surname = QtWidgets.QLineEdit()
        self.date_request = QtWidgets.QDateEdit()
        self.time_request = QtWidgets.QTimeEdit()
        self.text_reason = QtWidgets.QTextEdit()

        self.line_family_name.setText(family_name_init)
        self.line_name.setText(name_init)
        self.line_surname.setText(surname_init)
        self.date_request.setDate(date_request_init)
        self.time_request.setTime(time_request_init)
        self.text_reason.setText(reason_init)

        btn_save_request = QtWidgets.QPushButton('Сохранить')
        btn_cancel_request = QtWidgets.QPushButton('Отмена')

        btn_save_request.clicked.connect(self._btn_save_request_clicked)
        btn_cancel_request.clicked.connect(self._btn_cancel_request_clicked)

        layout_data = QtWidgets.QFormLayout()
        layout_data.addRow(lbl_family_name, self.line_family_name)
        layout_data.addRow(lbl_name, self.line_name)
        layout_data.addRow(lbl_surname, self.line_surname)
        layout_data.addRow(lbl_request_date, self.date_request)
        layout_data.addRow(lbl_request_time, self.time_request)
        layout_data.addRow(lbl_reason, self.text_reason)

        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.setAlignment(QtCore.Qt.AlignRight)
        layout_buttons.addWidget(btn_save_request)
        layout_buttons.addWidget(btn_cancel_request)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_data)
        layout_main.addLayout(layout_buttons)

        self.setLayout(layout_main)
