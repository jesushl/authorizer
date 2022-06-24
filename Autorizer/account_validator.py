from validator import Validator
from account import Account

# Account Violation messages
ACCOUNT_ALREADY_INITIALIZED = "account-already-initialized"

class AccountValidator(Validator):
    def __init__(self):
        super().__init__()
        self.account: Account = None
        self.meta_account = None # transitory object to get log messages

    def verify(self):
        """
        This method apply a list of verifications to implement
        and error messages
        """
        self.meta_account = self.account.metadata_copy()
        self.is_already_initiated()
        return self.meta_account

    def is_valid_account(self):
        if self.meta_account:
            if isinstance(self.meta_account, Account):
                return True
        return False

    def is_already_initiated(self):
        if self.is_valid_account():
            if self.meta_account.initialized:
                self.meta_account.add_violation(ACCOUNT_ALREADY_INITIALIZED)
                return True 
        return False
