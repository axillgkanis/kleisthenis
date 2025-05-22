import customtkinter as ctk
import json
import os
import tkinter.messagebox as messagebox
from dialog_screens.announcement_popup import AnnouncementPopup  

DATA_FILE = "announcements.json"

class ANNOUNCEMENT_SCREEN(ctk.CTkFrame):
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
            row = ctk.CTkFrame(self.list_panel)
            row.pack(fill="x", padx=10, pady=2)

            btn = ctk.CTkButton(row, text=ann['title'], anchor="w",
                                command=lambda i=index: self.show_announcement(i))
            btn.pack(side="left", fill="x", expand=True)

            delete_btn = ctk.CTkButton(row, text="-", width=30,
                                       command=lambda i=index: self.delete_announcement(i))
            delete_btn.pack(side="right", padx=5)

            self.list_buttons.append(row)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.announcements = json.load(f)
        else:
            self.announcements = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.announcements, f, indent=4, ensure_ascii=False)

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

    def delete_announcement(self, index):
        if 0 <= index < len(self.announcements):
            deleted_title = self.announcements[index]['title']
            del self.announcements[index]
            self.save_data()
            self.refresh_list()
            self.title_label.configure(text="")
            self.body_label.configure(state="normal")
            self.body_label.delete("1.0", "end")
            self.body_label.configure(state="disabled")
            self.edit_button.configure(state="disabled")

            messagebox.showinfo(
                "Deleted",
                f"Announcement '{deleted_title}' was successfully deleted."
            )
