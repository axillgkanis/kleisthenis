import tkinter as tk
from dialog_screens.Login import LoginScreen
from home_screen import KleisthenisDashboard


def launch_dashboard():
    root.destroy()
    KleisthenisDashboard().mainloop()

root = tk.Tk()
root.title("Σύνδεση")
root.geometry("1000x700")

login = LoginScreen(root, on_submit_callback=launch_dashboard)
login.pack(fill="both", expand=True)

root.mainloop()