from turtle import pd
from unittest import TestCase

# Models
from account import Account

# validator
from account_validator import AccountValidator, ACCOUNT_ALREADY_INITIALIZED


class TestAccountValidator(TestCase):
    
    def setUp(self):
        self.valid_account = Account(active_card=True, available_limit=10)
        self.not_initiated_account = Account()
        self.account_validator = AccountValidator()

    def test_exist_a_valid_account(self):
        self.assertFalse(self.account_validator.is_valid_account())
        self.account_validator.account = self.valid_account
        self.account_validator.meta_account = self.valid_account.metadata_copy()
        self.assertTrue(self.account_validator.is_valid_account())

    def test_is_already_initiated(self):
        self.account_validator.account = None
        self.account_validator.meta_account = None
        self.assertFalse(
            self.account_validator.is_already_initiated()
        )
        self.account_validator.account = self.not_initiated_account
        self.account_validator.meta_account = self.not_initiated_account.metadata_copy()
        self.assertFalse(
            self.account_validator.is_already_initiated()
        )
        self.account_validator.account = self.valid_account
        self.account_validator.meta_account = self.valid_account.metadata_copy()
        self.assertTrue(
            self.account_validator.is_already_initiated()
        )

    def test_verify(self):
        self.account_validator.account = self.valid_account
        self.account_validator.verify()
        self.assertListEqual(
            self.account_validator.meta_account.violations, 
            [ACCOUNT_ALREADY_INITIALIZED]
        )
