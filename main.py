import os
import subprocess
import requests
import webbrowser
import tkinter as tk
from tkinter import Tk, messagebox, Button, Label, CENTER, Toplevel
from tkinterweb import HtmlFrame

base_dir = os.path.abspath(os.path.dirname(__file__))
dump1090_path = r"C:\Users\alexc\Desktop\projects\Dump1090-main\run-dump1090-SBS.bat"
server_script = os.path.join(base_dir, "server.py")
dump1090_process = None
server_process = None
update_task = None
selected_airport = None

def check_rtlsdr_connection():
    try:
        result = subprocess.Popen(["rtl_test", "-t"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = result.communicate(timeout=3)
        return "No supported devices found" not in stderr
    except Exception:
        return False

def update_rtlsdr_status():
    global update_task
    if check_rtlsdr_connection():
        rtlsdr_status_label.config(text="RTL-SDR Conectat", fg="green")
    else:
        rtlsdr_status_label.config(text="RTL-SDR Lipsă", fg="red")
    update_task = root.after(1000, update_rtlsdr_status)

def start_dump1090():
    global dump1090_process
    if dump1090_process is not None and dump1090_process.poll() is None:
        messagebox.showwarning("Avertisment", "Dump1090 rulează deja!")
        return
    try:
        dump1090_process = subprocess.Popen([dump1090_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        messagebox.showinfo("Info", "Dump1090 a fost pornit!")
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la pornirea Dump1090: {e}")

def start_server():
    global server_process
    if server_process is not None and server_process.poll() is None:
        messagebox.showwarning("Avertisment", "Serverul rulează deja!")
        return
    try:
        server_process = subprocess.Popen(["python", server_script], creationflags=subprocess.CREATE_NEW_CONSOLE)
        messagebox.showinfo("Info", "Serverul Flask a fost pornit!")
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la pornirea serverului Flask: {e}")

def generate_map():
    try:
        webbrowser.open("https://127.0.0.1:5000/")
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la deschiderea hărții: {e}")

def close_application():
    global dump1090_process, server_process, update_task
    try:
        if update_task:
            root.after_cancel(update_task)
        if dump1090_process is not None and dump1090_process.poll() is None:
            subprocess.call(["taskkill", "/F", "/T", "/PID", str(dump1090_process.pid)])
        if server_process is not None and server_process.poll() is None:
            subprocess.call(["taskkill", "/F", "/T", "/PID", str(server_process.pid)])

        messagebox.showinfo("Info", "Toate procesele au fost închise!")
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la închiderea aplicației: {e}")
    finally:
        root.destroy()

def create_gui():
    global root, rtlsdr_status_label
    root = Tk()
    root.title("FCT (Flight Communications and Tracker)")
    root.geometry("800x600")

    Button(root, text="Pornește Dump1090", command=start_dump1090, width=40, height=3).place(relx=0.5, rely=0.25, anchor=CENTER)
    Button(root, text="Pornește Server Flask", command=start_server, width=40, height=3).place(relx=0.5, rely=0.35, anchor=CENTER)
    Button(root, text="Afișează Harta Live", command=generate_map, width=40, height=3).place(relx=0.5, rely=0.45, anchor=CENTER)
    Button(root, text="Închide aplicația", command=close_application, width=40, height=3).place(relx=0.5, rely=0.55, anchor=CENTER)

    rtlsdr_status_label = Label(root, text="Verificare RTL-SDR...", fg="blue", font=("Helvetica", 12))
    rtlsdr_status_label.place(relx=0.98, rely=0.98, anchor="se")

    update_rtlsdr_status()
    root.mainloop()

if __name__ == "__main__":
    create_gui()
