from blockchain import Blockchain
from announcement_manager import AnnouncementManager
from framework_manager import FrameworkManager
from database_manager import DatabaseManager


class MeetingController:
    def __init__(self):
        """Initialize the MeetingController with required managers and Blockchain."""
        self.blockchain = Blockchain.load_from_file()  # Load the blockchain once
        self.announcement_manager = AnnouncementManager()
        self.framework_manager = FrameworkManager()
        self.database_manager = DatabaseManager()

    def countVotesAndResults(self, meeting):
        """Count votes and calculate results for the meeting."""
        print(
            f"Counting votes and calculating results for meeting: {meeting['title']}")

        # Get the framework IDs associated with the meeting
        framework_ids = meeting.get("framework_ids", [])
        if not framework_ids:
            print("No framework IDs found for the meeting.")
            return

        results = {}  # Store results for each framework #TODO This changes into another function that is called calculateAndSaveResults

        for framework_id in framework_ids:
            votes = self.blockchain.get_votes_for_topic(framework_id)
            if not votes:
                print(f"No votes found for framework ID: {framework_id}")
                results[framework_id] = {"status": "no_votes"}
                continue

            # Count votes for the framework
            total_votes = sum(votes.values())
            max_votes = max(votes.values())
            tied = list(votes.values()).count(max_votes) > 1

            # Save the result for the framework
            if tied:
                self.handleTie(framework_id, votes, meeting)
                results[framework_id] = {"status": "tie", "votes": votes}
            else:
                winner = max(votes, key=votes.get)
                self.handleAgreeOrDisagree(
                    framework_id, winner, votes[winner], meeting)
                results[framework_id] = {
                    "status": "resolved", "winner": winner, "votes": votes}

        # After processing all frameworks, perform an additional action
        self.finalizeMeeting(meeting, results)

    def handleAgreeOrDisagree(self, framework_id, verdict, vote_count, meeting):
        """Handle behavior for 'agree' or 'disagree' results."""
        print(
            f"Framework '{framework_id}' resolved with verdict '{verdict}' in meeting '{meeting['title']}'")
        print(f"Total votes for winner '{verdict}': {vote_count}")

        # Call setFrameworkSettled on the FrameworkManager
        self.framework_manager.setFrameworkSettled(framework_id, verdict)

        # Add logic to save the result or perform specific actions
        print(f"Action for framework '{framework_id}' completed.")

    def handleTie(self, framework_id, votes, meeting):
        """Handle behavior for a tie."""
        print(
            f"Framework '{framework_id}' resulted in a tie in meeting '{meeting['title']}'")
        print(f"Votes: {votes}")

        # Call createNewFramework on the FrameworkManager
        self.framework_manager.createNewFramework(framework_id, votes)

        # Add logic to handle tie (e.g., notify stakeholders or log the tie)
        print(f"Action for tie in framework '{framework_id}' completed.")

    def finalizeMeeting(self, meeting, results):
        """Perform final actions after processing all frameworks."""
        print(f"Finalizing meeting '{meeting['title']}'")
        print(f"Results: {results}")

        # Call createResultsAnnouncement for each framework
        for framework_id, result_data in results.items():
            self.announcement_manager.createResultsAnnouncement(
                framework_id=framework_id,
                meeting_title=meeting["title"],
                result_data=result_data
            )

        print(f"Meeting '{meeting['title']}' finalized.")


def getFrameworks(self, meeting):
    """Retrieve frameworks for the meeting."""
    print(f"Retrieving frameworks for meeting: {meeting['title']}")

    # Call queryFrameworks from the DatabaseManager
    frameworks = self.database_manager.queryFrameworks()
    if not frameworks:
        print("No framework IDs found for the meeting.")
        # Call createCancelledAnnouncement from AnnouncementManager
        self.announcement_manager.createCancelledAnnouncement(
            meeting_title=meeting["date"],
            reason="No framework IDs associated with the meeting."
        )
    else:
        print(
            f"No frameworks found in the database for meeting '{meeting['title']}'")
        # Call createCancelledAnnouncement from AnnouncementManager
        self.announcement_manager.createCancelledAnnouncement(
            meeting_title=meeting["title"],
            reason="No frameworks found in the database."
        )
