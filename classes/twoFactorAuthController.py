from dbManager import DatabaseManager


class twoFactorAuthController:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def createOtp(self, email: str):
        print(f"Creating OTP for email: {email}")
        self.db_manager.createOtp(email)

    def checkIfUserIsBanned(self, email: str):

        print(f"Checking if user is banned for email: {email}")
        self.db_manager.checkIfUserIsBanned(email)
