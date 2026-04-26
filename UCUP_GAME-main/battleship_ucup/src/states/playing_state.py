# src/states/playing_state.py
import pygame
import random
from src.states.base_state import BaseState
from src.core.board import Board
from config import *
from constants import LETTERS

class PlayingState(BaseState):
    def __init__(self, game, player_board):
        super().__init__(game)
        self.player_board = player_board
        self.enemy_board = Board()
        self.enemy_board.auto_place_all()

        self.current_player = "player"
        self.message = "Ваша черга! Клікніть по полю суперника"
        self.game_over = False
        self.winner = None

    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                from src.states.placement_state import PlacementState
                self.game.change_state(PlacementState(self.game))
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.current_player == "player":
            mx, my = pygame.mouse.get_pos()
            enemy_offset_x = BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE + 150

            grid_x = (mx - enemy_offset_x) // CELL_SIZE
            grid_y = (my - BOARD_OFFSET_Y) // CELL_SIZE

            if 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE:
                result = self.enemy_board.shoot(grid_x, grid_y)

                if result in ["hit", "sunk"]:
                    self.message = "Влучили! Додатковий хід"
                else:
                    self.message = "Мимо. Хід AI"
                    self.current_player = "ai"

                self.check_game_over()

    def update(self):
        if self.game_over:
            return
        if self.current_player == "ai":
            pygame.time.wait(400)
            self.ai_make_move()

    def ai_make_move(self):
        while True:
            x = random.randint(0, BOARD_SIZE-1)
            y = random.randint(0, BOARD_SIZE-1)
            if (x, y) not in self.player_board.shots:
                result = self.player_board.shoot(x, y)
                if result in ["hit", "sunk"]:
                    self.message = "AI влучив! AI ходить знову"
                else:
                    self.message = "AI промахнувся. Ваш хід"
                    self.current_player = "player"
                break
        self.check_game_over()

    def check_game_over(self):
        player_lost = all(ship.is_sunk() for ship in self.player_board.ships)
        enemy_lost = all(ship.is_sunk() for ship in self.enemy_board.ships)

        if player_lost:
            self.game_over = True
            self.winner = "AI"
            self.message = "💀 Ви програли... AI переміг"
        elif enemy_lost:
            self.game_over = True
            self.winner = "player"
            self.message = "ВИ ПЕРЕМОГЛИ!"

    def draw(self, screen):
        screen.fill(COLOR_BG)

        # Захист від None шрифтів
        big_font = FONT_BIG if FONT_BIG is not None else pygame.font.SysFont("Arial", 48, bold=True)
        medium_font = FONT_MEDIUM if FONT_MEDIUM is not None else pygame.font.SysFont("Arial", 32)
        small_font = FONT_SMALL if FONT_SMALL is not None else pygame.font.SysFont("Arial", 24)

        title = big_font.render("МОРСЬКИЙ БІЙ", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))

        # Поле гравця
        self.draw_board(screen, self.player_board, BOARD_OFFSET_X, BOARD_OFFSET_Y, "ВАШЕ ПОЛЕ", hide_ships=False)

        # Поле суперника
        enemy_x = BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE + 150
        self.draw_board(screen, self.enemy_board, enemy_x, BOARD_OFFSET_Y, "ПОЛЕ СУПЕРНИКА", hide_ships=True)

        # Повідомлення
        msg_color = (255, 50, 50) if self.game_over and self.winner == "AI" else (50, 255, 50)
        msg = medium_font.render(self.message, True, msg_color)
        screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, 620))

        if self.game_over:
            restart_text = medium_font.render("Натисніть R для нової гри", True, (255, 255, 100))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 670))

    def draw_board(self, screen, board, offset_x, offset_y, title_text, hide_ships=True):
        title_surf = FONT_MEDIUM.render(title_text, True, (200, 220, 255)) if FONT_MEDIUM is not None else pygame.font.SysFont("Arial", 28).render(title_text, True, (200, 220, 255))
        screen.blit(title_surf, (offset_x + 40, offset_y - 40))

        pygame.draw.rect(screen, COLOR_WATER, (offset_x, offset_y, BOARD_SIZE*CELL_SIZE, BOARD_SIZE*CELL_SIZE))

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                rect = pygame.Rect(offset_x + x*CELL_SIZE, offset_y + y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLOR_GRID, rect, 1)

                if not hide_ships and board.grid[y][x]:
                    pygame.draw.rect(screen, COLOR_SHIP, rect)

                if (x, y) in board.hits:
                    pygame.draw.rect(screen, COLOR_HIT, rect)
                elif (x, y) in board.misses:
                    pygame.draw.rect(screen, COLOR_MISS, rect)