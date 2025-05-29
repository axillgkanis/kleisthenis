from twoFactorAuthController import twoFactorAuthController


class twoFactorAuthInterface:
    def __init__(self):
        self.controller = twoFactorAuthController()

    def signInProcedure(self, email: str):
        # Check if the user is banned
        self.controller.checkIfUserIsBanned(email)

        # Create an OTP for the user
        self.controller.createOtp(email)
