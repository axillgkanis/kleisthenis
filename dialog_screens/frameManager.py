import mysql.connector
from dbManager import dbManager
from dialog_screens.DIALOGUE_SCREEN import DIALOGUE
from classes.blockchain import Blockchain


class frameManager:
    def __init__(self):
        self.dialogue_screen = DIALOGUE()
        self.blockchain = Blockchain.load_from_file()

    def searchProposedFrameworks(self):
        """
        Retrieves all proposed frameworks from the database
        Returns: List of dictionaries containing proposed frameworks
        """
        try:
            # Call dbManager to get proposed frameworks
            frameworks = dbManager.queryProposedFrameworks()
            return frameworks if frameworks else DIALOGUE().displayFailure("No proposed frameworks found.")
        except Exception as e:
            print(f"Error retrieving proposed frameworks: {e}")
            return []

    def searchProposedFrameDetails(self, framework_id):
        """
        Retrieves details for a specific framework
        Args:
            framework_id: ID of the framework to retrieve
        Returns: Dictionary containing framework details or None if not found
        """
        try:
            # Call dbManager to get framework details
            framework = dbManager.queryProposedFrameworkDetails(framework_id)
            return framework
        except Exception as e:
            print(f"Error retrieving framework details: {e}")
            return None

    def createVote(self, framework_id, vote_choice, voter_id):

        try:
            # Update framework status in database
            result = dbManager.updateProposedFrameworkStatus(
                framework_id, voted=True)

            return result
        except Exception as e:
            print(f"Error creating vote: {e}")
            return False

    def proposeFrame(self, title, body):
        try:
            # Insert new framework into database
            new_framework_id = dbManager.insertProposedFramework(title, body)

            # Create a new topic in blockchain
            if new_framework_id:
                self.blockchain.add_topic_block(
                    topic_id=f"framework-{new_framework_id}",
                    title=title,
                    description=body,
                    options=["agree", "disagree"]
                )
                self.blockchain.save_to_file()

            return new_framework_id
        except Exception as e:
            print(f"Error proposing new framework: {e}")
            return None
