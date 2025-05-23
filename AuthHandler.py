import random
import smtplib
import time
from email.mime.text import MIMEText
from typing import Dict, List, Optional, Tuple


class TwoFAController:
    def __init__(self):
        self.registered_emails: List[str] = []  # List of registered emails
        # email -> (otp, timestamp)
        self.active_otps: Dict[str, Tuple[str, float]] = {}
        self.otp_validity_seconds = 300  # 5 minutes

    def check_email_exists(self, email: str) -> bool:
        """Check if email is registered in the system."""
        return email in self.registered_emails

    def generate_otp(self) -> str:
        """Generate a random 6-digit OTP."""
        return ''.join(random.choices('0123456789', k=6))

    def create_otp(self, email: str) -> str:
        """Create OTP for an email."""
        otp = self.generate_otp()
        self.active_otps[email] = (otp, time.time())
        return otp

    def send_email(self, email: str, otp: str) -> bool:
        """Simulate sending email by writing to a file."""
        try:
            # Create emails directory if it doesn't exist
            import os
            os.makedirs("emails", exist_ok=True)
    
            # Create file with the email content
            with open(f"emails/{email.replace('@', '_at_')}.txt", "w") as f:
                f.write(f"To: {email}\n")
                f.write(f"Subject: Your Authentication OTP\n\n")
                f.write(f"Your OTP for authentication is: {otp}")
    
            print(f"[Development] OTP {otp} sent to {email} (saved to file)")
            return True
        except Exception as e:
            print(f"Failed to save email: {e}")
            return False


class TwoFactorAuthInterface:
    def __init__(self):
        self.controller = TwoFAController()

    def createOTP(self, email: str) -> Dict[str, bool]:
        """Process OTP creation and sending based on email existence."""
        # Check if email is registered
        email_exists = self.controller.check_email_exists(email)

        auth_result = {
            "email_exists": email_exists,
            "can_login": False
        }

        if not email_exists:
            # Email doesn't exist - create and send OTP
            otp = self.controller.create_otp(email)
            otp_sent = self.controller.send_email(email, otp)

            auth_result["otp_sent"] = otp_sent
            # User can login if OTP sent successfully
            auth_result["can_login"] = otp_sent
        else:
            # Email exists, user can't login as per requirements
            auth_result["can_login"] = False

        return auth_result


class AuthHandler:
    def __init__(self):
        self.twofa_interface = TwoFactorAuthInterface()

    def login(self, email: str, password: str) -> Dict[str, any]:
        """Handle login attempt."""
        # Validate credentials (simplified)
        credentials_valid = self._validate_credentials(email, password)

        if not credentials_valid:
            return {"status": "failed", "message": "Invalid credentials"}

        # Request OTP creation through the interface
        auth_result = self.twofa_interface.createOTP(email)

        if auth_result["can_login"]:
            return {
                "status": "pending",
                "message": "OTP sent to email, please verify"
            }
        else:
            if auth_result["email_exists"]:
                return {"status": "failed", "message": "Email already registered, cannot login"}
            else:
                return {"status": "failed", "message": "Failed to process authentication"}

    def _validate_credentials(self, email: str, password: str) -> bool:
        """Validate user credentials."""
        # Simplified validation
        return '@' in email and len(password) >= 6


# Example usage
if __name__ == "__main__":
    auth_system = AuthHandler()
    result = auth_system.login("new.user@example.com", "password123")
    print(result)

    # Add email to registered list for testing
    auth_system.twofa_interface.controller.registered_emails.append(
        "existing@example.com")

    result = auth_system.login("existing@example.com", "password123")
    print(result)
