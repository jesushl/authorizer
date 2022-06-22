class Account:
    def __init__(self, active_card=False, available_limit=0):
        self.active_card = active_card
        self.available_limit = available_limit
        self.violations = []

    def add_violations(self, violation:str)->None:
        self.violations.append(violation)
        
    def disbursment(self, amount) -> boolean:
        if amount > self.available_limit:
            return False
        else:
            self.available_limit = self.available_limit - amount

    def __repr__(self) -> str:
        return """
            active: {self.active_card}
            limit: {self.available_limit}
            """.format(
            self=self
        )
