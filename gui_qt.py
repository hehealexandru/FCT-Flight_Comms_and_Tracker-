import os

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMessageBox
)
from PyQt6.QtWebEngineWidgets import QWebEngineView

from gui_style import (
    button_class_blue, button_class_green,
    button_class_red, GLOBAL_STYLES
)

from utils import check_rtlsdr_connection


class MessageBoxNoX(QMessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint
        )


class MapWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Live Map")
        self.resize(1000, 700)
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.browser.load(QUrl("http://127.0.0.1:5000/"))


class SDRTrackerApp(QMainWindow):
    def __init__(self, dump_ctrl, server_ctrl):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint |
            Qt.WindowType.WindowMinimizeButtonHint
        )

        self.setWindowIcon(QIcon("FCT_white_minilogo.png"))

        self.dump_ctrl = dump_ctrl
        self.server_ctrl = server_ctrl
        self.map_window = None
        self.timer = None

        self.setWindowTitle("Flight Communications and Tracker")
        self.resize(900, 650)
        self.setFixedSize(900, 650)

        self.build_ui()

        self.setStyleSheet(GLOBAL_STYLES)

        self.start_status_timer()

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(40, 30, 40, 20)
        layout.setSpacing(25)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.logo_label = QLabel()
        pix = QPixmap("FCT.png")
        pix = pix.scaled(300, 160, Qt.AspectRatioMode.KeepAspectRatio,
                         Qt.TransformationMode.SmoothTransformation)
        self.logo_label.setPixmap(pix)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)

        btn_dump = QPushButton("Start Dump1090")
        btn_dump.setProperty("class", button_class_blue)
        btn_dump.clicked.connect(self.start_dump1090)
        layout.addWidget(btn_dump)

        btn_server = QPushButton("Start Server Flask")
        btn_server.setProperty("class", button_class_blue)
        btn_server.clicked.connect(self.start_server)
        layout.addWidget(btn_server)

        btn_map = QPushButton("Show Live Map")
        btn_map.setProperty("class", button_class_green)
        btn_map.clicked.connect(self.show_map)
        layout.addWidget(btn_map)

        btn_close = QPushButton("Close App")
        btn_close.setProperty("class", button_class_red)
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

        status_layout = QHBoxLayout()
        status_layout.addStretch()

        self.rtlsdr_status_label = QLabel("RTL-SDR Missing")
        self.rtlsdr_status_label.setObjectName("statusLabel")
        status_layout.addWidget(self.rtlsdr_status_label)

        layout.addLayout(status_layout)

    def start_status_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rtlsdr_status)
        self.timer.start(1000)

    def update_rtlsdr_status(self):
        if check_rtlsdr_connection():
            self.rtlsdr_status_label.setText("RTL-SDR Connected")
            self.rtlsdr_status_label.setProperty("status", "ok")
        else:
            self.rtlsdr_status_label.setText("RTL-SDR Missing")
            self.rtlsdr_status_label.setProperty("status", "bad")

        self.rtlsdr_status_label.style().unpolish(self.rtlsdr_status_label)
        self.rtlsdr_status_label.style().polish(self.rtlsdr_status_label)

    def msg(self, title, text, icon):
        box = MessageBoxNoX(self)
        box.setWindowTitle(title)
        box.setText(text)
        box.setIcon(icon)
        box.setStandardButtons(QMessageBox.StandardButton.Ok)
        box.exec()

    def start_dump1090(self):
        result = self.dump_ctrl.start_dump1090()
        if result == "RUNNING":
            self.msg("Dump1090", "Dump1090 is already running!", QMessageBox.Icon.Warning)
        elif result == "MISSING":
            self.msg("Dump1090", "The file Dump1090 does not exist..", QMessageBox.Icon.Critical)
        elif result == "ERROR":
            self.msg("Dump1090", "Error starting Dump1090!", QMessageBox.Icon.Critical)

    def start_server(self):
        result = self.server_ctrl.start_server()
        if result == "RUNNING":
            self.msg("Flask Server", "Serverul Flask is already running!", QMessageBox.Icon.Warning)
        elif result == "MISSING":
            self.msg("Flask Server", "The file server.py does not exist", QMessageBox.Icon.Critical)
        elif result == "ERROR":
            self.msg("Flask Server", "Error starting Flask server!", QMessageBox.Icon.Critical)

    def show_map(self):
        if not self.server_ctrl.is_running():
            self.msg("Live Map",
                "The Flask server is not running. Start it first.",
                QMessageBox.Icon.Warning)
            return

        if self.map_window is None:
            self.map_window = MapWindow(self)

        self.map_window.show()
        self.map_window.raise_()

    def closeEvent(self, event):
        box = MessageBoxNoX(self)
        box.setWindowTitle("Confirm")
        box.setText("Do you want to close the application and stop all processes?")
        box.setIcon(QMessageBox.Icon.Question)
        box.setStandardButtons(
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        reply = box.exec()

        if reply == QMessageBox.StandardButton.Yes:
            if self.timer:
                self.timer.stop()

            self.dump_ctrl.stop_dump1090()
            self.server_ctrl.stop_server()

            okmsg = MessageBoxNoX(self)
            okmsg.setWindowTitle("Closing")
            okmsg.setText("All processes have been closed.")
            okmsg.setIcon(QMessageBox.Icon.Information)
            okmsg.setStandardButtons(QMessageBox.StandardButton.Ok)
            okmsg.exec()

            event.accept()
        else:
            event.ignore()
