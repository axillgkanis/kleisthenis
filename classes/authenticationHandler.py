import random
import smtplib


class authenticationHandler:
    def __init__(self):
        """Initialize the AuthenticationHandler."""
        print("AuthenticationHandler initialized.")

    def createOtp(self, email: str):
        """Generate an OTP, save it to the database, and send it to the user's email."""
        # Generate a random 6-digit OTP
        otp = ''.join(random.choices('0123456789', k=6))
        print(f"Generated OTP: {otp} for email: {email}")

        # Simulate saving OTP to the database
        print(f"Saving OTP {otp} to the database for email: {email}")

        # Simulate sending OTP via email
        self.sendEmail(email, otp)

    def checkOtp(self, email: str, otp: str):
        """Check the OTP with the database."""
        print(f"Checking OTP {otp} for email: {email} with the database.")
        # Simulate OTP check
        # Replace with actual validation logic
        print(f"OTP {otp} for email {email} is valid.")

    def checkPassword(self, email: str, password: str):
        """Check the user's password with the database."""
        print(f"Checking password for email: {email} with the database.")
        # Simulate password check
        # Replace with actual validation logic
        print(f"Password for email {email} is valid.")
