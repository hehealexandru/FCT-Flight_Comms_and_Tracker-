import subprocess
import os

class ServerController:
    def __init__(self, server_script):
        self.server_script = server_script
        self.server_process = None

    def start_server(self):
        if self.server_process is not None and self.server_process.poll() is None:
            return "Serverul rulează deja!"
        try:
            self.server_process = subprocess.Popen(
                ["python", self.server_script], creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            return "Serverul Flask a fost pornit!"
        except Exception as e:
            return f"Eroare la pornirea serverului Flask: {e}"

    def stop_server(self):
        try:
            if self.server_process is not None and self.server_process.poll() is None:
                subprocess.call(["taskkill", "/F", "/T", "/PID", str(self.server_process.pid)])
                return "Serverul a fost oprit."
        except Exception as e:
            return f"Eroare la oprirea serverului: {e}"

    def is_running(self):
        return self.server_process is not None and self.server_process.poll() is None