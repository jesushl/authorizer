# utils
from datetime import datetime
# Models
from account import Account
from account_validator import AccountValidator
from account_validator import (
    ACCOUNT_NOT_INITIALIZED
)
from transaction import Transaction
from transaction_validator import TransactionValidator
from transaction_validator import (
    CARD_NOT_ACTIVE,
    INSUFICIENT_LIMIT,
    HIGH_FRECUENCY_SMALL_INTERVAL,
    DOUBLED_TRANSACTION
)

class OperationsValidator():

    def __init__(self):
        self.transaction_validator = TransactionValidator()
        self.account_validator = AccountValidator()
        self.kind_transction = "transaction"
        self.kind_account = "account"
        self.date_format = "%Y-%m-%dT%H:%M:%S.%fZ" 
        self.actions_log = []

    def validate_operations(self, operations: list):
        for operation in operations:
            pass 

    def validate_operation(self, operation: dict):
        transaction = operation.get(self.kind_transction, None)
        if transaction:
            self.validate_transaction(transaction)
        else:
            account = operation.get(self.kind_account, None)
            if account:
                self.validate_account(account)


    def validate_transaction(self, transaction: dict):
        c_time = datetime.strptime(
                transaction.get("time"),
                self.date_format
            )
        c_transaction = Transaction(
            merchant=transaction.get("merchant", ""),
            amount=transaction.get("amount"),
            time=c_time
        )
        self.transaction_validator.set_transaction(c_transaction)
        _account_operation = self.transaction_validator.verify()
        self.actions_log.append(_account_operation)

    def validate_account(self, account: dict):
        pass
