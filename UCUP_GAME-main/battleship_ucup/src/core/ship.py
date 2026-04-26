# src/core/ship.py
class Ship:
    def __init__(self, length, name=""):
        self.length = length
        self.name = name
        self.positions = []      # список (x, y)
        self.hits = 0
        self.is_vertical = True

    def place(self, start_x, start_y, vertical=True):
        self.positions = []
        self.is_vertical = vertical
        for i in range(self.length):
            x = start_x + (0 if vertical else i)
            y = start_y + (i if vertical else 0)
            self.positions.append((x, y))
        return True

    def is_sunk(self):
        return self.hits >= self.length

    def hit(self, x, y):
        if (x, y) in self.positions:
            self.hits += 1
            return True
        return False