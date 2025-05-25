import customtkinter as ctk
from tkinter import filedialog
import os
import json

class ProposeFramePopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Πρόταση Πλαισίου")
        self.geometry("400x400")
        self.configure(fg_color="#fef9ff")

        self.pdf_path = None


        # --- Frame Title
        ctk.CTkLabel(self, text="Τίτλος Πλαισίου", font=("Arial", 12)).pack(pady=(10, 2))
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Εισαγωγή τίτλου")
        self.title_entry.pack(padx=20, fill="x")

        # --- Description or PDF
        ctk.CTkLabel(self, text="Description / PDF", font=("Arial", 12)).pack(pady=(15, 5))

        self.desc_text = ctk.CTkTextbox(self, height=100)
        self.desc_text.insert("0.0", "Πληκτρολόγησε το πλαίσιο εδώ ή επέλεξε αρχείο.")
        self.desc_text.pack(padx=20, fill="both")

        ctk.CTkButton(self, text="📎 Επέλεξε αρχείο", command=self.select_pdf).pack(pady=(10, 5))

        # --- Submit
        ctk.CTkButton(self, text="Υποβολή", command=self.submit_frame).pack(pady=(10, 5))

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
            ctk.CTkLabel(self, text="Απαιτήται τίτλος", text_color="red").pack()
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
            ctk.CTkLabel(self, text=f"Σφάλμα: {e}", text_color="red").pack()