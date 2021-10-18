class Valve:
    def __init__(self, name):
        self.name = name
        self.switch = None
        self.next = None

    def __repr__(self):
        return self.name + ": " + str(self.switch)

    def connect(self, next):
        if self.next is None:
            self.next = next
        else:
            raise Exception(print("reconnection!!!!!!!"))

    def renew_switch_state(self, state: bool):
        self.switch = state

    def is_open(self):
        return self.switch
