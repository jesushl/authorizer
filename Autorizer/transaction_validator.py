from datetime import timedelta
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
        self.historic_transactions  = []

    def verify(self):
        pass 

    def set_account(self, account: Account):
        if self.account:
            return False
        else:
            self.account = account 
            return True
    
    def set_transaction(self, transaction: Transaction):
        self.transaction = transaction
    
    def set_historic_transactions(self, historic_transactions: list):
        self.historic_transactions=historic_transactions
    
    def has_initialized_account(self):
        if self.account:
            if isinstance(self.account, Account):
                if self.transaction:
                    if not self.transaction.account:
                        self.transaction.account = self.account
                return True 
        return False

    def is_card_active(self):
        if self.account.active_card:
            return True
        else:
            return False

    def is_in_limit(self):
        _account_balance = self.account.available_limit
        if self.transaction.amount > _account_balance:
            return False 
        else:
            return True
    
    def in_limit_for_hight_frecuency_interval(self):
        if len(self.historic_transactions) > 1:
            _prev_two_transactions = self.historic_transactions[:2]
            _time_laps_pass_limit = _prev_two_transactions[1].time
            _current_time  = self.transaction.time
            if (_current_time - _time_laps_pass_limit) < timedelta(minutes=2):
                 return True 
        return False
    
    def in_limit_to_not_dobled_transaction(self):
        pass    
    