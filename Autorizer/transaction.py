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

    def __repr__(self) -> str:
        _merchant = "\"merchant\": \"{self.merchant}\", "
        _amount = "\"amount\": {self.amount}, "
        _time = "\"time\": \"{self.time}\""
        _t = _merchant + _amount + _time
        _t = _t.format(self=self)
        return "{\"transaction\": {" + _t + "}}"
    
    def __str__(self) -> str:
        _merchant = "\"merchant\": \"{self.merchant}\", "
        _amount = "\"amount\": {self.amount}, "
        _time = "\"time\": \"{self.time}\", "
        _account = "\"account\": \"{self.account}\""
        _t = _merchant + _amount + _time + _account
        _t = _t.format(self=self)
        return "{\"transaction\": {" + _t + "}}"