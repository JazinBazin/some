from PyQt5 import QtWidgets, QtGui, QtCore
from electronic_reception_widget import ElectronicReceptionWidget
from tasks_control_widget import TasksControlWidget
from digital_clock import DigitalClock


class MainWindowWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        window_width = 1200
        window_height = 800
        header_height = 180
        calendar_width = 400
        clock_width = 250
        clock_height = 125
        clock_border_color = QtGui.QColor(255, 255, 255)
        clock_digits_color = QtGui.QColor(194, 13, 25)

        self.setWindowTitle('Технополис ЭРА')
        self.setMinimumSize(window_width, window_height)
        self.setWindowIcon(QtGui.QIcon('logo_era.png'))

        electronic_reception = ElectronicReceptionWidget()
        tasks_control = TasksControlWidget()

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(electronic_reception, 'Электронная приёмная')
        tabs.addTab(tasks_control, 'Контроль задач')

        lbl_logo_era = QtWidgets.QLabel()
        logo = QtGui.QPixmap('logo_era_full.png')
        logo_scaled = logo.scaledToHeight(header_height)
        lbl_logo_era.setPixmap(logo_scaled)

        clock = DigitalClock(clock_width, clock_height, clock_border_color, clock_digits_color)

        calendar = QtWidgets.QCalendarWidget()
        calendar.setMaximumSize(calendar_width, header_height)
        calendar.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        calendar.setNavigationBarVisible(False)

        layout_logo = QtWidgets.QHBoxLayout()
        layout_logo.setAlignment(QtCore.Qt.AlignLeft)
        layout_logo.addWidget(lbl_logo_era)

        layout_calendar_and_clock = QtWidgets.QHBoxLayout()
        layout_calendar_and_clock.setAlignment(QtCore.Qt.AlignRight)
        layout_calendar_and_clock.addWidget(clock)
        layout_calendar_and_clock.addWidget(calendar)

        layout_header = QtWidgets.QHBoxLayout()
        layout_header.addLayout(layout_logo)
        layout_header.addLayout(layout_calendar_and_clock)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_header)
        layout_main.addWidget(tabs)

        self.setLayout(layout_main)
