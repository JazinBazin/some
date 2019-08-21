from PyQt5 import QtWidgets, QtGui, QtCore


class TaskWidget(QtWidgets.QDialog):
    signal_save_task = QtCore.pyqtSignal(QtCore.QDate, QtCore.QTime, str, str, str)

    def _btn_save_task_clicked(self):
        if self.date_task.date() < QtCore.QDate.currentDate():
            QtWidgets.QMessageBox.information(self, 'Контроль задач', 'Дата не может быть меньше текущей')
            return
        if self.date_task.date() == QtCore.QDate.currentDate() and \
                self.time_task.time() < QtCore.QTime.currentTime():
            QtWidgets.QMessageBox.information(self, 'Контроль задач', 'Время не может быть меньше текущего')
            return
        if len(self.line_responsible.text()) == 0:
            QtWidgets.QMessageBox.information(self, 'Контроль задач', 'Заполните поле "Ответственный"')
            return
        if len(self.text_description.toPlainText()) == 0:
            QtWidgets.QMessageBox.information(self, 'Контроль задач', 'Заполните поле "Описание задачи"')
            return
        self.signal_save_task.emit(self.date_task.date(), self.time_task.time(), self.line_responsible.text(),
                                   self.text_description.toPlainText(), self.text_notes.toPlainText())
        self.close()

    def _btn_cancel_task_clicked(self):
        self.close()

    def __init__(self, headline, date_init=QtCore.QDate.currentDate(),
                 time_init=QtCore.QTime.currentTime(), responsible_init='',
                 description_init='', notes_init='', parent=None):
        super().__init__(parent)
        self.setWindowTitle(headline)
        self.setWindowIcon(QtGui.QIcon('logo_era.png'))

        lbl_period_date = QtWidgets.QLabel('Дата:')
        lbl_period_time = QtWidgets.QLabel('Время:')
        lbl_responsible = QtWidgets.QLabel('Ответственный:')
        lbl_description = QtWidgets.QLabel('Описание задачи:')
        lbl_notes = QtWidgets.QLabel('Примечания:')

        self.date_task = QtWidgets.QDateEdit()
        self.time_task = QtWidgets.QTimeEdit()
        self.line_responsible = QtWidgets.QLineEdit()
        self.text_description = QtWidgets.QTextEdit()
        self.text_notes = QtWidgets.QTextEdit()

        self.date_task.setDate(date_init)
        self.time_task.setTime(time_init)
        self.line_responsible.setText(responsible_init)
        self.text_description.setText(description_init)
        self.text_notes.setText(notes_init)

        btn_save_task = QtWidgets.QPushButton('Сохранить')
        btn_cancel_task = QtWidgets.QPushButton('Отмена')

        btn_save_task.clicked.connect(self._btn_save_task_clicked)
        btn_cancel_task.clicked.connect(self._btn_cancel_task_clicked)

        layout_data = QtWidgets.QFormLayout()
        layout_data.addRow(lbl_period_date, self.date_task)
        layout_data.addRow(lbl_period_time, self.time_task)
        layout_data.addRow(lbl_responsible, self.line_responsible)
        layout_data.addRow(lbl_description, self.text_description)
        layout_data.addRow(lbl_notes, self.text_notes)

        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.setAlignment(QtCore.Qt.AlignRight)
        layout_buttons.addWidget(btn_save_task)
        layout_buttons.addWidget(btn_cancel_task)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_data)
        layout_main.addLayout(layout_buttons)

        self.setLayout(layout_main)
