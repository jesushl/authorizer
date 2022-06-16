from unittest import TestCase

# Models
from account import Account

# validator
from account_validator import AccountValidator


class TestAccountValidator(TestCase):
    def setUp(self):
        self.valid_account = Account(active_card=True, available_limit=10)
        self.second_not_valid_account = Account(active_card=True, available_limit=100)
        self.account_validator = AccountValidator()

    def test_exist_a_valid_account(self):
        self.assertTrue(self.account_validator.not_exists_a_valid_account())
        self.account_validator.account = self.valid_account
        self.assertFalse(self.account_validator.not_exists_a_valid_account())

    def test_verify(self):
        self.assertListEqual(
            self.account_validator.verify(), ["account-not-initialized"]
        )
        self.account_validator = AccountValidator()
        self.account_validator.account = "Account"
        self.assertListEqual(
            self.account_validator.verify(), ["account-not-initialized"]
        )
        self.account_validator = AccountValidator()
        self.account_validator.account = self.valid_account
        self.assertListEqual(self.account_validator.verify(), [])
