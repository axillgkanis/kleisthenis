import customtkinter as ctk
import json
import os

DATA_FILE = "announcements.json"

class AnnouncementPopup(ctk.CTkToplevel):
    def __init__(self, parent, mode="create", index=None, data=None):
        super().__init__(parent)
        self.title("Announcement")
        self.geometry("400x400")
        self.configure(fg_color="#fef9ff")

        self.mode = mode
        self.index = index
        self.data = data or {}

        ctk.CTkLabel(self, text="LOGO", font=("Arial", 16, "bold"), text_color="#0f172a").pack(pady=(10, 5))

        ctk.CTkLabel(self, text="Announcement Title", font=("Arial", 12)).pack(pady=(10, 2))
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Enter title")
        self.title_entry.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Announcement Body", font=("Arial", 12)).pack(pady=(15, 2))
        self.body_text = ctk.CTkTextbox(self, height=150)
        self.body_text.pack(padx=20, fill="both", expand=True)

        if self.mode == "edit" and self.data:
            self.title_entry.insert(0, self.data.get("title", ""))
            self.body_text.insert("0.0", self.data.get("body", ""))

        ctk.CTkButton(self, text="Submit", command=self.save_announcement).pack(pady=10)

    def save_announcement(self):
        title = self.title_entry.get().strip()
        body = self.body_text.get("0.0", "end").strip()

        if not title:
            ctk.CTkLabel(self, text="Title is required", text_color="red").pack()
            return

        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        new_entry = {"title": title, "body": body}

        if self.mode == "edit" and self.index is not None:
            data[self.index] = new_entry
        else:
            data.append(new_entry)

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        self.destroy()