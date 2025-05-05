import subprocess

class Dump1090Controller:
    def __init__(self, dump1090_path):
        self.dump1090_path = dump1090_path
        self.dump1090_process = None

    def start_dump1090(self):
        if self.dump1090_process is not None and self.dump1090_process.poll() is None:
            return "Dump1090 rulează deja!"
        try:
            self.dump1090_process = subprocess.Popen([self.dump1090_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            return "Dump1090 a fost pornit!"
        except Exception as e:
            return f"Eroare la pornirea Dump1090: {e}"

    def stop_dump1090(self):
        try:
            if self.dump1090_process is not None and self.dump1090_process.poll() is None:
                subprocess.call(["taskkill", "/F", "/T", "/PID", str(self.dump1090_process.pid)])
                return "Dump1090 a fost oprit."
        except Exception as e:
            return f"Eroare la oprirea Dump1090: {e}"
