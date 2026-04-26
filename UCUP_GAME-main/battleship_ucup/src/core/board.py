# src/core/board.py
from src.core.ship import Ship
from config import BOARD_SIZE
from constants import SHIP_SET

class Board:
    def __init__(self):
        self.size = BOARD_SIZE
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]  # None / Ship
        self.ships = []
        self.shots = set()          # (x,y) — зроблені постріли
        self.hits = set()
        self.misses = set()

    def can_place_ship(self, ship: Ship, start_x, start_y, vertical):
        positions = []
        for i in range(ship.length):
            x = start_x + (0 if vertical else i)
            y = start_y + (i if vertical else 0)
            if not (0 <= x < self.size and 0 <= y < self.size):
                return False
            positions.append((x, y))

        # Перевірка на перетин і дотик (навіть по діагоналі)
        for x, y in positions:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        if self.grid[ny][nx] is not None:
                            return False
        return True

    def place_ship(self, ship: Ship, start_x, start_y, vertical=True):
        if self.can_place_ship(ship, start_x, start_y, vertical):
            ship.place(start_x, start_y, vertical)
            for x, y in ship.positions:
                self.grid[y][x] = ship
            self.ships.append(ship)
            return True
        return False

    def auto_place_all(self):
        import random
        self.reset()
        for data in SHIP_SET:
            for _ in range(data["count"]):
                ship = Ship(data["length"], data["name"])
                placed = False
                attempts = 0
                while not placed and attempts < 100:
                    attempts += 1
                    x = random.randint(0, self.size - 1)
                    y = random.randint(0, self.size - 1)
                    vertical = random.choice([True, False])
                    if self.place_ship(ship, x, y, vertical):
                        placed = True
                if not placed:
                    return False  # рідко, але на всяк
        return True

    def reset(self):
        self.grid = [[None] * self.size for _ in range(self.size)]
        self.ships = []
        self.shots = set()
        self.hits = set()
        self.misses = set()

    def shoot(self, x, y):
        if (x, y) in self.shots:
            return "already"
        self.shots.add((x, y))
        for ship in self.ships:
            if ship.hit(x, y):
                self.hits.add((x, y))
                if ship.is_sunk():
                    return "sunk"
                return "hit"
        self.misses.add((x, y))
        return "miss"