import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
import json
import os
from datetime import datetime

DATA_FILE = "meeting_data.json"

class SetMeetingPopup(ctk.CTkToplevel):
    def __init__(self, parent, on_close=None):
        super().__init__(parent)
        self.title("Set Meeting")
        self.geometry("500x500")
        self.configure(fg_color="white")
        self.on_close = on_close

        ctk.CTkLabel(self, text="Choose Date & Time", font=("Arial", 18, "bold"), text_color="black").pack(pady=10)

        self.calendar_frame = ctk.CTkFrame(self, fg_color="white")
        self.calendar_frame.pack(pady=10)

        self.calendar = Calendar(self.calendar_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.pack(pady=5)

        self.start_entry = ctk.CTkEntry(self, placeholder_text="Start time (HH:MM)")
        self.start_entry.pack(pady=5)

        self.end_entry = ctk.CTkEntry(self, placeholder_text="End time (HH:MM)")
        self.end_entry.pack(pady=5)

        btn_frame = ctk.CTkFrame(self, fg_color="white")
        btn_frame.pack(pady=15)

        ctk.CTkButton(btn_frame, text="Submit", command=self.submit_meeting).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Delete Date", fg_color="#ef4444", command=self.delete_meeting).pack(side="left", padx=10)

    def get_selected_date(self):
        raw = self.calendar.get_date()
        try:
            return datetime.strptime(raw, "%m/%d/%y").strftime("%Y-%m-%d")
        except ValueError:
            return raw  # Already in correct format

    def date_already_exists(self, selected_date):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = [data]
                except json.JSONDecodeError:
                    return False
            for entry in data:
                if entry.get("date") == selected_date:
                    return True
        return False

    def submit_meeting(self):
        date = self.get_selected_date()
        start_time = self.start_entry.get().strip()
        end_time = self.end_entry.get().strip()

        if self.date_already_exists(date):
            messagebox.showwarning("Date Exists", f"A meeting is already scheduled on {date}.")
            return

        try:
            datetime.strptime(start_time, "%H:%M")
            datetime.strptime(end_time, "%H:%M")
        except ValueError:
            messagebox.showerror("Invalid Format", "Please use valid time format HH:MM.")
            return

        new_entry = {
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "status": "scheduled"
        }

        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = [data]
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append(new_entry)

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Success", "Meeting added.")

        if self.on_close:
            self.on_close()

        self.destroy()

    def delete_meeting(self):
        selected_date = self.get_selected_date()

        if not os.path.exists(DATA_FILE):
            messagebox.showinfo("No Data", "No meetings to delete.")
            return

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
            except json.JSONDecodeError:
                data = []

        updated_data = [entry for entry in data if entry.get("date") != selected_date]

        if len(updated_data) == len(data):
            messagebox.showinfo("Nothing Found", "No meetings found for selected date.")
            return

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_data, f, indent=4)

        messagebox.showinfo("Deleted", f"Meetings on {selected_date} deleted.")

        if self.on_close:
            self.on_close()

        self.destroy()
