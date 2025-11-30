import sys
import os

from PyQt6.QtWidgets import QApplication

from dump1090_control import Dump1090Controller
from server_control import ServerController
from gui_qt import SDRTrackerApp


def main():
    app = QApplication(sys.argv)

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
