from datetime import datetime, timedelta
from selectors import EpollSelector
from validator import Validator

# Models
from transaction import Transaction
from account import Account


class TransactionValidator(Validator):
    def __init__(self):
        super().__init__()
        self.account = None
        self.transaction = None
        self.historic_transactions = []
        self.hight_frecuency_interval = timedelta(minutes=2)
        self.hight_frecuency_interval_transactions = 3
        self.dobled_transaction_interval = timedelta(minutes=2)

    def verify(self):
        pass

    def verify(self, transaction:Transaction)->list:
        return super().verify()

    def set_account(self, account: Account):
        if self.account:
            return False
        else:
            self.account = account
            return True

    def set_transaction(self, transaction: Transaction)->None:
        self.transaction = transaction
        self.historic_transactions.append(transaction)

    def set_historic_transactions(self, historic_transactions: list)->None:
        self.historic_transactions = historic_transactions

    def has_initialized_account(self)->bool:
        if self.account:
            if isinstance(self.account, Account):
                if self.transaction:
                    if not self.transaction.account:
                        self.transaction.account = self.account
                return True
        return False

    def is_card_active(self)->bool:
        if self.account:
            if self.account.active_card:
                return True
        return False

    def is_in_limit(self)->bool:
        _account_balance = self.account.available_limit
        if self.transaction.amount > _account_balance:
            return False
        else:
            return True

    def in_limit_for_hight_frecuency_interval(self)->bool:
        """
        There should be no more than 3 transactions within a 2 minutes interval
        * Can be configure with  class values :
            hight_frecuency_interval
            hight_frecuency_interval_transactionsal 

        """
        if len(self.historic_transactions) > 1:
            # Takes the second transaction before current one
            _prev_sec_transactions = self.historic_transactions[-self.hight_frecuency_interval_transactions]
            _time_laps_pass_limit = _prev_sec_transactions.time
            _current_time = self.transaction.time
            if ((_current_time - _time_laps_pass_limit) > self.hight_frecuency_interval):
                return True
            else:
                return False
        else:
            return True

    def in_limit_to_not_dobled_transaction(self)->bool:
        """
            This method validates that historic transactions in an hiostoric interval not 
            have same merchant and amount in this time interval
        """
        time_limit = self.transaction.time - self.dobled_transaction_interval
        # This index ignores current transaction that should be set before run this
        transaction_index = len(self.historic_transactions) - 2
        while transaction_index >= 0:
            c_transaction  = self.historic_transactions[transaction_index]
            if c_transaction.time > time_limit:
                return True
            if (
                c_transaction.merchant == self.transaction.merchant
                and 
                c_transaction.amount == self.transaction.merchant
            ):
                return False
        return True
