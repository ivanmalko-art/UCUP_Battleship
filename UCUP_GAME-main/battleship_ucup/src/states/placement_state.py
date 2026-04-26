# src/states/placement_state.py
import pygame
from src.states.base_state import BaseState
from src.core.board import Board
from src.core.ship import Ship
from config import *
from constants import SHIP_SET

class PlacementState(BaseState):
    def __init__(self, game, is_host=True):
        super().__init__(game)
        self.is_host = is_host
        super().__init__(game)
        self.player_board = Board()
        self.current_ship_index = 0
        self.current_ship = None
        self.vertical = True
        self.hover_pos = (0, 0)
        self.message = "ЛКМ — поставити | R (або р) — ПОВЕРНУТИ | ПКМ / A — авто"

        print("PlacementState запущено")
        self.next_ship()

    def next_ship(self):
        total = sum(d["count"] for d in SHIP_SET)
        if self.current_ship_index < total:
            idx = 0
            for data in SHIP_SET:
                for _ in range(data["count"]):
                    if idx == self.current_ship_index:
                        self.current_ship = Ship(data["length"], data["name"])
                        print(f"→ Наступний корабель: {self.current_ship.name}")
                        return
                    idx += 1
        else:
            from src.states.playing_state import PlayingState
            self.game.change_state(PlayingState(self.game, self.player_board))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key).lower()
            print(f"[Placement] Натиснуто: {key_name} (code: {event.key})")

            # Підтримка ВСІХ можливих варіантів R / р
            if self.current_ship and key_name in ["r", "р", "к", "g", "п"] or event.key in [pygame.K_r, 1082]:
                self.vertical = not self.vertical
                print(f"✅ ПОВОРОТ ВИКОНАНО! Вертикально = {self.vertical}")
                # Примусово оновлюємо hover
                self.update()

            if key_name in ["a", "ф"] or event.key == pygame.K_a:
                print("Авто розміщення...")
                if self.player_board.auto_place_all():
                    self.current_ship_index = sum(d["count"] for d in SHIP_SET)
                    self.next_ship()

        # Миша
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            grid_x = (mx - BOARD_OFFSET_X) // CELL_SIZE
            grid_y = (my - BOARD_OFFSET_Y) // CELL_SIZE

            if not (0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE):
                return

            if event.button == 1 and self.current_ship:   # ЛКМ
                if self.player_board.place_ship(self.current_ship, grid_x, grid_y, self.vertical):
                    self.current_ship_index += 1
                    self.next_ship()

            elif event.button == 3:  # ПКМ
                if self.player_board.auto_place_all():
                    self.current_ship_index = sum(d["count"] for d in SHIP_SET)
                    self.next_ship()

    def update(self):
        mx, my = pygame.mouse.get_pos()
        self.hover_pos = (
            (mx - BOARD_OFFSET_X) // CELL_SIZE,
            (my - BOARD_OFFSET_Y) // CELL_SIZE
        )

    def draw(self, screen):
        screen.fill(COLOR_BG)

        title_font = FONT_BIG if FONT_BIG is not None else pygame.font.SysFont("Arial", 48, bold=True)
        medium_font = FONT_MEDIUM if FONT_MEDIUM is not None else pygame.font.SysFont("Arial", 32)

        title = title_font.render("РОЗМІЩЕННЯ КОРАБЛІВ", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))

        self.draw_board(screen, self.player_board, BOARD_OFFSET_X, BOARD_OFFSET_Y)

        if self.current_ship:
            status = f"Поточний: {self.current_ship.name} ({self.current_ship.length}) — {'↑ ВЕРТИКАЛЬНО' if self.vertical else '→ ГОРИЗОНТАЛЬНО'}"
            info = medium_font.render(status, True, (255, 255, 100))
            screen.blit(info, (50, 650))

        msg = medium_font.render(self.message, True, (200, 255, 200))
        screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, 680))

    def draw_board(self, screen, board, offset_x, offset_y):
        pygame.draw.rect(screen, COLOR_WATER, (offset_x, offset_y, BOARD_SIZE*CELL_SIZE, BOARD_SIZE*CELL_SIZE))

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                rect = pygame.Rect(offset_x + x*CELL_SIZE, offset_y + y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLOR_GRID, rect, 1)
                if board.grid[y][x]:
                    pygame.draw.rect(screen, COLOR_SHIP, rect)

        if self.current_ship and self.hover_pos:
            hx, hy = self.hover_pos
            if 0 <= hx < BOARD_SIZE and 0 <= hy < BOARD_SIZE:
                for i in range(self.current_ship.length):
                    dx = 0 if self.vertical else i
                    dy = i if self.vertical else 0
                    px = hx + dx
                    py = hy + dy
                    if 0 <= px < BOARD_SIZE and 0 <= py < BOARD_SIZE:
                        s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                        s.fill((0, 255, 255, 180))
                        screen.blit(s, (offset_x + px*CELL_SIZE, offset_y + py*CELL_SIZE))
                        pygame.draw.rect(screen, (255, 255, 255),
                                       (offset_x + px*CELL_SIZE, offset_y + py*CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)