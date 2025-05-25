from datetime import datetime, timedelta


class ManagePenalty:
    def __init__(self, email: str, period: int, reason: str):

        self.email = email
        self.period = period
        self.reason = reason
        self.ban_start_date = datetime.now()

    def checkDuration(self) -> bool:
        ban_end_date = self.ban_start_date + timedelta(days=self.period)
        if datetime.now() < ban_end_date:
            print(
                f"Ban is still active for email: {self.email}. Ban ends on: {ban_end_date}")
            return True
        else:
            print(f"Ban has expired for email: {self.email}.")
            return False

    def checkEmail(self, email: str) -> bool:
        if self.email == email:
            print(f"Email {email} is banned. Reason: {self.reason}")
            return True
        else:
            print(f"Email {email} is not banned.")
            return False
