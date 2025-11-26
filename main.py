import sys
import os

from PyQt6.QtWidgets import QApplication

from dump1090_control import Dump1090Controller
from server_control import ServerController
from gui_qt import SDRTrackerApp


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QMessageBox {
            background-color: white;
        }

        QMessageBox QLabel {
            color: black;
            font-size: 14px;
        }

        QMessageBox QPushButton {
            background-color: #e0e0e0;
            color: black;
            border-radius: 6px;
            padding: 6px 12px;
            min-width: 80px;
            font-size: 13px;
        }

        QMessageBox QPushButton:hover {
            background-color: #d5d5d5;
        }
    """)
    base_dir = os.path.abspath(os.path.dirname(__file__))

    dump1090_path = r"C:\Users\alexc\Desktop\projects\Dump1090-main\run-dump1090-SBS.bat"
    server_script = os.path.join(base_dir, "server.py")

    dump_ctrl = Dump1090Controller(dump1090_path)
    server_ctrl = ServerController(server_script)

    window = SDRTrackerApp(dump_ctrl, server_ctrl)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
