from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # six.text_type yerine direkt str() (string) kullanıyoruz
        return (
            str(user.pk) + str(timestamp) +
            str(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()