import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        # https://www.upwork.com/resources/paypal-client-id-secret-key
        self.client_id = "CLIENT ID"
        self.client_secret = "SECRET KEY"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
        print(self.environment, '\n', self.client)
