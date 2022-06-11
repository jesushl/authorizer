from validator import Validator
from account import Account

class AccountValidator(Validator):
    def __init__(self):
        super().__init__()
        self.account = None
        
    def verify(self):
        """
        This method apply a list of verifications to implement
        and error messages 
        """
        validators = {
            self.exists_a_valid_account: "account-not-initialized"
        }
        for validator in validators:
            if validator():
                self.violations.append(validators[validator])

    def exists_a_valid_account(self):
        if self.account:
            if isinstance(self.account, Account):
                return True
        return False
