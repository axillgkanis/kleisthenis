import smtplib
from email.mime.text import MIMEText


class OTPEmailController:
    def __init__(self):
        """
        Initialize the OTPEmailController class.
        """
        self.otp = None
        self.email_content = None

    def createOTPEmail(self, email: str, otp: str):
        self.otp = otp
        self.email_content = f"Hello,\n\nYour OTP is: {self.otp}\n\nThank you."
        print(f"Email content created for {email} with OTP: {self.otp}")

    def sendOTPEMAIL(self, email: str):
        try:
            print(f"Sending OTP email to {email}...")
            msg = MIMEText(self.email_content)
            msg['Subject'] = "Your OTP Code"
            msg['From'] = "noreply@example.com"
            msg['To'] = email
            with smtplib.SMTP('smtp.example.com', 587) as server:
                server.starttls()
                server.login("email@ac.upatras.gr", "SECRET42")
                server.send_message(msg)
            print(f"Email sent to {email} with OTP: {self.otp}")
        except Exception as e:
            print(f"Failed to send email to {email}: {e}")
