from unittest import TestCase
from datetime import datetime, timedelta

# Models
from account import Account
from transaction import Transaction

# Validator
from transaction_validator import TransactionValidator


class TestTransactionValidator(TestCase):
    def setUp(self):
        self.merchant_1 = "1"
        self.merchant_2 = "2"
        self.merchant_3 = "3"
        self.time_now = datetime.now()
        self.delta_30_s = timedelta(seconds=30)
        self.delta_10_s = timedelta(seconds=10)
        self.delta_1_m = timedelta(minutes=1)
        self.valid_account = Account(
            active_card=True, 
            available_limit=10
        )
        self.second_not_valid_account = Account(
            active_card=False,
            available_limit=100
        )
        self.transaction_1_merchant_1 = Transaction(
            merchant=self.merchant_1,
            amount=1,
        )

    def test_has_inizialized_account(self):
        transaction_validator = TransactionValidator()
        self.assertFalse(transaction_validator.has_initialized_account())
        transaction_validator.set_account(self.valid_account)
        self.assertTrue(transaction_validator.has_initialized_account())
    
    def test_is_card_active(self):
        transaction_validator = TransactionValidator()
        self.assertFalse(
            transaction_validator.is_card_active()
        )
        transaction_validator.set_account(
            self.second_not_valid_account
        )
        self.assertFalse(
            transaction_validator.is_card_active()
        )
        transaction_validator.account = self.valid_account
    
        self.assertTrue(
            transaction_validator.is_card_active()
        )
