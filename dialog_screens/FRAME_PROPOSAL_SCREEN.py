import customtkinter as ctk
from tkinter import filedialog
from dialog_screens.frameManager import frameManager
from dialog_screens.DIALOGUE_SCREEN import DIALOGUE


class FRAME_PROPOSAL_SCREEN(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Πρόταση Πλαισίου")
        self.geometry("400x400")
        self.configure(fg_color="#fef9ff")

        self.pdf_path = None

        # --- Frame Title
        ctk.CTkLabel(self, text="Τίτλος Πλαισίου",
                     font=("Arial", 12)).pack(pady=(10, 2))
        self.title_entry = ctk.CTkEntry(
            self, placeholder_text="Εισαγωγή τίτλου")
        self.title_entry.pack(padx=20, fill="x")

        # --- Description or PDF
        ctk.CTkLabel(self, text="Description / PDF",
                     font=("Arial", 12)).pack(pady=(15, 5))

        self.desc_text = ctk.CTkTextbox(self, height=100)
        self.desc_text.insert(
            "0.0", "Πληκτρολόγησε το πλαίσιο εδώ ή επέλεξε αρχείο.")
        self.desc_text.pack(padx=20, fill="both")

        ctk.CTkButton(self, text="📎 Επέλεξε αρχείο",
                      command=self.select_pdf).pack(pady=(10, 5))

        # --- Submit
        self.submit_button = ctk.CTkButton(
            self, text="Υποβολή", command=self.submit_frame, state="disabled")
        self.submit_button.pack(pady=(10, 5))

        # Add bindings for text changes
        self.title_entry.bind('<KeyRelease>', self.enableSubmit)
        self.desc_text.bind('<KeyRelease>', self.enableSubmit)

    def enableSubmit(self, event=None):
        title = self.title_entry.get().strip()
        description = self.desc_text.get("0.0", "end").strip()

        if title and description:
            self.submit_button.configure(state="normal")
        else:
            self.submit_button.configure(state="disabled")

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
            ctk.CTkLabel(self, text="Απαιτήται τίτλος",
                         text_color="red").pack()
            return

        try:
            # Create instance of frameManager
            manager = frameManager()

            # Call proposeNewFramework method to save to database
            result = manager.proposeFramework(title, description)

            if result:
                self.destroy()
                DIALOGUE().displaySuccess("Το πλαίσιο προτάθηκε με επιτυχία!")
            else:
                ctk.CTkLabel(
                    self, text="Αδυναμία αποθήκευσης πλαισίου", text_color="red").pack()

        except Exception as e:
            ctk.CTkLabel(self, text=f"Σφάλμα: {e}", text_color="red").pack()
