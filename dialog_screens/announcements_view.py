import customtkinter as ctk
import json
import os
from dialog_screen.announcement_popup import AnnouncementPopup

DATA_FILE = "announcements.json"

class AnnouncementsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.announcements = []
        self.selected_index = None

        ctk.CTkLabel(self, text="Announcements", font=("Arial", 20, "bold")).pack(pady=10)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        # List Panel (Left)
        self.list_panel = ctk.CTkFrame(container, width=200)
        self.list_panel.pack(side="left", fill="y", padx=(0, 10))

        self.list_buttons = []
        self.refresh_list()

        ctk.CTkButton(self.list_panel, text="+ Create Announcement", command=self.open_create_popup).pack(pady=10)

        # Detail Panel (Right)
        self.detail_panel = ctk.CTkFrame(container)
        self.detail_panel.pack(side="left", fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.detail_panel, text="", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=(10, 5))

        self.body_label = ctk.CTkTextbox(self.detail_panel, height=200, wrap="word")
        self.body_label.pack(padx=10, pady=5, fill="both", expand=True)
        self.body_label.configure(state="disabled")

        self.edit_button = ctk.CTkButton(self.detail_panel, text="Edit", command=self.open_edit_popup)
        self.edit_button.pack(pady=5)
        self.edit_button.configure(state="disabled")

    def refresh_list(self):
        for btn in self.list_buttons:
            btn.destroy()
        self.list_buttons = []

        self.load_data()

        for index, ann in enumerate(self.announcements):
            btn = ctk.CTkButton(self.list_panel, text=ann['title'], anchor="w",
                                 command=lambda i=index: self.show_announcement(i))
            btn.pack(fill="x", padx=10, pady=2)
            self.list_buttons.append(btn)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.announcements = json.load(f)
        else:
            self.announcements = []

    def show_announcement(self, index):
        self.selected_index = index
        announcement = self.announcements[index]
        self.title_label.configure(text=announcement['title'])

        self.body_label.configure(state="normal")
        self.body_label.delete("1.0", "end")
        self.body_label.insert("1.0", announcement['body'])
        self.body_label.configure(state="disabled")

        self.edit_button.configure(state="normal")

    def open_create_popup(self):
        popup = AnnouncementPopup(self, mode="create")
        self.wait_window(popup)
        self.refresh_list()

    def open_edit_popup(self):
        if self.selected_index is not None:
            popup = AnnouncementPopup(self, mode="edit", index=self.selected_index,
                                       data=self.announcements[self.selected_index])
            self.wait_window(popup)
            self.refresh_list()
            self.show_announcement(self.selected_index)