from unittest import TestCase
from transaction import Transaction
from datetime import datetime


class TestTransaction(TestCase):
    def setUp(self) -> None:
        self.meta_transaction = Transaction(merchant="merchant", amount=0, time="time")

    def test_repr(self):
        _repr = self.meta_transaction.__repr__()
        expected_str = (
            '{"transaction": {"merchant": "merchant", "amount": 0, "time": "time"}}'
        )
        self.assertEqual(_repr, expected_str)

    def test_str(self):
        self.meta_transaction.account = "account"
        _repr = self.meta_transaction.__str__()
        expected_str = '{"transaction": {"merchant": "merchant", "amount": 0, "time": "time", "account": "account"}}'
        self.assertEqual(_repr, expected_str)
