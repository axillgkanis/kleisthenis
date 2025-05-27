import mysql.connector
from dbManager import dbManager
from dialog_screens.DIALOGUE_SCREEN import DIALOGUE_SCREEN
from classes.blockchain import Blockchain

class frameManager:
    def __init__(self):
        self.dialogue_screen = DIALOGUE_SCREEN()
        self.blockchain = Blockchain.load_from_file()

    def searchProposedFrameworks(self):
        """
        Retrieves all proposed frameworks from the database
        Returns: List of dictionaries containing proposed frameworks
        """
        try:
            # Call dbManager to get proposed frameworks
            frameworks = dbManager.queryProposedFrameworks()
            return frameworks if frameworks else DIALOGUE_SCREEN().displayFailure("No proposed frameworks found.")
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
        """
        Creates a vote for a framework and updates its status
        Args:
            framework_id: ID of the framework being voted on
            vote_choice: 'agree' or 'disagree'
            voter_id: ID or email of the user voting
        Returns: True if successful, False otherwise
        """
        try:
            # Update framework status in database
            result = dbManager.updateProposedFrameworkStatus(framework_id, voted=True)
            
            return result
        except Exception as e:
            print(f"Error creating vote: {e}")
            return False

    # def proposeNewFramework(self, title, body):
    #     """
    #     Creates a new proposed framework in the database
    #     Args:
    #         title: Title of the proposed framework
    #         body: Content/description of the proposed framework
    #     Returns: ID of the new framework if successful, None otherwise
    #     """
    #     try:
    #         # Insert new framework into database
    #         new_framework_id = dbManager.insertProposedFramework(title, body)
            
    #         # Create a new topic in blockchain
    #         if new_framework_id:
    #             self.blockchain.add_topic_block(
    #                 topic_id=f"framework-{new_framework_id}",
    #                 title=title,
    #                 description=body,
    #                 options=["agree", "disagree"]
    #             )
    #             self.blockchain.save_to_file()
            
    #         return new_framework_id
    #     except Exception as e:
    #         print(f"Error proposing new framework: {e}")
    #         return None

    # def approveFramework(self, framework_id):
    #     """
    #     Approves a framework for voting
    #     Args:
    #         framework_id: ID of the framework to approve
    #     Returns: True if successful, False otherwise
    #     """
    #     try:
    #         # Update framework status in database
    #         result = dbManager.updateFrameworkApproval(framework_id, approved=True)
    #         return result
    #     except Exception as e:
    #         print(f"Error approving framework: {e}")
    #         return False

    # def rejectFramework(self, framework_id):
    #     """
    #     Rejects a proposed framework
    #     Args:
    #         framework_id: ID of the framework to reject
    #     Returns: True if successful, False otherwise
    #     """
    #     try:
    #         # Delete framework from database
    #         result = dbManager.deleteProposedFramework(framework_id)
    #         return result
    #     except Exception as e:
    #         print(f"Error rejecting framework: {e}")
    #         return False