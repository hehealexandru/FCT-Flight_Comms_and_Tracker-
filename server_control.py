import os
import sys
import subprocess
class ServerController:

    def __init__(self, server_script: str):
        self.server_script = server_script
        self.server_process: subprocess.Popen | None = None

    def start_server(self) -> str:
        if not os.path.exists(self.server_script):
            return "MISSING"
        if self.server_process is not None and self.server_process.poll() is None:
            return "RUNNING"
        try:
            python_exe = sys.executable
            self.server_process = subprocess.Popen(
                [python_exe, self.server_script],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            return "STARTED"
        except Exception:
            return "ERROR"

    def stop_server(self) -> None:
        if self.server_process is not None and self.server_process.poll() is None:
            try:
                subprocess.call(
                    ["taskkill", "/F", "/T", "/PID", str(self.server_process.pid)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                pass

        self.server_process = None

    def is_running(self) -> bool:
        return self.server_process is not None and self.server_process.poll() is None
