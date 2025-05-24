import tkinter as tk
from tkinter import messagebox


class AuthenticationFrame(tk.Frame):
    def __init__(self, parent, on_success):
        super().__init__(parent, bg="#1e1e1e")
        self.on_success = on_success
        self.otp_code = tk.StringVar()
        self.create_widgets()
        self.otp_code.trace_add("write", self.check_valid)

        

    def create_widgets(self):

        tk.Label(self, text="AUTHENTICATION", font=("Helvetica", 12, "bold"),
                 fg="white", bg="#1e1e1e").pack(pady=(0, 5))

        tk.Label(self, text="Enter the OTP sent to your email", font=("Helvetica", 10),
                 fg="white", bg="#1e1e1e").pack(pady=(0, 20))

        self.otp_entry = tk.Entry(self, textvariable=self.otp_code, width=30, fg="grey")
        self.otp_entry.insert(0, "Enter OTP code")
        self.otp_entry.bind("<FocusIn>", self.clear_placeholder)
        self.otp_entry.bind("<FocusOut>", self.restore_placeholder)
        self.otp_entry.pack(pady=(0, 20))

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
        self.submit_button.pack()

    def clear_placeholder(self, event):
        if self.otp_entry.get() == "Enter OTP code":
            self.otp_entry.delete(0, tk.END)
            self.otp_entry.config(fg="white")

    def restore_placeholder(self, event):
        if not self.otp_entry.get():
            self.otp_entry.insert(0, "Enter OTP code")
            self.otp_entry.config(fg="grey")
            self.submit_button.config(state="disabled")

    def check_valid(self, *args):
        otp = self.otp_code.get()
        if otp.strip() and otp != "Enter OTP code":
            self.submit_button.config(state="normal")
        else:
            self.submit_button.config(state="disabled")

    def submit(self):
        otp = self.otp_code.get()
        if otp == "Enter OTP code" or not otp.strip():
            messagebox.showwarning("Missing OTP", "Please enter the OTP code.")
            return

        messagebox.showinfo("Submitted", f"OTP Entered: {otp}")
        if self.on_success:
            self.on_success()