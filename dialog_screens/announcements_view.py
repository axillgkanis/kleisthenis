import customtkinter as ctk
import json
import os
from dialog_screens.announcement_popup import ANNOUNCEMENT_CREATION_SCREEN, EDIT_ANNOUNCEMENT_SCREEN
from announcementHandler import annoucementHandler

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
            btn = ctk.CTkButton(self.list_panel, text=ann['title'], anchor="w",
                                 command=lambda i=index: self.displayAnnouncementScreen(i))
            btn.pack(fill="x", padx=10, pady=2)
            self.list_buttons.append(btn)

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