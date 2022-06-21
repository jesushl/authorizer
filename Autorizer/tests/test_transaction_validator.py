from time import time
from unittest import TestCase
from datetime import date, datetime, timedelta

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
        self.valid_account = Account(active_card=True, available_limit=10)
        self.second_not_valid_account = Account(active_card=False, available_limit=100)
        self.transaction_1_merchant_1 = Transaction(
            merchant=self.merchant_1,
            amount=10,
        )
        self.transaction_2 = Transaction(merchant=self.merchant_2, amount=20)
        self.transaction_3 = Transaction(merchant=self.merchant_3, amount=30)

    def test_has_inizialized_account(self):
        transaction_validator = TransactionValidator()
        self.assertFalse(transaction_validator.has_initialized_account())
        transaction_validator.set_account(self.valid_account)
        self.assertTrue(transaction_validator.has_initialized_account())

    def test_is_card_active(self):
        transaction_validator = TransactionValidator()
        self.assertFalse(transaction_validator.is_card_active())
        transaction_validator.set_account(self.second_not_valid_account)
        self.assertFalse(transaction_validator.is_card_active())
        transaction_validator.account = self.valid_account
        self.assertTrue(transaction_validator.is_card_active())

    def test_is_in_limit(self):
        transaction_validator = TransactionValidator()
        # Account limit 10, transaction 10
        transaction_validator.set_transaction(self.transaction_1_merchant_1)
        transaction_validator.set_account(self.valid_account)
        self.assertTrue(transaction_validator.is_in_limit())
        transaction_validator.account.available_limit = (
            transaction_validator.account.available_limit
            - transaction_validator.transaction.amount
        )
        self.assertFalse(transaction_validator.is_in_limit())

    def test_in_limit_for_hight_frecuency_interval(self):
        transaction_validator = TransactionValidator()
        now = datetime.now()
        t1 = Transaction(time=now)
        t2 = Transaction(time=now + timedelta(seconds=10))
        t3 = Transaction(time=now + timedelta(seconds=20))
        time_limit = transaction_validator.hight_frecuency_interval
        historic = [t1, t2]
        transaction_validator.set_historic_transactions(historic)
        transaction_validator.set_transaction(t3)
        self.assertFalse(transaction_validator.in_limit_for_hight_frecuency_interval())
        t3.time = now + timedelta(minutes=2)
        self.assertFalse(transaction_validator.in_limit_for_hight_frecuency_interval())
        t3.time = now + timedelta(minutes=2, seconds=10)
        self.assertTrue(transaction_validator.in_limit_for_hight_frecuency_interval())
        t3.time = now + timedelta(minutes=2, seconds=11)
        self.assertTrue(transaction_validator.in_limit_for_hight_frecuency_interval())
        transaction_validator.set_historic_transactions([])
        transaction_validator.set_transaction(t3)
        self.assertTrue(transaction_validator.in_limit_for_hight_frecuency_interval())

    def test_in_limit_to_not_dobled_transaction(self):
        merchant_1 = "merchant_1"
        merchant_2 = "merchant_2"
        amount_1 = 1
        amount_2 = 2
        now = datetime.now()
        t_plus_one_minute = now + timedelta(minutes=1)
        t_plus_two_minuntes = now + timedelta(minutes=2)
        t_plus_two_minuntes_one_second = now + timedelta(minutes=2, seconds=1)
        t1 = Transaction(merchant=merchant_1, amount=amount_1, time=now)
        t2_not_valid = Transaction(
            merchant=merchant_1, amount=amount_1, time=t_plus_one_minute
        )
        t3_not_valid = Transaction(
            merchant=merchant_1, amount=amount_1, time=t_plus_two_minuntes
        )
        t4_valid = Transaction(
            merchant=merchant_2, amount=amount_1, time=t_plus_two_minuntes_one_second
        )
        t5_valid = Transaction(
            merchant=merchant_2, amount=amount_2, time=t_plus_one_minute
        )
        transaction_validator = TransactionValidator()
        transaction_validator.set_historic_transactions([t1])
        transaction_validator.set_transaction(t2_not_valid)
        self.assertFalse(transaction_validator.in_limit_to_not_dobled_transaction())
        transaction_validator.transaction = t3_not_valid
        self.assertFalse(transaction_validator.in_limit_to_not_dobled_transaction())
        transaction_validator.transaction = t4_valid
        self.assertTrue(transaction_validator.in_limit_to_not_dobled_transaction())
        transaction_validator.transaction = t5_valid
        self.assertTrue(transaction_validator.in_limit_to_not_dobled_transaction())
