from meeting_controller import MeetingController


class MeetingInterface:
    def __init__(self):
        # Create an instance of MeetingController
        self.meeting_controller = MeetingController()

    def start_meeting(self, meeting):
        """Start the meeting."""
        print(f"Starting meeting: {meeting['title']}")
        # Call getFrameworks() from MeetingController
        frameworks = self.meeting_controller.getFrameworks(meeting)
        print(f"Frameworks for meeting '{meeting['title']}': {frameworks}")

    def end_meeting(self, meeting):
        """End the meeting."""
        print(f"Ending meeting: {meeting['title']}")
        # Call countVotesAndResults() from MeetingController
        self.meeting_controller.countVotesAndResults(meeting)
