# screens/propose_frame.py
import tkinter as tk

def show_popup():
    top = tk.Toplevel()
    top.title("Propose New Frame")
    top.geometry("400x300")
    top.configure(bg="#fdf2f8")  # pastel pink background

    tk.Label(top, text="Frame Title:", font=("Helvetica", 12, "bold"),
             bg="#fdf2f8").pack(pady=(20, 5))
    title_entry = tk.Entry(top, width=40, font=("Helvetica", 11))
    title_entry.pack(pady=5)

    tk.Label(top, text="Frame Description:", font=("Helvetica", 12),
             bg="#fdf2f8").pack(pady=(15, 5))
    desc_text = tk.Text(top, height=6, width=40, font=("Helvetica", 10))
    desc_text.pack()

    tk.Button(top, text="Submit", font=("Helvetica", 11, "bold"),
              bg="#93c5fd", fg="#0f172a",
              command=lambda: print("Submitted")).pack(pady=15)