import Pump
import Valve


class Tank:
    def __init__(self, name):
        self.name = name
        self.amount = -1
        self.next = None
        self.is_exporting = False
        self.is_importing = False

    def __repr__(self):
        return self.name + ": " + str(self.amount)

    def init(self, amount):
        self.amount = amount

    def connect(self, next):
        if self.next is None:
            self.next = next
        else:
            raise Exception(print("reconnection!!!!!!!"))

    def renew_amount(self, amount):
        if abs(amount-self.amount) < 100:
            if amount > self.amount:
                self.is_importing = True
                self.is_exporting = False
            elif amount == self.amount:
                self.is_importing = False
                self.is_exporting = False
            else:
                self.is_importing = False
                self.is_exporting = True
            self.amount = amount

    def is_exporting_state(self):
        return self.is_exporting

    def is_importing_state(self):
        return self.is_importing
