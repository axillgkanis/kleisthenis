import tkinter as tk
from tkinter import messagebox

class LoginScreen(tk.Frame):
    def __init__(self, parent, on_submit_callback=None):
        super().__init__(parent, bg="#1e1e1e")
        self.parent = parent
        self.on_submit_callback = on_submit_callback

        self.is_admin = tk.BooleanVar()
        self.email = tk.StringVar()
        self.admin_code = tk.StringVar()
        self.show_password = False  # αρχική κατάσταση: κωδικός κρυφός

        # Παρακολούθηση αλλαγής στο email
        self.email.trace_add("write", self.on_email_change)

        self.create_widgets()

    def create_widgets(self):
        # Logo και τίτλος
        tk.Label(self, text="LOGO", font=("Helvetica", 16, "bold"), fg="white", bg="#1e1e1e").pack(pady=(30, 10))
        tk.Label(self, text="LOGIN", font=("Helvetica", 12, "bold"), fg="white", bg="#1e1e1e").pack(pady=(0, 10))

        # Πεδίο Email
        tk.Label(self, text="email:", fg="white", bg="#1e1e1e").pack()
        tk.Entry(self, textvariable=self.email, width=30).pack(pady=(0, 10))

        # Επιλογή Admin
        tk.Checkbutton(self, text="Are you an admin?", variable=self.is_admin,
                       command=self.toggle_admin_entry, fg="white", bg="#1e1e1e",
                       selectcolor="#1e1e1e").pack(pady=5)

        # Frame για admin code + μάτι
        self.admin_frame = tk.Frame(self, bg="#1e1e1e")
        self.admin_entry = tk.Entry(self.admin_frame, textvariable=self.admin_code, width=25, show="*")
        self.admin_entry.pack(side="left", padx=(0, 5))

        self.eye_button = tk.Button(
            self.admin_frame,
            text="👁️",
            command=self.toggle_password_visibility,
            bg="white",
            fg="black",
            width=2
        )
        self.eye_button.pack(side="left")

        # Submit κουμπί (disabled από την αρχή)
        self.submit_button = tk.Button(
            self,
            text="SUBMIT",
            command=self.submit,
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg="black",
            width=20,
            state="disabled"
        )
        self.submit_button.pack(pady=30)

    def toggle_admin_entry(self):
        if self.is_admin.get():
            self.admin_frame.pack(pady=(10, 0))
            self.admin_frame.pack(before=self.submit_button)
        else:
            self.admin_frame.pack_forget()

    def toggle_password_visibility(self):
        if self.show_password:
            self.admin_entry.config(show="*")
            self.eye_button.config(text="👁️")
        else:
            self.admin_entry.config(show="")
            self.eye_button.config(text="❌")
        self.show_password = not self.show_password

    def on_email_change(self, *args):
        if self.email.get().strip():
            self.submit_button.config(state="normal")
        else:
            self.submit_button.config(state="disabled")

    def submit(self):
        email = self.email.get()
        is_admin = self.is_admin.get()
        code = self.admin_code.get() if is_admin else None

        msg = f"Email: {email}\nAdmin: {is_admin}"
        if is_admin:
            msg += f"\nCode: {code}"

        messagebox.showinfo("Submitted", msg)

        if self.on_submit_callback:
            self.on_submit_callback()