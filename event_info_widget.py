from PyQt5 import QtWidgets, QtGui, QtCore


class EventInfoWidget(QtWidgets.QDialog):
    def __init__(self, headline, parent=None):
        super().__init__(parent)
        self.setWindowTitle(headline)
        self.setWindowIcon(QtGui.QIcon('logo_era.png'))

        lbl_event_name = QtWidgets.QLabel('Мероприятие:')
        lbl_event_date = QtWidgets.QLabel('Дата:')
        lbl_event_time = QtWidgets.QLabel('Время:')
        lbl_responsible = QtWidgets.QLabel('Кто привлекается:')

        self.line_event_name = QtWidgets.QLineEdit()
        self.date_event = QtWidgets.QDateEdit()
        self.time_event = QtWidgets.QTimeEdit()


