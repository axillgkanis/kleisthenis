import json
import time
from datetime import datetime, timedelta
import threading
from meeting_interface import MeetingInterface


class MeetingScheduler:
    def __init__(self, json_file="meetings.json"):
        self.json_file = json_file
        self.meetings = []
        self.load_meetings()
        self.running = True
        # Create an instance of MeetingInterface
        self.meeting_interface = MeetingInterface()

    def load_meetings(self):
        """Load meetings from a JSON file."""
        try:
            with open(self.json_file, "r") as file:
                self.meetings = json.load(file)
                print(
                    f"Loaded {len(self.meetings)} meetings from {self.json_file}")
        except FileNotFoundError:
            print(
                f"File {self.json_file} not found. Starting with an empty meeting list.")
            self.meetings = []
        except json.JSONDecodeError:
            print(
                f"Error decoding JSON in {self.json_file}. Starting with an empty meeting list.")
            self.meetings = []

    def start_scheduler(self):
        """Start the meeting scheduler in a separate thread."""
        def scheduler_loop():
            while self.running:
                now = datetime.now()
                for meeting in self.meetings:
                    start_time = datetime.strptime(
                        meeting["start_time"], "%Y-%m-%d %H:%M:%S")
                    end_time = datetime.strptime(
                        meeting["end_time"], "%Y-%m-%d %H:%M:%S")

                    # Check if it's time to start the meeting
                    if start_time <= now < start_time + timedelta(seconds=1):
                        self.handle_signal("start", meeting)

                    # Check if it's time to end the meeting
                    if end_time <= now < end_time + timedelta(seconds=1):
                        self.handle_signal("end", meeting)

                time.sleep(60)  # Check every second

        threading.Thread(target=scheduler_loop, daemon=True).start()

    def handle_signal(self, signal_type, meeting):
        """Handle start or end signals for meetings."""
        if signal_type == "start":
            print(f"Meeting '{meeting['title']}' is starting.")
            self.meeting_interface.start_meeting(meeting)
        elif signal_type == "end":
            print(f"Meeting '{meeting['title']}' is ending.")
            self.meeting_interface.end_meeting(meeting)

    def stop_scheduler(self):
        """Stop the meeting scheduler."""
        self.running = False
