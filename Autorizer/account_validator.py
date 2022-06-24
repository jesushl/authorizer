from validator import Validator
from account import Account

# Account Violation messages
ACCOUNT_NOT_INITIALIZED="account-not-initialized"
CARD_NOT_ACTIVE = "card-not-active"

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

    def is_active(self):
        if self.account.active_card:
           return True
        else:
            self.account.add_violation(CARD_NOT_ACTIVE)
            return False 
