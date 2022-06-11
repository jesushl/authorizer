from abc import ABC
from abc import abstractmethod

class Validator(ABC):
    def __init__(self):
        """
        Violations store a list of messages related with 
        rules violation
        """
        self.violations = list()
    
    @abstractmethod
    def get_status(self) -> list:
        return self.violations

    @abstractmethod
    def add_violation(self, violation: str):
        self.violations.append(violation)
    
    @abstractmethod
    def verify(self):
        """
        All childs of validator should implements a method
        called verify to create procedures to add violations
        """
        return NotImplemented
