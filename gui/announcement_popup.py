import customtkinter as ctk
from classes.announcementHandler import announcementHandler


class ANNOUNCEMENT_CREATION_SCREEN(ctk.CTkToplevel):
    def __init__(self, parent, mode="create", index=None, data=None):
        super().__init__(parent)
        self.title("Δημιουργία Ανακοίνωσης")
        self.geometry("400x400")
        self.configure(fg_color="#fef9ff")

        self.mode = mode
        self.index = index
        self.data = data or {}

        ctk.CTkLabel(self, text="Τίτλος Ανακοίνωσης",
                     font=("Arial", 12)).pack(pady=(10, 2))
        self.title_entry = ctk.CTkEntry(
            self, placeholder_text="Εισάγετε τίτλο")
        self.title_entry.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Σώμα Ανακοίνωσης",
                     font=("Arial", 12)).pack(pady=(15, 2))
        self.body_text = ctk.CTkTextbox(self, height=150)
        self.body_text.pack(padx=20, fill="both", expand=True)

        if self.mode == "edit" and self.data:
            self.title_entry.insert(0, self.data.get("title", ""))
            self.body_text.insert("0.0", self.data.get("body", ""))

        self.submit_button = ctk.CTkButton(self, text="Υποβολή",
                                           command=self.submit_announcement,
                                           state="disabled")

        self.submit_button.pack(pady=10)

        # Add bindings for text changes
        self.title_entry.bind('<KeyRelease>', self.enableSubmit)
        self.body_text.bind('<KeyRelease>', self.enableSubmit)

    def displayCreateAnnouncement(parent):
        popup = ANNOUNCEMENT_CREATION_SCREEN(parent, mode="create")
        parent.wait_window(popup)
        parent.refresh_list()

    # Validates inputs and enables/disables submit button
    def enableSubmit(self, event=None):
        title = self.title_entry.get().strip()
        body = self.body_text.get("0.0", "end").strip()

        if title and body:
            self.submit_button.configure(state="normal")
        else:
            self.submit_button.configure(state="disabled")

    # helper function that handles the actual submission of the announcement
    def submit_announcement(self):
        title = self.title_entry.get().strip()
        body = self.body_text.get("0.0", "end").strip()

        announcement_data = {
            "title": title,
            "body": body
        }

        handler = announcementHandler(announcement_data)
        if handler.newAnnouncement():
            self.destroy()
        else:
            ctk.CTkLabel(
                self, text="Αδυναμία αποθήκευσης ανακοίνωσης", text_color="red").pack()


class EDIT_ANNOUNCEMENT_SCREEN(ctk.CTkToplevel):
    def __init__(self, parent, mode="create", index=None, data=None):
        super().__init__(parent)
        self.title("Εοεξεργασία Ανακοίνωσης")
        self.geometry("400x400")
        self.configure(fg_color="#fef9ff")

        self.mode = mode
        self.index = index
        self.data = data or {}

        ctk.CTkLabel(self, text="Τίτλος Ανακοίνωσης",
                     font=("Arial", 12)).pack(pady=(10, 2))
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Enter title")
        self.title_entry.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Σώμα Ανακοίνωσης",
                     font=("Arial", 12)).pack(pady=(15, 2))
        self.body_text = ctk.CTkTextbox(self, height=150)
        self.body_text.pack(padx=20, fill="both", expand=True)

        if self.mode == "edit" and self.data:
            self.title_entry.insert(0, self.data.get("title", ""))
            self.body_text.insert("0.0", self.data.get("body", ""))

        self.submit_button = ctk.CTkButton(self, text="Υποβολή",
                                           command=self.submit_announcement,
                                           state="disabled")

        self.submit_button.pack(pady=10)

        # Add bindings for text changes
        self.title_entry.bind('<KeyRelease>', self.enableSubmit)
        self.body_text.bind('<KeyRelease>', self.enableSubmit)

    def displayEditAnnouncement(parent, index, data):
        popup = EDIT_ANNOUNCEMENT_SCREEN(
            parent, mode="edit", index=index, data=data)
        parent.wait_window(popup)
        parent.refresh_list()
        # parent.show_announcement(index)

    # Validates inputs and enables/disables submit button
    def enableSubmit(self, event=None):
        title = self.title_entry.get().strip()
        body = self.body_text.get("0.0", "end").strip()

        if title and body:
            self.submit_button.configure(state="normal")
        else:
            self.submit_button.configure(state="disabled")

    # helper function that handles the actual submission of the announcement
    def submit_announcement(self):
        title = self.title_entry.get().strip()
        body = self.body_text.get("0.0", "end").strip()

        announcement_data = {
            # Add the id from the existing announcement
            "id": self.data.get("id"),
            "title": title,
            "body": body
        }

        handler = announcementHandler(announcement_data)
        if handler.editAnnouncement():
            self.destroy()
        else:
            ctk.CTkLabel(
                self, text="Αδυναμία αποθήκευσης ανακοίνωσης", text_color="red").pack()
