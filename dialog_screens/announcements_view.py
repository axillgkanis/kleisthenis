import customtkinter as ctk
import json
import os
from dialog_screens.announcement_popup import ANNOUNCEMENT_CREATION_SCREEN,EDIT_ANNOUNCEMENT_SCREEN
from announcementHandler import annoucementHandler
from dialog_screens.DIALOGUE_SCREEN import DIALOGUE_SCREEN

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

        ctk.CTkButton(self.list_panel, text="+ Create Announcement", command=self.open_create_announcement_popup).pack(pady=10)

        # Detail Panel (Right)
        self.detail_panel = ctk.CTkFrame(container)
        self.detail_panel.pack(side="left", fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.detail_panel, text="", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=(10, 5))

        self.body_label = ctk.CTkTextbox(self.detail_panel, height=200, wrap="word")
        self.body_label.pack(padx=10, pady=5, fill="both", expand=True)
        self.body_label.configure(state="disabled")

        self.edit_button = ctk.CTkButton(self.detail_panel, text="Edit", command=self.open_edit_announcement_popup)
        self.edit_button.pack(pady=5)
        self.edit_button.configure(state="disabled")

    #helper function to load data
    def refresh_list(self):
        for btn in self.list_buttons:
            btn.destroy()
        self.list_buttons = []

        self.displayAnnouncements()

        for index, ann in enumerate(self.announcements):
            row = ctk.CTkFrame(self.list_panel)
            row.pack(fill="x", padx=10, pady=2)

            btn = ctk.CTkButton(row, text=ann['title'], anchor="w",
                                command=lambda i=index: self.displayAnnouncementScreen(i))
            btn.pack(side="left", fill="x", expand=True)

            delete_btn = ctk.CTkButton(row, text="-", width=30,
                                       command=lambda i=index: self.delete_announcement(i))
            delete_btn.pack(side="right", padx=5)

            self.list_buttons.append(row)

    def displayAnnouncements(self):
        handler = annoucementHandler(None)
        self.announcements = handler.searchAnnouncement()
        if self.announcements is None:
            self.announcements = []

    #exluded from the uses cases because of simplicity
    def displayAnnouncementScreen(self, index):
        self.selected_index = index
        announcement = self.announcements[index]
        self.title_label.configure(text=announcement['title'])

        self.body_label.configure(state="normal")
        self.body_label.delete("1.0", "end")
        self.body_label.insert("1.0", announcement['body'])
        self.body_label.configure(state="disabled")

        self.edit_button.configure(state="normal")

    #helper for create announcement pop up
    def open_create_announcement_popup(self):
        ANNOUNCEMENT_CREATION_SCREEN.displayAnnouncementScreen(self)

    #helper for edit announcement pop up
    def open_edit_announcement_popup(self):
        if self.selected_index is not None:
            EDIT_ANNOUNCEMENT_SCREEN.displayEditAnnouncement(self, self.selected_index, self.announcements[self.selected_index])

    def save_data(self):
        with open("announcements.json", "w", encoding="utf-8") as f:
            json.dump(self.announcements, f, indent=4, ensure_ascii=False)

    def delete_announcement(self, index):
        if 0 <= index < len(self.announcements):
            announcement_data = self.announcements[index]
            handler = annoucementHandler(announcement_data)
            
            if handler.deleteAnnouncement():
                deleted_title = announcement_data['title']
                self.refresh_list()
                
                # Clear the detail panel
                self.title_label.configure(text="")
                self.body_label.configure(state="normal")
                self.body_label.delete("1.0", "end")
                self.body_label.configure(state="disabled")
                self.edit_button.configure(state="disabled")

                DIALOGUE_SCREEN().displaySuccess(
                    f"Announcement '{deleted_title}' was successfully deleted."
                )
        else:
            DIALOGUE_SCREEN().displayFail(
                "Failed to delete the announcement. Please try again."
            )           