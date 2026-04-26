# config.py
import pygame

# ====================== НАЛАШТУВАННЯ ======================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

BOARD_SIZE = 10          # можна буде змінювати для твіку
CELL_SIZE = 45
BOARD_OFFSET_X = 100
BOARD_OFFSET_Y = 120

# Кольори
COLOR_BG = (10, 25, 45)
COLOR_WATER = (0, 80, 130)
COLOR_GRID = (200, 220, 255)
COLOR_SHIP = (180, 130, 70)
COLOR_HIT = (200, 50, 50)
COLOR_MISS = (100, 180, 255)
COLOR_SUNK = (120, 0, 0)
COLOR_HIGHLIGHT = (255, 255, 100, 80)

# Шрифти
FONT_SMALL = None
FONT_MEDIUM = None
FONT_BIG = None

# Твіки (легко вмикати/вимикати)
TWEAKS = {
    "ship_movement": False,      # перед ходом можна рухати корабель
    "board_size": 10,
    "torpedo": False,
    "ai_level": "smart",         # random / smart
}

# Звуки та музика (шляхи)
SOUNDS = {
    "shot": "assets/sounds/shot.wav",
    "hit": "assets/sounds/hit.wav",
    "sunk": "assets/sounds/sunk.wav",
    "miss": "assets/sounds/miss.wav",
    "bg_music": "assets/sounds/bg_music.ogg",
}