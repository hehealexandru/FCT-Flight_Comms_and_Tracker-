import os

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMessageBox
)
from PyQt6.QtWebEngineWidgets import QWebEngineView

from utils import check_rtlsdr_connection

class MapWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Harta Live Avioane")
        self.resize(1000, 700)

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        self.browser.load(QUrl("http://127.0.0.1:5000/"))

class SDRTrackerApp(QMainWindow):
    def __init__(self, dump_ctrl, server_ctrl):
        super().__init__()

        self.dump_ctrl = dump_ctrl
        self.server_ctrl = server_ctrl
        self.map_window: MapWindow | None = None
        self.timer: QTimer | None = None

        self.setWindowTitle("FCT (Flight Communications and Tracker)")
        self.resize(800, 600)
        self.setStyleSheet("background-color: #f5f5f5;")

        self.build_ui()
        self.start_status_timer()

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        logo = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "FCT.png")

        pix = QPixmap(logo_path)
        if not pix.isNull():
            pix = pix.scaled(
                280, 160,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo.setPixmap(pix)

        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)

        button_base = """
            QPushButton {
                border-radius: 10px;
                padding: 12px;
                font-size: 15px;
                font-weight: 500;
                color: white;
            }
            QPushButton:hover {
                filter: brightness(1.08);
            }
        """

        btn_dump = QPushButton("Pornește Dump1090")
        btn_dump.setStyleSheet(button_base + "QPushButton { background-color: #2196F3; }")
        btn_dump.clicked.connect(self.start_dump1090)
        layout.addWidget(btn_dump)

        btn_server = QPushButton("Pornește Server Flask")
        btn_server.setStyleSheet(button_base + "QPushButton { background-color: #2196F3; }")
        btn_server.clicked.connect(self.start_server)
        layout.addWidget(btn_server)

        btn_map = QPushButton("Afișează Harta Live")
        btn_map.setStyleSheet(button_base + "QPushButton { background-color: #4CAF50; }")
        btn_map.clicked.connect(self.show_map)
        layout.addWidget(btn_map)

        btn_close = QPushButton("Închide aplicația")
        btn_close.setStyleSheet(button_base + "QPushButton { background-color: #E53935; }")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

        status_layout = QHBoxLayout()
        status_layout.addStretch()

        self.rtlsdr_status_label = QLabel("RTL-SDR Lipsă")
        self.rtlsdr_status_label.setStyleSheet("color: #d32f2f; font-size: 12px;")
        status_layout.addWidget(self.rtlsdr_status_label)

        layout.addLayout(status_layout)

    def start_status_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rtlsdr_status)
        self.timer.start(1000)

    def update_rtlsdr_status(self):
        if check_rtlsdr_connection():
            self.rtlsdr_status_label.setText("RTL-SDR Conectat")
            self.rtlsdr_status_label.setStyleSheet("color: #388E3C; font-size: 12px;")
        else:
            self.rtlsdr_status_label.setText("RTL-SDR Lipsă")
            self.rtlsdr_status_label.setStyleSheet("color: #d32f2f; font-size: 12px;")

    def start_dump1090(self):
        result = self.dump_ctrl.start_dump1090()

        if result == "RUNNING":
            QMessageBox.warning(self, "Dump1090", "Dump1090 rulează deja!")
        elif result == "MISSING":
            QMessageBox.critical(
                self, "Dump1090",
                "Fișierul Dump1090 (.bat / .exe) nu există.\n"
                "Verifică calea din main.py."
            )
        elif result == "ERROR":
            QMessageBox.critical(self, "Dump1090", "Eroare la pornirea Dump1090!")
        # STARTED => nu afișăm nimic, exact cum ai cerut.

    def start_server(self):
        result = self.server_ctrl.start_server()

        if result == "RUNNING":
            QMessageBox.warning(self, "Server Flask", "Serverul Flask rulează deja!")
        elif result == "MISSING":
            QMessageBox.critical(
                self, "Server Flask",
                "Fișierul server.py nu există în folderul proiectului."
            )
        elif result == "ERROR":
            QMessageBox.critical(self, "Server Flask", "Eroare la pornirea serverului Flask!")

    def show_map(self):
        if not self.server_ctrl.is_running():
            QMessageBox.warning(
                self,
                "Harta Live",
                "Serverul Flask nu rulează.\nPornește mai întâi 'Pornește Server Flask'."
            )
            return

        if self.map_window is None:
            self.map_window = MapWindow(self)
        self.map_window.show()
        self.map_window.raise_()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Confirmare",
            "Vrei să închizi aplicația și să oprești toate procesele?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.timer is not None:
                    self.timer.stop()
            except Exception:
                pass

            try:
                self.dump_ctrl.stop_dump1090()
            except Exception:
                pass

            try:
                self.server_ctrl.stop_server()
            except Exception:
                pass

            QMessageBox.information(
                self,
                "Închidere",
                "Toate procesele au fost închise corect."
            )

            event.accept()
        else:
            event.ignore()
