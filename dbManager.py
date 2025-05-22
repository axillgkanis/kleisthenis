import mysql.connector
from datetime import datetime
import mysql.connector
from typing import List, Dict
import tkinter as tk
from tkinter import messagebox

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'dbManager',
    'password': '1234',
    'database': 'cleisthenes_database'
}

# Database setup function
def setup_database():
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    cursor = conn.cursor()
class dbManager:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()
        self.create_table()

    def query_announcements() -> List[Dict]:
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

    def insert_announcement(title: str, body: str) -> bool:
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

    # Add after create_announcement function
    def modify_announcement(id: int, title: str, body: str) -> bool:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE announcements SET title=%s, body=%s WHERE id=%s',
                (title, body, id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error updating announcement: {e}")
            return False

    def delete_announcement(id: int) -> bool:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM announcements WHERE id=%s', (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error deleting announcement: {e}")
            return False