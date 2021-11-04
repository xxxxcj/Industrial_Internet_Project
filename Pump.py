from Queue import Queue
from PumpState import PumpState
from graphviz import Graph


class Pump:
    def __init__(self, name, window_size, graph: Graph):
        self.name = name
        self.next = None
        self.state = PumpState.standing
        self.window = Queue(window_size)
        graph.node(self.name)
        self.graph = graph

    def __repr__(self):
        return self.name

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

    def renew_state(self, state: int):
        self.window.put(state)
        if self.window.full():
            s, n = self.window.is_same()
            if n == 1:
                self.state = PumpState.open
            elif n == 0:
                self.state = PumpState.close
            else:
                self.state = PumpState.uncertain

    def get_state(self):
        return self.state
