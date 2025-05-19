import tkinter as tk
from tkinter import messagebox, ttk

class SetEmailRegexPopup(tk.Toplevel):
    def __init__(self, parent, on_submit=None):
        super().__init__(parent)
        self.title("Set Email Regex")
        self.geometry("420x300")
        self.configure(bg="#1e1e1e")

        self.username = tk.StringVar()
        self.domain = tk.StringVar()
        self.tld = tk.StringVar()
        self.tld.set("com")  # default επιλογή

        self.on_submit = on_submit

        # Συνδέουμε trace για ενεργοποίηση του κουμπιού
        self.username.trace_add("write", self.check_fields)
        self.domain.trace_add("write", self.check_fields)
        self.tld.trace_add("write", self.check_fields)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="LOGO", font=("Helvetica", 16, "bold"),
                 fg="white", bg="#1e1e1e").pack(pady=(20, 5))

        tk.Label(self, text="SET EMAIL REGEX", font=("Helvetica", 12, "bold"),
                 fg="white", bg="#1e1e1e").pack(pady=(0, 15))

        frame = tk.Frame(self, bg="#1e1e1e")
        frame.pack(pady=(0, 20))

        # Email μορφή: username @ domain . [dropdown]
        tk.Entry(frame, textvariable=self.username, width=10).pack(side="left", padx=3)
        tk.Label(frame, text="@", fg="white", bg="#1e1e1e").pack(side="left", padx=3)
        tk.Entry(frame, textvariable=self.domain, width=10).pack(side="left", padx=3)
        tk.Label(frame, text=".", fg="white", bg="#1e1e1e").pack(side="left", padx=3)
        ttk.Combobox(frame, textvariable=self.tld, values=["com", "gr", "co", "org"], width=5).pack(side="left", padx=3)

        self.submit_button = tk.Button(
            self,
            text="SUBMIT",
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg="black",
            width=20,
            command=self.submit,
            state="disabled"  # αρχικά ανενεργό
        )
        self.submit_button.pack()

    def check_fields(self, *args):
        if self.username.get().strip() and self.domain.get().strip() and self.tld.get().strip():
            self.submit_button.config(state="normal")
        else:
            self.submit_button.config(state="disabled")

    def submit(self):
        user = self.username.get().strip()
        dom = self.domain.get().strip()
        tld = self.tld.get().strip()

        email = f"{user}@{dom}.{tld}"

        messagebox.showinfo("Regex Set", f"Email set to: {email}")

        if self.on_submit:
            self.on_submit(email)

        self.destroy()