# utils
from datetime import datetime, timedelta
# thread
import threading
# Models
from transaction import Transaction
from account import Account
from account_validator import AccountValidator
from validator import Validator


ACCOUNT_NOT_INITIALIZED = "account-not-initialized"
CARD_NOT_ACTIVE="card-not-active"
INSUFICIENT_LIMIT="insufficient-limit"
HIGH_FRECUENCY_SMALL_INTERVAL="high-frequency-small-interval"
DOUBLED_TRANSACTION="doubled-transaction"

class TransactionValidator(Validator):
    # Uses Threads for every validation
    def __init__(self, account:Account=Account()):
        super().__init__()
        self.account: Account = account
        self._account_operation = None
        self.transaction: Transaction = None
        self.historic_transactions: list = []
        self.hight_frecuency_interval: timedelta = timedelta(minutes=2)
        self.hight_frecuency_interval_transactions: int = 3
        self.dobled_transaction_interval: timedelta = timedelta(minutes=2)

    def verify(self):
        self._account_operation = self.account.metadata_copy()
        _is_card_active = threading.Thread(target=self.is_card_active)
        _in_limit = threading.Thread(target=self.is_in_limit)
        _in_limit_for_hight_frecuency_interval = threading.Thread(
            target=self.in_limit_for_hight_frecuency_interval
       )
        _in_limit_to_not_dobled_transaction = threading.Thread(
            target=self.in_limit_to_not_dobled_transaction
        )
        _has_initialized_account = threading.Thread(
            target=self.has_initialized_account
        )
        _is_card_active.start()
        _in_limit.start()
        _in_limit_for_hight_frecuency_interval.start()
        _in_limit_to_not_dobled_transaction.start()
        _has_initialized_account.start()

        _is_card_active.join()
        _in_limit.join()
        _in_limit_for_hight_frecuency_interval.join()
        _in_limit_to_not_dobled_transaction.join()
        _has_initialized_account.join()
        return self._account_operation

    def set_account(self, account: Account):
        if self.account.initialized:
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
                if self.account.initialized:
                    if self.transaction:
                        if not self.transaction.account:
                            self.transaction.account = self.account
                    return True
        self._account_operation.add_violation(
            ACCOUNT_NOT_INITIALIZED
        )
        return False

    def is_card_active(self)->bool:
        if self.account:
            if self.account.active_card:
                return True
        self._account_operation.add_violation(CARD_NOT_ACTIVE)
        return False

    def is_in_limit(self)->bool:
        _account_balance = self.account.available_limit
        if self.transaction.amount > _account_balance:
            self._account_operation.add_violation(INSUFICIENT_LIMIT)
            return False

        return True

    def in_limit_for_hight_frecuency_interval(self)->bool:
        """
        There should be no more than 3 transactions within a 2 minutes interval
        * Can be configure with  class values :
            hight_frecuency_interval
            hight_frecuency_interval_transactionsal 

        """
        # His can be change it  for a query
        historic_success_transactions_in_lapse_time = self.get_last_succesfull_transactions_history(
            recent_time=self.transaction.time,
            time_lapse=self.hight_frecuency_interval
        )
        if not historic_success_transactions_in_lapse_time:
            return True
        else:
            self._account_operation.add_violation(HIGH_FRECUENCY_SMALL_INTERVAL)
            return False

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
            if c_transaction.time >= time_limit:      
                if (
                    c_transaction.merchant == self.transaction.merchant
                    and 
                    c_transaction.amount == self.transaction.amount
                ):  
                    self._account_operation.add_violation(DOUBLED_TRANSACTION)
                    return False
            else:
                return True
            transaction_index = transaction_index - 1
        return True

    def get_current_account_operation(self):
        return self._account_operation

    def get_last_succesfull_transactions_history(self, recent_time: datetime, time_lapse: timedelta):
        index = -2
        success_historic = []
        while index >= -len(self.historic_transactions):
            i_transaction =self.historic_transactions[index]
            if (recent_time - i_transaction.time) <= time_lapse:
                if i_transaction.applied:# add it if is success
                    success_historic.append(self.historic_transactions)
            else:
                break
            index = index - 1
        return success_historic
