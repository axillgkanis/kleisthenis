from datetime import datetime
from dbManager import DatabaseManager


class MeetingHandler:
    def __init__(self, date: str, startTime: str, endTime: str):
        self.date = date
        self.startTime = startTime
        self.endTime = endTime

    def newMeeting(self):
        if not self.validateMeeting():
            print("Invalid meeting details. Meeting creation failed.")
            return

        # Call the dbManager's insertMeeting method
        print(
            f"Creating meeting on {self.date} from {self.startTime} to {self.endTime}.")

        db_manager = DatabaseManager()
        db_manager.insertMeeting(self.date, self.startTime, self.endTime)

    def validateMeeting(self) -> bool:
        """
        Validate the meeting details (e.g., date and time).
        :return: True if the meeting details are valid, False otherwise.
        """

        try:
            # Validate date format
            meeting_date = datetime.strptime(self.date, "%Y-%m-%d").date()

            # Validate time format
            start_time = datetime.strptime(self.startTime, "%H:%M").time()
            end_time = datetime.strptime(self.endTime, "%H:%M").time()

            # Ensure start time is before end time
            if start_time >= end_time:
                print("Start time must be before end time.")
                return False

            # Ensure the meeting date is not in the past
            if meeting_date < datetime.now().date():
                print("Meeting date cannot be in the past.")
                return False

            return True
        except ValueError as e:
            print(f"Validation error: {e}")
            return False
