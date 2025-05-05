import subprocess

def check_rtlsdr_connection():

    try:
        result = subprocess.Popen(["rtl_test", "-t"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = result.communicate(timeout=3)
        return "No supported devices found" not in stderr
    except Exception:
        return False
