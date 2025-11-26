import os
import subprocess


class Dump1090Controller:
    """
    Controlează procesul Dump1090 (pornește / oprește).
    Returnează coduri simple:
        - "STARTED"  – pornit cu succes
        - "RUNNING"  – era deja pornit
        - "MISSING"  – fișierul .bat / .exe nu există
        - "ERROR"    – altă eroare la pornire
    """

    def __init__(self, dump1090_path: str):
        self.dump1090_path = dump1090_path
        self.dump1090_process: subprocess.Popen | None = None

    def start_dump1090(self) -> str:
        if not os.path.exists(self.dump1090_path):
            return "MISSING"

        if self.dump1090_process is not None and self.dump1090_process.poll() is None:
            return "RUNNING"

        try:
            self.dump1090_process = subprocess.Popen(
                [self.dump1090_path],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            return "STARTED"
        except Exception:
            return "ERROR"

    def stop_dump1090(self) -> None:
        """Oprește procesul Dump1090 dacă este pornit."""
        if self.dump1090_process is not None and self.dump1090_process.poll() is None:
            try:
                subprocess.call(
                    ["taskkill", "/F", "/T", "/PID", str(self.dump1090_process.pid)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                pass

        self.dump1090_process = None

    def is_running(self) -> bool:
        return self.dump1090_process is not None and self.dump1090_process.poll() is None
