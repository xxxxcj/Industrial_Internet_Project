class Queue:
    def __init__(self, max_size):
        self.li = [-1 for _ in range(max_size)]
        self.max_size = max_size
        self.pos = 0
        self.count = 0

    def put(self, n):
        self.li[self.pos] = n
        self.pos = (self.pos + 1) % self.max_size
        if self.count < self.max_size:
            self.count += 1

    def is_increasing(self):
        for i in range(1, self.max_size):
            if self.li[(self.pos - i) % self.max_size] <= self.li[(self.pos - i - 1) % self.max_size]:
                return False
        return True

    def is_decreasing(self):
        for i in range(1, self.max_size):
            if self.li[(self.pos - i) % self.max_size] >= self.li[(self.pos - i - 1) % self.max_size]:
                return False
        return True

    def full(self):
        return self.count == self.max_size

    def is_same(self):
        for i in range(self.max_size-1):
            if self.li[i] != self.li[i+1]:
                return False, -1
        return True, self.li[0]
