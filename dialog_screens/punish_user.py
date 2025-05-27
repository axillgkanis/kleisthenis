import tkinter as tk
from tkinter import messagebox
import re

class PunishUserPopup(tk.Toplevel):
    def __init__(self, parent, on_submit=None):
        super().__init__(parent)
        self.title("Ορισμός Ποινής Χρήστη")
        self.geometry("420x360")
        self.configure(bg="#1e1e1e")

        self.user_email = tk.StringVar()
        self.timeout_days = tk.StringVar()
        self.reason = tk.StringVar()
        self.on_submit = on_submit

        
        self.user_email.trace_add("write", self.check_fields)
        self.timeout_days.trace_add("write", self.check_fields)
        self.reason.trace_add("write", self.check_fields)

        self.create_widgets()

    def create_widgets(self):
        
        tk.Label(self, text="ΟΡΙΣΜΟΣ ΠΟΙΝΗΣ ΧΡΗΣΤΗ", font=("Helvetica", 12, "bold"),
                 fg="white", bg="#1e1e1e").pack(pady=(40, 20))

        tk.Label(self, text="Χρονική Περίοδος Διακοπής (Μέρες):", fg="white", bg="#1e1e1e").pack()
        tk.Entry(self, textvariable=self.timeout_days, width=30).pack(pady=(0, 15))

        tk.Label(self, text="Αιτιολογία:", fg="white", bg="#1e1e1e").pack()
        tk.Entry(self, textvariable=self.reason, width=30).pack(pady=(0, 10))

        tk.Label(self, text="Email Χρήστη:", fg="white", bg="#1e1e1e").pack()
        tk.Entry(self, textvariable=self.user_email, width=30).pack(pady=(0, 20))

        self.submit_button = tk.Button(
            self,
            text="Υποβολή",
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg="black",
            width=20,
            state="disabled", 
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
            messagebox.showerror("Λάθος περίοδος", "Η περίοδος διακοπής πρέπει να είναι θετικός ακέραιος.")
            return

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$'
        if not re.match(pattern, email):
            messagebox.showerror("Λάθος Email", "Εισάγετε σωστή διεύθυνδη email.")
            return

        messagebox.showinfo("Αποθηκεύτηκε η ποινή", f"{email} απαγορεύτηκε για {days} μέρες.")

        if self.on_submit:
            self.on_submit(email, int(days), reason)

        self.destroy()