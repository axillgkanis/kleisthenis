import re
from dbManager import DatabaseConnectionManager


class EmailValidator:
    _local_domain = ""
    _allowed_mail_server = ""

    @staticmethod
    def checkEmail():
        print("Checking email format...")
        # TODO
