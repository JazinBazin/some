from PyQt5 import QtWidgets, QtSql
from card_widget import CardWidget


class CardsDeck(QtWidgets.QWidget):

    @staticmethod
    def _load_data():
        query = QtSql.QSqlQuery()
        query.exec("SELECT number, name, status FROM Card;")
        data = {}
        while query.next():
            data[query.value(0)] = (query.value(1), query.value(2))
        return data

    def __init__(self, photo_max_height, rows=2, columns=4, parent=None):
        super().__init__(parent)

        layout_main = QtWidgets.QVBoxLayout()
        data = CardsDeck._load_data()
        for i in range(rows):
            layout_row = QtWidgets.QHBoxLayout()
            for j in range(columns):
                card_id = columns * i + j
                layout_row.addWidget(CardWidget(card_id=card_id, photo_max_height=photo_max_height,
                                                user_name=data[card_id][0], status=data[card_id][1]))
            layout_main.addLayout(layout_row)

        self.setLayout(layout_main)
