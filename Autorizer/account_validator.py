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
        validators = {self.not_exists_a_valid_account: "account-not-initialized"}
        for validator in validators:
            _ = validator()
            if _:
                self.violations.append(validators[validator])
        return self.violations

    def not_exists_a_valid_account(self):
        if self.account:
            if isinstance(self.account, Account):
                return False
        return True
