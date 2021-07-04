import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AUdym9sqk-OJr0aFbmAyOmzOcoDyrJQdDeB0Dm9SYwiLOOoJEBmERhN4q11yGQGeBEZU0oNRkruA4W0F"
        self.client_secret = "ENL_VHg9HeM-GOUU7onbYiPDaXqDyhkcxNQ33rR3563JlW2J7sIF34JavbPPfdCRoA5MtjJRUMgrPrGe"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
        print(self.environment, '\n', self.client)