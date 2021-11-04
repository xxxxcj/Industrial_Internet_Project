import Pump
import Valve
from TankState import TankState
from Queue import Queue
from graphviz import Graph


class Tank:
    def __init__(self, name, window_size, graph: Graph):
        self.name = name
        self.next = None
        self.state = TankState.standing
        self.window = Queue(window_size)
        graph.node(self.name, shape='rect')
        self.graph = graph

    def __repr__(self):
        return self.name + ": " + str(self.state)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        ascii_sum = 0
        for ch in self.name:
            ascii_sum += ord(ch)
        return ascii_sum

    def connect(self, next):
        if self.next is None:
            self.next = next
            self.graph.edge(self.name, next.name)
        elif self.next == next:
            pass
        else:
            raise Exception(print("reconnection!!!!!!!"))

    def renew_amount(self, amount):
        self.window.put(amount)
        if not self.window.full():
            self.state = TankState.standing
        else:
            same, n = self.window.is_same()
            if self.window.is_increasing():
                self.state = TankState.importing
            elif self.window.is_decreasing():
                self.state = TankState.exporting
            elif same:
                self.state = TankState.standing
            else:
                self.state = TankState.uncertain

    def get_state(self):
        return self.state
