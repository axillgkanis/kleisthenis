import tkinter as tk
from tkinter import messagebox
import re

class PunishUserPopup(tk.Toplevel):
    def __init__(self, parent, on_submit=None):
        super().__init__(parent)
        self.title("Punish User")
        self.geometry("420x360")
        self.configure(bg="#1e1e1e")

        self.user_email = tk.StringVar()
        self.timeout_days = tk.StringVar()
        self.reason = tk.StringVar()
        self.on_submit = on_submit

        # Συνδέουμε τα πεδία με αλλαγή
        self.user_email.trace_add("write", self.check_fields)
        self.timeout_days.trace_add("write", self.check_fields)
        self.reason.trace_add("write", self.check_fields)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="LOGO", font=("Helvetica", 16, "bold"),
                 fg="white", bg="#1e1e1e").pack(pady=(20, 5))

        tk.Label(self, text="PUNISH USER", font=("Helvetica", 12, "bold"),
                 fg="white", bg="#1e1e1e").pack(pady=(0, 15))

        tk.Label(self, text="Timeout Period (days):", fg="white", bg="#1e1e1e").pack()
        tk.Entry(self, textvariable=self.timeout_days, width=30).pack(pady=(0, 10))

        tk.Label(self, text="Reason:", fg="white", bg="#1e1e1e").pack()
        tk.Entry(self, textvariable=self.reason, width=30).pack(pady=(0, 10))

        tk.Label(self, text="User Email:", fg="white", bg="#1e1e1e").pack()
        tk.Entry(self, textvariable=self.user_email, width=30).pack(pady=(0, 20))

        self.submit_button = tk.Button(
            self,
            text="SUBMIT",
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg="black",
            width=20,
            state="disabled",  # ξεκινά απενεργοποιημένο
            command=self.submit
        )
        self.submit_button.pack()

    def check_fields(self, *args):
        email = self.user_email.get().strip()
        days = self.timeout_days.get().strip()
        reason = self.reason.get().strip()

        if email and days and reason:
            self.submit_button.config(state="normal")
        else:
            self.submit_button.config(state="disabled")

    def submit(self):
        email = self.user_email.get().strip()
        days = self.timeout_days.get().strip()
        reason = self.reason.get().strip()

        if not days.isdigit() or int(days) <= 0:
            messagebox.showerror("Invalid Timeout", "Timeout must be a positive integer.")
            return

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$'
        if not re.match(pattern, email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        messagebox.showinfo("Punishment Saved", f"{email} punished for {days} days.")

        if self.on_submit:
            self.on_submit(email, int(days), reason)

        self.destroy()