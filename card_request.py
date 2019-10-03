from PyQt5 import QtWidgets, QtGui, QtCore


class CardRequest(QtWidgets.QDialog):
    signal_save_request = QtCore.pyqtSignal(str)

    def _btn_add_request_clicked(self):
        if len(self.line_name.text()) == 0:
            QtWidgets.QMessageBox.information(self, 'Электронная приёмная', 'Заполните поле "Имя"')
            return
        self.close()
        self.signal_save_request.emit(self.line_name.text())

    def _btn_cancel_clicked(self):
        self.close()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Создать заявку")
        self.setWindowIcon(QtGui.QIcon('images/logo_era.png'))
        self.setWindowFlags(self.windowFlags() & (~QtCore.Qt.WindowContextHelpButtonHint))

        lbl_name = QtWidgets.QLabel('Имя:')
        self.line_name = QtWidgets.QLineEdit()
        btn_add_request = QtWidgets.QPushButton('Добавить')
        btn_cancel = QtWidgets.QPushButton('Отмена')

        btn_add_request.clicked.connect(self._btn_add_request_clicked)
        btn_cancel.clicked.connect(self._btn_cancel_clicked)

        layout_name = QtWidgets.QHBoxLayout()
        layout_name.addWidget(lbl_name)
        layout_name.addWidget(self.line_name)

        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.addWidget(btn_add_request)
        layout_buttons.addWidget(btn_cancel)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_name)
        layout_main.addLayout(layout_buttons)

        self.setLayout(layout_main)
