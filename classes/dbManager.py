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
            cursor.execute(
                'SELECT * FROM announcements ORDER BY date_created DESC')
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

    def queryEmailRegex(self):
        print("Querying email regex from the database.")

    def queryAccess(self):
        print("Querying access details from the database.")

    def queryFrameworks(self):
        print("Querying frameworks from the database.")

    def queryFrameworkDetails(self, framework_id):
        print(f"Querying details for framework ID: {framework_id}.")

    def queryBannedEmails(self):
        print("Querying banned emails from the database.")

    def saveOTP(self, email, otp):
        print(f"Saving OTP {otp} for email {email}.")

    def queryAnnouncements(self):
        print("Querying announcements from the database.")

    def insertAnnouncement(self, announcement_data):
        print(f"Inserting announcement: {announcement_data}.")

    def modifyAnnouncement(self, announcement_id, updated_data):
        print(
            f"Modifying announcement ID {announcement_id} with data {updated_data}.")

    def deleteAnnouncement(self, announcement_id):
        print(f"Deleting announcement ID {announcement_id}.")

    def queryPassword(self, email):
        print(f"Querying password for email: {email}.")

    def insertMeeting(self, meeting_data):
        print(f"Inserting meeting: {meeting_data}.")

    def insertPenalty(self, penalty_data):
        print(f"Inserting penalty: {penalty_data}.")

    def insertRegexEmail(self, regex_data):
        print(f"Inserting regex email: {regex_data}.")

    def updateFrameworkToSettled(self, framework_id, verdict):
        print(
            f"Updating framework ID {framework_id} to settled with verdict {verdict}.")
