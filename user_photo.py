from PyQt5 import QtWidgets, QtGui, QtCore


class UserPhoto(QtWidgets.QLabel):
    signal_clicked = QtCore.pyqtSignal()

    def __init__(self, photo_max_height, user_photo=None, parent=None):
        super().__init__(parent)
        self.photo_height = photo_max_height

        if user_photo is None:
            user_photo = QtGui.QPixmap('images/default_photo.png')

        self.source_photo = user_photo.scaledToHeight(self.photo_height)
        self.setPixmap(self.source_photo)
        self.setAlignment(QtCore.Qt.AlignCenter)

    def _draw_image(self, image):
        photo = self.source_photo.copy(QtCore.QRect(0, 0, self.source_photo.width(), self.source_photo.height()))
        painter = QtGui.QPainter(photo)
        top_left_x = (photo.width() - image.width()) / 2
        top_left_y = (photo.height() - image.height()) / 2
        painter.drawImage(QtCore.QRect(top_left_x, top_left_y, image.width(), image.height()), image)
        painter.end()
        self.setPixmap(photo)

    def set_accepted(self, accept):
        if accept:
            self._draw_image(QtGui.QImage('images/accepted_small.png'))
        else:
            self._draw_image(QtGui.QImage('images/cancel_small.png'))

    def set_photo(self, photo):
        self.source_photo = photo.scaledToHeight(self.photo_height)
        self.setPixmap(self.source_photo)

    def set_default(self):
        user_photo = QtGui.QPixmap('images/default_photo.png')
        self.source_photo = user_photo.scaledToHeight(self.photo_height)
        self.setPixmap(self.source_photo)

    def mousePressEvent(self, event):
        self.signal_clicked.emit()
