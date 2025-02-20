import subprocess

dump1090_path = r"C:\Users\alexc\Desktop\projects\Dump1090-main\dump1090.exe"
output_folder = r"C:\Users\alexc\Desktop\projects\Dump1090-main"

try:
    subprocess.Popen(
        [dump1090_path, "--interactive", "--net", "--write-json", output_folder],
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    print("Dump1090 a fost pornit cu succes!")
except Exception as e:
    print(f"Eroare la pornirea Dump1090: {e}")
