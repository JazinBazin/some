from PyQt5 import QtWidgets, QtGui, QtCore
# from electronic_reception_widget import ElectronicReceptionWidget
from tasks_control_widget import TasksControlWidget
from events_widget import EventsWidget
from cards_deck_widget import CardsDeck
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
        header_height = 120
        clock_width = 200
        clock_height = header_height
        clock_border_color = background_color
        clock_digits_color = QtGui.QColor(194, 13, 25)

        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)

        palette = self.palette()
        palette.setColor(palette.Background, background_color)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.setWindowTitle('Технополис ЭРА')
        self.setMinimumSize(window_width, window_height)
        self.setWindowIcon(QtGui.QIcon('images/logo_era.ico'))

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(CardsDeck(photo_max_height=190, rows=2, columns=5), 'Электронная приёмная')
        # tabs.addTab(ElectronicReceptionWidget(), 'Электронная приёмная')
        tabs.addTab(TasksControlWidget(), 'Контроль задач')
        tabs.addTab(EventsWidget(), 'Мероприятия')

        lbl_logo_era = QtWidgets.QLabel()
        logo = QtGui.QPixmap('images/logo_era_full2.png')
        logo_scaled = logo.scaledToHeight(header_height)
        lbl_logo_era.setPixmap(logo_scaled)

        clock = DigitalClock(clock_width, clock_height, clock_border_color, clock_digits_color)

        current_date = QtCore.QDate.currentDate()
        self.lbl_current_date = QtWidgets.QLabel(current_date.toString(QtCore.Qt.DefaultLocaleLongDate))
        self.lbl_current_date.setAlignment(QtCore.Qt.AlignRight)
        self.lbl_current_date.setFont(QtGui.QFont('Courier New', 20))
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

        layout_header = QtWidgets.QHBoxLayout()
        layout_header.setAlignment(QtCore.Qt.AlignTop)
        layout_header.addLayout(layout_logo)
        layout_header.addLayout(layout_calendar_clock_date)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_header)
        layout_main.addWidget(tabs)

        self.setLayout(layout_main)

        self.timer_update_date = QtCore.QTimer()
        self.timer_update_date.timeout.connect(self.update_date)
        self.timer_update_date.start(5000)

# from electronic_reception_widget import ElectronicReceptionWidget
# electronic_reception = ElectronicReceptionWidget()

# background = QtGui.QPixmap('background.png')
# palette = self.palette()
# palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(background))
# self.setPalette(palette)

# calendar_width = 400
# calendar = QtWidgets.QCalendarWidget()
# calendar.setMaximumSize(calendar_width, header_height)
# calendar.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
# calendar.setNavigationBarVisible(False)
# calendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
# calendar.setStyleSheet('border-color')
# layout_calendar_clock_date.addLayout(layout_clock_and_date)
