import customtkinter as ctk
from tkinter import filedialog
import os
import json

class ProposeFramePopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Propose Frame")
        self.geometry("400x400")
        self.configure(fg_color="#fef9ff")

        self.pdf_path = None

        # --- Logo
        ctk.CTkLabel(self, text="LOGO", font=("Arial", 18, "bold")).pack(pady=(10, 5))

        # --- Frame Title
        ctk.CTkLabel(self, text="Frame Title", font=("Arial", 12)).pack(pady=(10, 2))
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Enter title here")
        self.title_entry.pack(padx=20, fill="x")

        # --- Description or PDF
        ctk.CTkLabel(self, text="Description / PDF", font=("Arial", 12)).pack(pady=(15, 5))

        self.desc_text = ctk.CTkTextbox(self, height=100)
        self.desc_text.insert("0.0", "Type your frame here or select PDF.")
        self.desc_text.pack(padx=20, fill="both")

        ctk.CTkButton(self, text="📎 Select PDF", command=self.select_pdf).pack(pady=(10, 5))

        # --- Submit
        ctk.CTkButton(self, text="Submit", command=self.submit_frame).pack(pady=(10, 5))

    def select_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.pdf_path = path
            self.desc_text.delete("0.0", "end")
            self.desc_text.insert("0.0", f"📎 {os.path.basename(path)}")

    def submit_frame(self):
        title = self.title_entry.get().strip()
        description = self.desc_text.get("0.0", "end").strip()

        if not title:
            ctk.CTkLabel(self, text="Title is required", text_color="red").pack()
            return

        new_frame = {
            "title": title,
            "description": description if not self.pdf_path else "",
            "pdf_file": self.pdf_path if self.pdf_path else None,
            "status": "pending"
        }

        try:
            if os.path.exists("proposed_frames.json"):
                with open("proposed_frames.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = []

            data.append(new_frame)

            with open("proposed_frames.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            self.destroy()

        except Exception as e:
            ctk.CTkLabel(self, text=f"Error: {e}", text_color="red").pack()