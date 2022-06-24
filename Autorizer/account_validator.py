from validator import Validator
from account import Account

# Account validation messages
ACCOUNT_NOT_INITIALIZED="account-not-initialized"

class AccountValidator(Validator):
    def __init__(self):
        super().__init__()
        self.account: Account = None

    def verify(self):
        """
        This method apply a list of verifications to implement
        and error messages
        """
        validators = {self.is_valid_account: "account-not-initialized"}
        for validator in validators:
            _ = validator()
            if _:
                self.violations.append(validators[validator])
        return self.violations

    def is_valid_account(self):
        if self.account:
            if isinstance(self.account, Account):
                return True
        return False

    def is_initiated(self):
        if self.is_valid_account():
            if self.account.initialized:
                return True 
        self.account.add_violation(ACCOUNT_NOT_INITIALIZED)
        return False
