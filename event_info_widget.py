from PyQt5 import QtWidgets, QtGui, QtCore


class EventInfoWidget(QtWidgets.QDialog):
    signal_save_event = QtCore.pyqtSignal(str, QtCore.QDate, QtCore.QTime, str)

    def _btn_save_event_clicked(self):
        if len(self.line_event_name.text()) == 0:
            QtWidgets.QMessageBox.information(self, 'Мероприятия', 'Заполните поле "Мероприятие"')
            return
        if self.date_event.date() < QtCore.QDate.currentDate():
            QtWidgets.QMessageBox.information(self, 'Мероприятия', 'Дата не может быть меньше текущей')
            return
        if self.date_event.date() == QtCore.QDate.currentDate() and \
                self.time_event.time() < QtCore.QTime.currentTime():
            QtWidgets.QMessageBox.information(self, 'Мероприятия', 'Время не может быть меньше текущего')
            return
        self.signal_save_event.emit(self.line_event_name.text(), self.date_event.date(),
                                    self.time_event.time(), self.text_responsible.toPlainText())
        self.close()

    def _btn_cancel_event_clicked(self):
        self.close()

    def __init__(self, headline, name_init='', date_init=QtCore.QDate.currentDate(),
                 time_init=QtCore.QTime.currentTime(), responsible_init='',
                 save_button_enabled=True, parent=None):
        super().__init__(parent)
        self.setWindowTitle(headline)
        self.setWindowIcon(QtGui.QIcon('images/logo_era.png'))
        self.setWindowFlags(self.windowFlags() & (~QtCore.Qt.WindowContextHelpButtonHint))

        lbl_event_name = QtWidgets.QLabel('Мероприятие:')
        lbl_event_date = QtWidgets.QLabel('Дата:')
        lbl_event_time = QtWidgets.QLabel('Время:')
        lbl_responsible = QtWidgets.QLabel('Кто привлекается:')

        self.line_event_name = QtWidgets.QLineEdit()
        self.date_event = QtWidgets.QDateEdit()
        self.time_event = QtWidgets.QTimeEdit()
        self.text_responsible = QtWidgets.QTextEdit()

        self.line_event_name.setText(name_init)
        self.date_event.setDate(date_init)
        self.time_event.setTime(time_init)
        self.text_responsible.setText(responsible_init)

        btn_save_event = QtWidgets.QPushButton('Сохранить')
        btn_save_event.setEnabled(save_button_enabled)
        btn_cancel_event = QtWidgets.QPushButton('Отмена')

        btn_save_event.clicked.connect(self._btn_save_event_clicked)
        btn_cancel_event.clicked.connect(self._btn_cancel_event_clicked)

        layout_data = QtWidgets.QFormLayout()
        layout_data.addRow(lbl_event_name, self.line_event_name)
        layout_data.addRow(lbl_event_date, self.date_event)
        layout_data.addRow(lbl_event_time, self.time_event)
        layout_data.addRow(lbl_responsible, self.text_responsible)

        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.setAlignment(QtCore.Qt.AlignRight)
        layout_buttons.addWidget(btn_save_event)
        layout_buttons.addWidget(btn_cancel_event)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_data)
        layout_main.addLayout(layout_buttons)

        self.setLayout(layout_main)
