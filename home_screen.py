import customtkinter as ctk
import json
import os
import tkinter as tk
from datetime import datetime
from tkcalendar import Calendar
from PIL import Image

from dialog_screens.frames_view import FramesView
from dialog_screens.announcements_view import ANNOUNCEMENT_SCREEN
from dialog_screens.set_meeting import SetMeetingPopup
from dialog_screens.set_email_regex_popup import SetEmailRegexPopup
from dialog_screens.punish_user import PunishUserPopup
from dialog_screens.PROPOSED_FRAMEWORKS_SCREEN import PROPOSED_FRAMEWORKS_SCREEN

class KleisthenisDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Kleisthenis Dashboard")
        self.geometry("1000x700")


        self.configure(fg_color="#1e293b")  
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=0)     
        self.grid_rowconfigure(1, weight=1)     
        self.header = ctk.CTkFrame(self, fg_color="#1e293b", height=50)
        self.header.grid(row=0, column=0, columnspan=2, sticky="new")
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(self.header,text="KLEISTHENIS ADMIN DASHBOARD",font=ctk.CTkFont(size=18, weight="bold"),text_color="white").grid(row=0, column=0, padx=20, sticky="w")
        top_buttons = ctk.CTkFrame(self.header, fg_color="transparent")
        top_buttons.grid(row=0, column=1, padx=10, sticky="e")

        ctk.CTkButton(top_buttons, text="Ορισμός Επιτρεπτών Εmail", command=self.open_email_regex, fg_color="#10b981").pack(side="left", padx=5)
        ctk.CTkButton(top_buttons, text="Ορισμος Ποινής",command=self.open_punish_user, fg_color="#7c3aed").pack(side="left", padx=5)
        ctk.CTkButton(top_buttons, text="Αποσύνδεση", fg_color="#ef4444", command=self.destroy).pack(side="left", padx=5)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=300, fg_color="#1e293b")
        self.sidebar.grid(row=1, column=0, sticky="ns")
        self.grid_columnconfigure(0, minsize=300)
        self.sidebar.grid_rowconfigure(7, weight=1)

        user_hash_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        user_hash_container.grid(row=0, column=0, pady=(10, 0))

        ctk.CTkLabel(user_hash_container, text="USER HASH:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left")
        ctk.CTkLabel(user_hash_container, text="test test test", text_color="#22d3ee", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)

        ctk.CTkLabel(self.sidebar, text="Menu", font=ctk.CTkFont(size=20, weight="bold"),text_color="white").grid(row=1, column=0, pady=20)

        ctk.CTkButton(self.sidebar, text="Πλαίσια", command=self.show_frames).grid(row=2, column=0, pady=5)
        ctk.CTkButton(self.sidebar, text="Ανακοινώσεις", command=self.show_announcements).grid(row=3, column=0, pady=5)
        ctk.CTkButton(self.sidebar, text="Ορισμός Συνεδρίας", command=self.open_set_meeting).grid(row=4, column=0, pady=5)
        ctk.CTkButton(self.sidebar, text="Προτεινόμενα Πλαίσια", command=self.show_proposed_frameworks).grid(row=5, column=0, pady=5)

        # Calendar under Exit
        calendar_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        calendar_container.grid(row=7, column=0, padx=10, pady=(20, 10))

        calendar_native = tk.Frame(calendar_container)
        calendar_native.pack()

        self.calendar_widget = Calendar(calendar_native, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar_widget.pack()
        self.calendar_widget.bind("<<CalendarSelected>>", self.on_date_hover)

        self.mark_calendar_events(self.calendar_widget)

        
        logo_path = "Cleisthenes_Voting_Logo.png"
        if os.path.exists(logo_path):
            logo_image = ctk.CTkImage(Image.open(logo_path), size=(180, 180))
            logo_label = ctk.CTkLabel(self.sidebar, image=logo_image, text="")
            logo_label.grid(row=8, column=0, pady=(10, 20))

       
        self.content = ctk.CTkFrame(self)
        self.content.grid(row=1, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.current_view = None
        self.show_frames()

    def clear_content(self):
        if self.current_view:
            self.current_view.destroy()

    def show_frames(self):
        self.clear_content()
        self.current_view = FramesView(self.content)
        self.current_view.pack(fill="both", expand=True)

    def show_announcements(self):
        self.clear_content()
        self.current_view = ANNOUNCEMENT_SCREEN(self.content)
        self.current_view.pack(fill="both", expand=True)

    def open_set_meeting(self):
        popup = SetMeetingPopup(self, on_close=self.refresh_calendar)
        popup.grab_set()

    def show_proposed_frameworks(self):
        self.clear_content()
        self.current_view = PROPOSED_FRAMEWORKS_SCREEN(self.content)
        self.current_view.pack(fill="both", expand=True)

    def open_email_regex(self):
      SetEmailRegexPopup(self)
    def open_punish_user(self):
      PunishUserPopup(self)
    def load_meeting_data(self):
        if os.path.exists("meeting_data.json"):
            with open("meeting_data.json", "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    return data if isinstance(data, list) else [data]
                except json.JSONDecodeError:
                    return []
        return []

    def mark_calendar_events(self, cal):
        for entry in self.load_meeting_data():
            try:
                date_obj = datetime.strptime(entry["date"], "%Y-%m-%d")
                cal.calevent_create(date_obj, "Meeting", "meeting")
            except ValueError:
                pass
        cal.tag_config("meeting", background="blue", foreground="white")

    def refresh_calendar(self):
        self.calendar_widget.calevent_remove("all")
        self.mark_calendar_events(self.calendar_widget)

    def on_date_hover(self, event):
        selected_date = self.calendar_widget.get_date()
        meeting_info = next((entry for entry in self.load_meeting_data() if entry["date"] == selected_date), None)

        if meeting_info:
            message = f"Συνεδρία στις {selected_date}\nΈναρξη: {meeting_info.get('start_time')}\nΛήξη: {meeting_info.get('end_time')}\nΚατάσταση: {meeting_info.get('status')}"
        else:
            message = f"Καμία προγραμματισμένη συνεδρία για {selected_date}."

        tk.messagebox.showinfo("Πληροφορίες Συνεδρίας", message)

if __name__ == "__main__":
    app = KleisthenisDashboard()
    app.mainloop()