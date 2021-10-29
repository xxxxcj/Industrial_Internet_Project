class Valve:
    def __init__(self, name):
        self.name = name
        self.switch = False
        self.next = []
        self.state_change_to_open = False

    def __repr__(self):
        return self.name + ": " + str(self.switch)

    def connect(self, next):
        if next not in self.next:
            self.next.append(next)

    def renew_switch_state(self, state: bool):
        if state != self.switch and state:
            self.state_change_to_open = True
        else:
            self.state_change_to_open = False
        self.switch = state

    def is_open(self):
        return self.switch

    def is_switch(self):
        return self.state_change_to_open