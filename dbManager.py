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

    def queryProposedFrameworks():
        """
        Retrieve all proposed frameworks from the database
        Returns: List of dictionaries containing framework information
        """
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                'SELECT * FROM frameworks WHERE approved = 0 ORDER BY id DESC'
            )
            frameworks = cursor.fetchall()
            cursor.close()
            conn.close()
            return frameworks
        except mysql.connector.Error as e:
            print(f"Error retrieving frameworks: {e}")
            return []

    def queryProposedFrameworkDetails(framework_id):
        """
        Retrieve details for a specific framework
        Args:
            framework_id: ID of the framework to retrieve
        Returns: Dictionary containing framework details or None if not found
        """
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                'SELECT * FROM frameworks WHERE id = %s',
                (framework_id,)
            )
            framework = cursor.fetchone()
            cursor.close()
            conn.close()
            return framework
        except mysql.connector.Error as e:
            print(f"Error retrieving framework details: {e}")
            return None

    def updateProposedFrameworkStatus(framework_id, vote):
        """
        Update the vote status of a framework
        Args:
            framework_id: ID of the framework to update
            voted: Whether the framework has been voted on
        Returns: True if successful, False otherwise
        """
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE frameworks SET approved = %s WHERE id = %s',
                (vote, framework_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error updating framework status: {e}")
            return False

    def insertProposedFramework(title: str, body: str) -> int:
        """
        Inserts a new framework into the database
        Args:
            title: Title of the framework
            body: Content/description of the framework
        Returns: ID of the new framework if successful, None otherwise
        """
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO frameworks (title, body, approved, vote) VALUES (%s, %s, 0, 0)',
                (title, body)
            )
            framework_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            return framework_id
        except mysql.connector.Error as e:
            print(f"Error inserting framework: {e}")
            return None