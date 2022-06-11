from xmlrpc.client import boolean


class Account():
    def __init__(self, active_card=False, available_limit=0):
        self.active_card= active_card
        self.available_limit = available_limit
    
    def disbursment(self, amount)->boolean:
        if amount > self.available_limit:
            return False 
        else:
            self.available_limit = self.available_limit - amount
    