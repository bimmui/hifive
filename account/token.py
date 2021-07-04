from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.utils.crypto import salted_hmac
from django.utils.http import int_to_base36

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return (
            text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()