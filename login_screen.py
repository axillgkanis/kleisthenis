import tkinter as tk
from dialog_screens.Login import LOG_IN_SCREEN
from home_screen import INITIAL_SCREEN


def launch_dashboard():
    root.destroy()
    INITIAL_SCREEN().mainloop()


root = tk.Tk()
root.title("Σύνδεση")
root.geometry("1000x700")

login = LOG_IN_SCREEN(root, on_submit_callback=launch_dashboard)
login.pack(fill="both", expand=True)

root.mainloop()
