from datetime import datetime


from datetime import datetime

# models
from account import Account


class Transaction:
    def __init__(
        self, merchant: str = "", amount: int = 0, time: datetime = datetime.now()
    ):
        self.merchant = merchant
        self.amount = amount
        self.time = time
        self.account = None

    def set_account(self, account: Account):
        self.account = account
