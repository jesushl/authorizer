import imp
from unittest import TestCase
# Models
from account import Account
# validator
from account_validator import AccountValidator

class TestAccountValidator(TestCase):
    def setUp(self):
        self.valid_account = Account(
            active_card=True,
            available_limit=10
        )
        self.second_not_valid_account = Account(
            active_card=True,
            available_limit=100
        )
        self.account_validator = AccountValidator()

    def test_exist_a_valid_account(self):
        self.assertFalse(
            self.account_validator.exists_a_valid_account()
        )
        self.account_validator.account = self.valid_account
        self.assertTrue(
            self.account_validator.exists_a_valid_account()
        )
        
