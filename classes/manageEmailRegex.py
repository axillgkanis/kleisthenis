import re


class manageEmailRegex:
    def __init__(self, local_domain: str, mail_server: str):
        self.local_domain = local_domain
        self.mail_server = mail_server

    def checkEmail(self, email: str) -> bool:
        print(f"Checking email: {email}")
        # TODO: Implement email validation logic
        pass

    def checkInfo(self):
        print("Checking additional email information...")
        # TODO: Implement additional checks
        pass
