from datetime import datetime
import mysql.connector
from typing import List, Dict
import tkinter as tk
from tkinter import messagebox
from dbManager import DB_CONFIG, conn, setup_database

# Database operations
def load_announcements() -> List[Dict]:
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM announcements ORDER BY date_created DESC')
        announcements = cursor.fetchall()
        cursor.close()
        conn.close()
        return announcements
    except mysql.connector.Error as e:
        print(f"Error loading announcements: {e}")
        return []

def create_announcement(title: str, body: str) -> bool:
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO announcements (title, body) VALUES (%s, %s)',
            (title, body)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as e:
        print(f"Error creating announcement: {e}")
        return False

def insert_test_announcement():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        test_title = "Test Announcement"
        test_body = "This is a test announcement created on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute(
            'INSERT INTO announcements (title, body) VALUES (%s, %s)',
            (test_title, test_body)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Test announcement inserted successfully!")
        return True
    except mysql.connector.Error as e:
        print(f"Error inserting test announcement: {e}")
        return False

# UI Implementation
# class AnnouncementApp:
#     def __init__(self):
#         self.window = tk.Tk()
#         self.window.title("Announcements")
#         self.window.geometry("800x600")
        
#         # Create main screen elements
#         self.create_button = tk.Button(
#             self.window, 
#             text="Create Announcement",
#             command=self.show_creation_dialog
#         )
#         self.create_button.pack(pady=10)
        
#         self.announcements_frame = tk.Frame(self.window)
#         self.announcements_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
#         self.refresh_announcements()

#     def refresh_announcements(self):
#         # Clear existing announcements
#         for widget in self.announcements_frame.winfo_children():
#             widget.destroy()
            
#         # Load and display announcements
#         announcements = load_announcements()
#         for ann in announcements:
#             frame = tk.Frame(self.announcements_frame, relief=tk.RAISED, borderwidth=1)
#             frame.pack(fill=tk.X, pady=5)
            
#             tk.Label(frame, text=ann['title'], font=('Arial', 12, 'bold')).pack(anchor='w')
#             tk.Label(frame, text=ann['body']).pack(anchor='w')
#             tk.Label(frame, text=ann['date_created'], font=('Arial', 8)).pack(anchor='w')

#     def show_creation_dialog(self):
#         dialog = tk.Toplevel(self.window)
#         dialog.title("Create Announcement")
#         dialog.geometry("400x300")
        
#         tk.Label(dialog, text="Title:").pack(pady=5)
#         title_entry = tk.Entry(dialog, width=50)
#         title_entry.pack()
        
#         tk.Label(dialog, text="Body:").pack(pady=5)
#         body_text = tk.Text(dialog, height=10)
#         body_text.pack()
        
#         def submit():
#             title = title_entry.get()
#             body = body_text.get("1.0", tk.END).strip()
            
#             if title and body:
#                 if create_announcement(title, body):
#                     messagebox.showinfo("Success", "Announcement created successfully!")
#                     dialog.destroy()
#                     self.refresh_announcements()
#                 else:
#                     messagebox.showerror("Error", "Failed to create announcement")
#             else:
#                 messagebox.showwarning("Warning", "Please fill all fields")
        
#         submit_btn = tk.Button(dialog, text="Submit", command=submit)
#         submit_btn.pack(pady=10)

#     def run(self):
#         self.window.mainloop()

# Main execution
if __name__ == "__main__":
    try:
        setup_database()
        insert_test_announcement()
        # app = AnnouncementApp()
        # app.run()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", 
            "Failed to connect to database. Please check your MySQL configuration.")
        print(f"Database error: {e}")