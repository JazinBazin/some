from PyQt5 import QtWidgets, QtGui, QtCore
from electronic_reception_widget import ElectronicReceptionWidget
from tasks_control_widget import TasksControlWidget
from events_widget import EventsWidget
from digital_clock import DigitalClock


class MainWindowWidget(QtWidgets.QWidget):

    def update_date(self):
        current_date = QtCore.QDate.currentDate()
        self.lbl_current_date.setText(current_date.toString(QtCore.Qt.DefaultLocaleLongDate))

    def __init__(self, parent=None):
        super().__init__(parent)
        background_color = QtGui.QColor(255, 255, 255)

        window_width = 1200
        window_height = 800
        header_height = 180
        calendar_width = 400
        clock_width = 250
        clock_height = 125
        clock_border_color = background_color
        clock_digits_color = QtGui.QColor(194, 13, 25)

        palette = self.palette()
        palette.setColor(palette.Background, background_color)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.setWindowTitle('Технополис ЭРА')
        self.setMinimumSize(window_width, window_height)
        self.setWindowIcon(QtGui.QIcon('logo_era.png'))

        electronic_reception = ElectronicReceptionWidget()
        tasks_control = TasksControlWidget()
        events_widget = EventsWidget()

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(electronic_reception, 'Электронная приёмная')
        tabs.addTab(tasks_control, 'Контроль задач')
        tabs.addTab(events_widget, 'Мероприятия')

        lbl_logo_era = QtWidgets.QLabel()
        logo = QtGui.QPixmap('logo_era_full.png')
        logo_scaled = logo.scaledToHeight(header_height)
        lbl_logo_era.setPixmap(logo_scaled)

        clock = DigitalClock(clock_width, clock_height, clock_border_color, clock_digits_color)

        calendar = QtWidgets.QCalendarWidget()
        calendar.setMaximumSize(calendar_width, header_height)
        calendar.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        calendar.setNavigationBarVisible(False)
        calendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)

        current_date = QtCore.QDate.currentDate()
        self.lbl_current_date = QtWidgets.QLabel(current_date.toString(QtCore.Qt.DefaultLocaleLongDate))
        self.lbl_current_date.setAlignment(QtCore.Qt.AlignRight)
        self.lbl_current_date.setFont(QtGui.QFont('Times', 20))
        palette = self.lbl_current_date.palette()
        palette.setColor(palette.Foreground, clock_digits_color)
        self.lbl_current_date.setPalette(palette)

        layout_logo = QtWidgets.QHBoxLayout()
        layout_logo.setAlignment(QtCore.Qt.AlignLeft)
        layout_logo.addWidget(lbl_logo_era)

        layout_clock_and_date = QtWidgets.QVBoxLayout()
        layout_clock_and_date.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        layout_clock_and_date.addWidget(clock)
        layout_clock_and_date.addWidget(self.lbl_current_date)

        layout_calendar_clock_date = QtWidgets.QHBoxLayout()
        layout_calendar_clock_date.setAlignment(QtCore.Qt.AlignRight)
        layout_calendar_clock_date.addLayout(layout_clock_and_date)
        layout_calendar_clock_date.addWidget(calendar)

        layout_header = QtWidgets.QHBoxLayout()
        layout_header.addLayout(layout_logo)
        layout_header.addLayout(layout_calendar_clock_date)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_header)
        layout_main.addWidget(tabs)

        self.setLayout(layout_main)

        self.timer_update_date = QtCore.QTimer()
        self.timer_update_date.timeout.connect(self.update_date)
        self.timer_update_date.start(5000)
