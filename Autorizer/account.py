
class Account:
    def __init__(self, active_card: bool=None, available_limit: int=None):
        self.active_card = active_card
        self.available_limit = available_limit
        self.violations = []
        self.initialized = False
        # This can be fixed in a database adding a hash token
        self.is_metadata_copy = False 
        if isinstance(active_card, bool) and isinstance(available_limit, int):
            self.initialize()
    
    def metadata_copy(self):
        _copy_account_metadata = Account(
            active_card=self.active_card, 
            available_limit=self.available_limit
        )
        return _copy_account_metadata

    def initialize(self):
        self.initialized = True

    def add_violation(self, violation:str)->None:
        self.violations.append(violation)
        
    def disbursment(self, amount) -> bool:
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


def account_from_dict(
    account:dict,
    active_card_key: str='active-card',
    available_limit_key: str='available-limit'
):
    return Account(
        active_card=account.get(active_card_key, None),
        available_limit=account.get(available_limit_key, None)
    )
