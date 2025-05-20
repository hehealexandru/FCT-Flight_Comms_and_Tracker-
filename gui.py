import os
import webbrowser
import tkinter as tk
from tkinter import messagebox, CENTER
from ttkbootstrap import Button, Label
from PIL import Image, ImageTk
from gui_style import apply_style
from utils import check_rtlsdr_connection
from dump1090_control import Dump1090Controller
from server_control import ServerController


class SDRTrackerApp:
    def __init__(self, root, dump1090_controller, server_controller):
        self.root = root
        self.style = apply_style(self.root)
        self.root.title("FCT (Flight Communications and Tracker)")
        self.root.geometry("800x600")

        self.dump1090_controller = dump1090_controller
        self.server_controller = server_controller
        self.update_task = None

        self.create_widgets()
        self.update_rtlsdr_status()

    def update_rtlsdr_status(self):
        if check_rtlsdr_connection():
            self.rtlsdr_status_label.config(text="RTL-SDR Conectat", bootstyle="success")
        else:
            self.rtlsdr_status_label.config(text="RTL-SDR Lipsă", bootstyle="danger")
        self.update_task = self.root.after(1000, self.update_rtlsdr_status)

    def start_dump1090(self):
        msg = self.dump1090_controller.start_dump1090()
        messagebox.showinfo("Info", msg)

    def start_server(self):
        msg = self.server_controller.start_server()
        messagebox.showinfo("Info", msg)

    def generate_map(self):
        try:
            webbrowser.open("https://127.0.0.1:5000/")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la deschiderea hărții: {e}")

    def close_application(self):
        try:
            if self.update_task:
                self.root.after_cancel(self.update_task)
            self.dump1090_controller.stop_dump1090()
            self.server_controller.stop_server()
            messagebox.showinfo("Info", "Toate procesele au fost închise!")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la închiderea aplicației: {e}")
        finally:
            self.root.destroy()

    def create_widgets(self):

        logo_path = os.path.join(os.path.dirname(__file__), "FCT.png")
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((300, 175))
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            self.logo_label = tk.Label(self.root, image=self.logo_photo, bg="white")
            self.logo_label.place(relx=0.53, rely=0.15, anchor="center")

        Button(self.root, text="Pornește Dump1090", command=self.start_dump1090,
               width=40, bootstyle="info", padding=(0, 10)).place(relx=0.5, rely=0.35, anchor=CENTER)

        Button(self.root, text="Pornește Server Flask", command=self.start_server,
               width=40, bootstyle="info", padding=(0, 10)).place(relx=0.5, rely=0.45, anchor=CENTER)

        Button(self.root, text="Afișează Harta Live", command=self.generate_map,
               width=40, bootstyle="success", padding=(0, 10)).place(relx=0.5, rely=0.55, anchor=CENTER)

        Button(self.root, text="Închide aplicația", command=self.close_application,
               width=40, bootstyle="danger", padding=(0, 10)).place(relx=0.5, rely=0.65, anchor=CENTER)

        # === STATUS RTL-SDR ===
        self.rtlsdr_status_label = Label(self.root, text="Verificare RTL-SDR...", bootstyle="warning", font=("Helvetica", 12))
        self.rtlsdr_status_label.place(relx=0.98, rely=0.98, anchor="se")
