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

    def validate_operations(self, operations: list):
        for operation in operations:
            # transactions should be the most common operation
            transaction = operation.get(self.kind_transction, None)
            if transaction:
                c_time = datetime.strptime(
                    transaction.get("time"),
                    self.date_format
                )
                c_transaction = Transaction(
                    merchant=transaction.get("merchant", ""),
                    amount=transaction.get("amount"),
                    time=c_time
                )
                if self.transaction_validator.account:
                    # Set account relation into transaction
                    c_transaction.set_account(self.transaction_validator.account)
                self.transaction_validator.set_transaction(c_transaction)
                
            else:
                account = operation.get(self.kind_account, None)
                if account:
                    pass 
                else:
                    pass          
            
            if account:
                c_account = Account(
                    active_card=account.get("active-card", False),
                    available_limit=account.get("available-limit", -1)
                )
            else:
