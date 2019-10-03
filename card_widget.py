from PyQt5 import QtWidgets, QtCore, QtSql, QtGui
from user_photo import UserPhoto
from card_request import CardRequest


class CardWidget(QtWidgets.QWidget):

    @staticmethod
    def _set_font_size(element, font_size):
        font = element.font()
        font.setPointSize(font_size)
        element.setFont(font)

    def _btn_accept_clicked(self):
        if len(self.btn_user_name.text()) != 0:
            query = QtSql.QSqlQuery()
            query.exec("UPDATE Card SET status = 'accepted' WHERE number = '" + str(self.card_id) + "';")
            self.user_photo.set_accepted(True)

    def _btn_cancel_clicked(self):
        if len(self.btn_user_name.text()) != 0:
            query = QtSql.QSqlQuery()
            query.exec("UPDATE Card SET status = 'rejected' WHERE number = '" + str(self.card_id) + "';")
            self.user_photo.set_accepted(False)

    def _btn_add_request_clicked(self):
        request = CardRequest()
        request.signal_save_request.connect(self.slot_add_request)
        request.exec()

    def slot_add_request(self, user_name):
        query = QtSql.QSqlQuery()
        query.exec("UPDATE Card SET name = '" + user_name +
                   "' WHERE number = '" + str(self.card_id) + "';")
        self.btn_user_name.setText(user_name)
        self.btn_user_name.setEnabled(True)
        self.user_photo.set_photo(QtGui.QPixmap('images/no_photo.png'))

    def _btn_remove_request_clicked(self):
        query = QtSql.QSqlQuery()
        query.exec("UPDATE Card SET name = '', status = 'none' WHERE number = '" + str(self.card_id) + "';")
        self.user_photo.set_default()
        self.btn_user_name.setText('')
        self.btn_user_name.setEnabled(False)

    def __init__(self, card_id, photo_max_height, user_name='', status='none', user_photo=None, parent=None):
        super().__init__(parent)

        self.card_id = card_id

        self.user_photo = UserPhoto(photo_max_height, user_photo)
        self.user_photo.signal_clicked.connect(self._btn_add_request_clicked)

        self.btn_user_name = QtWidgets.QPushButton(user_name)
        CardWidget._set_font_size(self.btn_user_name, 12)
        self.btn_user_name.setFlat(True)
        self.btn_user_name.clicked.connect(self._btn_remove_request_clicked)

        if user_name:
            self.btn_user_name.setText(user_name)
            if user_photo:
                self.user_photo.set_photo(user_photo)
            else:
                self.user_photo.set_photo(QtGui.QPixmap('images/no_photo.png'))
        else:
            self.btn_user_name.setEnabled(False)
            self.user_photo.set_default()

        if status != 'none':
            self.user_photo.set_accepted(status == 'accepted')

        btn_accept_request = QtWidgets.QPushButton('Принять')
        btn_accept_request.setFlat(True)
        btn_cancel_request = QtWidgets.QPushButton('Отклонить')
        btn_cancel_request.setFlat(True)

        CardWidget._set_font_size(btn_accept_request, 12)
        CardWidget._set_font_size(btn_cancel_request, 12)

        btn_accept_request.setStyleSheet('color: #0dc243;')
        btn_cancel_request.setStyleSheet('color: #c20d19;')

        btn_accept_request.clicked.connect(self._btn_accept_clicked)
        btn_cancel_request.clicked.connect(self._btn_cancel_clicked)

        layout_user_name_button = QtWidgets.QHBoxLayout()
        layout_user_name_button.setAlignment(QtCore.Qt.AlignCenter)
        layout_user_name_button.addWidget(self.btn_user_name)

        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.setAlignment(QtCore.Qt.AlignJustify)
        layout_buttons.addWidget(btn_accept_request)
        layout_buttons.addWidget(btn_cancel_request)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_buttons)
        layout_main.addWidget(self.user_photo)
        layout_main.addLayout(layout_user_name_button)
        layout_main.setAlignment(QtCore.Qt.AlignTop)

        self.setLayout(layout_main)
