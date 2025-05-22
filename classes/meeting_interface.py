class MeetingInterface:
    def start_meeting(self, meeting):
        """Start the meeting."""
        print(f"Starting meeting: {meeting['title']}")

    def end_meeting(self, meeting):
        """End the meeting."""
        print(f"Ending meeting: {meeting['title']}")
