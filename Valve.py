from Queue import Queue
from ValveState import ValveState
from graphviz import Graph


class Valve:
    def __init__(self, name, window_size, graph:Graph):
        self.name = name
        self.next = []
        self.state = ValveState.standing
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
        if next not in self.next:
            self.next.append(next)
            self.graph.edge(self.name, next.name)

    def renew_state(self, state: int):
        self.window.put(state)
        if self.window.full():
            s, n = self.window.is_same()
            if n == 1:
                self.state = ValveState.open
            elif n == 0:
                self.state = ValveState.close
            else:
                self.state = ValveState.uncertain

    def get_state(self):
        return self.state
