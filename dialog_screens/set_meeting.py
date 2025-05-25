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
        self.title("Ορισμός Συνεδρίας")
        self.geometry("500x550")
        self.configure(fg_color="white")
        self.on_close = on_close

        ctk.CTkLabel(self, text="Επέλεξε Ημερομηνία & Ώρα", font=("Arial", 18, "bold"), text_color="black").pack(pady=10)

        self.calendar_frame = ctk.CTkFrame(self, fg_color="white")
        self.calendar_frame.pack(pady=10)

        self.calendar = Calendar(self.calendar_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.pack(pady=5)
        self.calendar.bind("<<CalendarSelected>>", lambda e: self.update_status_label())

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 14), text_color="black")
        self.status_label.pack(pady=5)

        self.start_entry = ctk.CTkEntry(self, placeholder_text="Ώρα Έναρξης (HH:MM)")
        self.start_entry.pack(pady=5)

        self.end_entry = ctk.CTkEntry(self, placeholder_text="Ώρα Λήξης (HH:MM)")
        self.end_entry.pack(pady=5)

        btn_frame = ctk.CTkFrame(self, fg_color="white")
        btn_frame.pack(pady=15)

        ctk.CTkButton(btn_frame, text="Υποβολή", command=self.submit_meeting).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Διαγραφή Ημερομηνίας", fg_color="#ef4444", command=self.delete_meeting).pack(side="left", padx=10)

        action_frame = ctk.CTkFrame(self, fg_color="white")
        action_frame.pack(pady=5)

       #ctk.CTkButton(action_frame, text="Start Meeting", command=self.start_meeting, fg_color="#10b981").pack(side="left", padx=10)
       #ctk.CTkButton(action_frame, text="End Meeting", command=self.end_meeting, fg_color="#facc15").pack(side="left", padx=10)

        self.update_status_label()

    def get_selected_date(self):
        raw = self.calendar.get_date()
        try:
            if "/" in raw:
                date_obj = datetime.strptime(raw, "%m/%d/%y")
            else:
                date_obj = datetime.strptime(raw, "%Y-%m-%d")
            return date_obj.strftime("%Y-%m-%d")
        except Exception as e:
            print("Date parsing error:", e)
            return ""

    def load_all_meetings(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    return data if isinstance(data, list) else [data]
                except json.JSONDecodeError:
                    return []
        return []

    def save_all_meetings(self, data):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def update_status_label(self):
        date = self.get_selected_date()
        for entry in self.load_all_meetings():
            if entry.get("date") == date:
                status = entry.get("status", "scheduled")
                self.status_label.configure(text=f"Status: {status.upper()}")
                return
        self.status_label.configure(text="Καμία προγραμματισμένη συνεδρία.")

    def date_already_exists(self, selected_date):
        return any(entry.get("date") == selected_date for entry in self.load_all_meetings())

    def submit_meeting(self):
        date = self.get_selected_date()
        start_time = self.start_entry.get().strip()
        end_time = self.end_entry.get().strip()

        if self.date_already_exists(date):
            messagebox.showwarning("Δεσμευμένη Ημερομηνία", f"Υπάρχει ήδη προγραμματισμένη συνεδρία για {date}.")
            return

        try:
            datetime.strptime(start_time, "%H:%M")
            datetime.strptime(end_time, "%H:%M")
        except ValueError:
            messagebox.showerror("Λάθοε μορφή Ώρας", "Εισάγετε σωστή μορφή ώρας HH:MM.")
            return

        new_entry = {
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "status": "scheduled"
        }

        data = self.load_all_meetings()
        data.append(new_entry)
        self.save_all_meetings(data)

        messagebox.showinfo("Επιτυχία", "Η συνεδρία προστέθηκε με επιτυχία.")
        self.update_status_label()
        if self.on_close:
            self.on_close()
        self.destroy()

    def delete_meeting(self):
        selected_date = self.get_selected_date()
        data = self.load_all_meetings()
        updated = [entry for entry in data if entry.get("date") != selected_date]

        if len(updated) == len(data):
            messagebox.showinfo("Δεν βρέθηκε", "Δεν βρέθηκε συνεδρ΄λια για την επιλεγμένη ημερομηνία.")
            return

        self.save_all_meetings(updated)
        messagebox.showinfo("Διαγράφηκε", f"Η συνεδρία στις {selected_date} διαγράφηκε.")
        self.update_status_label()
        if self.on_close:
            self.on_close()
        self.destroy()

    def start_meeting(self):
        date = self.get_selected_date()
        data = self.load_all_meetings()
        for meeting in data:
            if meeting.get("date") == date:
                if meeting["status"] == "scheduled":
                    meeting["status"] = "started"
                    self.save_all_meetings(data)
                    messagebox.showinfo("Ξεκίνησε", f"Η συνεδρία στις {date} ξεκίνησε.")
                    self.update_status_label()
                    return
                elif meeting["status"] == "started":
                    messagebox.showinfo("Πληροφορίες", "Η συνεδρία έχει ήδη ξεκινήσει.")
                    return
                elif meeting["status"] == "completed":
                    messagebox.showinfo("Πληροφορίες", "Η συνεδρία έχει ολοκληρωθεί.")
                    return
        messagebox.showwarning("Δεν βρέθηκε", f"Καμί προγραμματισμένη συνεδρία για {date}.")

    def end_meeting(self):
        date = self.get_selected_date()
        data = self.load_all_meetings()
        for meeting in data:
            if meeting.get("date") == date:
                if meeting["status"] == "started":
                    meeting["status"] = "completed"
                    self.save_all_meetings(data)
                    messagebox.showinfo("Ολοκληρομένη", f"Η συνεδρία στις {date} έχει χαρακτηριστεί ως ολοκληρωμένη.")
                    self.update_status_label()
                    return
                elif meeting["status"] == "scheduled":
                    messagebox.showinfo("Πληροφορίες", "Η συνεδρία δεν έχει ξεκινήσει ακόμα.")
                    return
                elif meeting["status"] == "completed":
                    messagebox.showinfo("Πληροφορίες", "Η συνεδρία έχει ολοκληρωθει.")
                    return
        messagebox.showwarning("Δεν βρέθηκε", f"Καμί συνεδρία στις {date}.")
