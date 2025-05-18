import tkinter as tk
from dialog_screens.Login import LoginScreen

def dummy_submit():
    print("✅ Login υποβλήθηκε (δοκιμαστικά)")

root = tk.Tk()
root.title("Test LoginScreen")
root.geometry("600x400")

login = LoginScreen(root, on_submit_callback=dummy_submit)
login.pack(fill="both", expand=True)

root.mainloop()