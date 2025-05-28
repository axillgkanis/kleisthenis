import re

# TODO Add connection to dbManager


class manageEmailRegex:
    def __init__(self, local_domain: str, mail_server: str):
        """
        Initialize the manageEmailRegex class with local domain and mail server.
        :param local_domain: The local domain to validate emails against.
        :param mail_server: The allowed mail server to validate emails against.
        """
        self.local_domain = local_domain
        self.mail_server = mail_server

    def checkEmail(self, email: str) -> bool:
        """
        Check if the given email matches the local domain and mail server.
        :param email: The email address to check.
        :return: True if the email is valid, False otherwise.
        """
        print(f"Checking email: {email}")
        # TODO: Implement email validation logic
        pass

    def checkInfo(self):
        """
        Check additional information related to the email validation.
        :return: None
        """
        print("Checking additional email information...")
        # TODO: Implement additional checks
        pass
