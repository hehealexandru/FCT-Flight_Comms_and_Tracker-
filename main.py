import os
import tkinter as tk
from gui import SDRTrackerApp
from server_control import ServerController
from dump1090_control import Dump1090Controller

def main():
    root = tk.Tk()

    base_dir = os.path.abspath(os.path.dirname(__file__))
    dump1090_path = r"C:\Users\alexc\Desktop\projects\Dump1090-main\run-dump1090-SBS.bat"
    server_script = os.path.join(base_dir, "server.py")

    dump1090_controller = Dump1090Controller(dump1090_path)
    server_controller = ServerController(server_script)

    app = SDRTrackerApp(root, dump1090_controller, server_controller)
    root.mainloop()

if __name__ == "__main__":
    main()
