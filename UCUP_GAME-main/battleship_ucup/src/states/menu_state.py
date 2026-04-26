# src/states/menu_state.py
import pygame
from src.states.base_state import BaseState
from config import COLOR_BG, SCREEN_WIDTH, FONT_BIG, FONT_MEDIUM

class MenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.options = [
            "1. Одиночна гра (проти AI)"
        ]
        self.selected = 0

        # Захист від None шрифтів
        self.big_font = FONT_BIG if FONT_BIG is not None else pygame.font.SysFont("Arial", 48, bold=True)
        self.medium_font = FONT_MEDIUM if FONT_MEDIUM is not None else pygame.font.SysFont("Arial", 32)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.select_mode()

    def select_mode(self):
        if self.selected == 0:   # Одиночна гра
            from src.states.placement_state import PlacementState
            self.game.change_state(PlacementState(self.game))

        elif self.selected == 1:   # Hotseat
            print("Hotseat режим ще не реалізований")
            from src.states.placement_state import PlacementState
            self.game.change_state(PlacementState(self.game))

        elif self.selected == 2:   # Host
            print("Запускаємо сервер...")
            success = self.game.network.host_game(port=8080)
            if success:
                from src.states.placement_state import PlacementState
                self.game.change_state(PlacementState(self.game, is_host=True))

        elif self.selected == 3:   # Join
            ip = self.ask_for_ip()
            if ip:
                success = self.game.network.join_game(ip, port=8080)
                if success:
                    from src.states.placement_state import PlacementState
                    self.game.change_state(PlacementState(self.game, is_host=False))

    def ask_for_ip(self):
        print("\n" + "="*60)
        ip = input("Введіть IP хоста (наприклад: 192.168.0.105): ").strip()
        print("="*60)
        return ip

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(COLOR_BG)

        title = self.big_font.render("BATTLESHIP", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))

        subtitle = self.medium_font.render("UCUP-2026 Game Jam", True, (200, 220, 255))
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 160))

        for i, option in enumerate(self.options):
            color = (255, 255, 100) if i == self.selected else (200, 200, 200)
            text = self.medium_font.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 250 + i * 60))

        hint = self.medium_font.render("↑ ↓ — вибір    ENTER — підтвердити", True, (150, 150, 150))
        screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, 620))