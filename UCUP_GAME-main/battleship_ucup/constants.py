# constants.py
from config import BOARD_SIZE

LETTERS = "ABCDEFGHIJ"[:BOARD_SIZE]
SHIP_SET = [
    {"name": "Лінкор", "length": 4, "count": 1},
    {"name": "Крейсер", "length": 3, "count": 2},
    {"name": "Есмінець", "length": 2, "count": 3},
    {"name": "Катер", "length": 1, "count": 4},
]