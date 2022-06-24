from os import access

class Account:
    def __init__(self, active_card: bool=None, available_limit: int=None):
        self.active_card = active_card
        self.available_limit = available_limit
        self.violations = []
        self.initialized = False
        if isinstance(active_card, bool) and isinstance(available_limit, int):
            self.initialized()

    def initialize(self):
        self.initialize = True

    def add_violations(self, violation:str)->None:
        self.violations.append(violation)
        
    def disbursment(self, amount) -> boolean:
        if amount > self.available_limit:
            return False
        elif (
                amount > self.available_limit 
                and 
                self.active_card
            ):
            self.available_limit = self.available_limit - amount

    def __repr__(self) -> str:
        _violations = '"violations": {self.violations}'.format(self=self)
        if self.initialized:
            _active = '"active-card": {self.active_card}'.format(self=self)
            _available_limit = '"available-limit": {self.available_limit}'.format(self=self)
            _account_body = _active +', ' + _available_limit 
        else:
            _account_body  = '{}'
        _account = '{"account": {' + _account_body + '}'+ ', ' + _violations + '}' 
        return _account
