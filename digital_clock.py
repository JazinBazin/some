from PyQt5 import QtWidgets, QtCore, QtGui


class DigitalClock(QtWidgets.QLCDNumber):
    def show_time(self):
        time = QtCore.QTime.currentTime()
        self.display(time.toString('hh:mm'))

    def __init__(self, width, height, border_color, digits_color, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Часы')
        self.setMaximumSize(width, height)
        self.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        palette = self.palette()
        palette.setColor(palette.Light, border_color)
        palette.setColor(palette.Dark, border_color)
        palette.setColor(palette.WindowText, digits_color)
        self.setPalette(palette)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)
        self.show_time()
