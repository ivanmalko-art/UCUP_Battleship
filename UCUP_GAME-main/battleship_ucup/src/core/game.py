# src/core/game.py
import pygame
from src.states.base_state import BaseState
from src.states.menu_state import MenuState
from src.network.network_manager import NetworkManager   # ← додали

from config import FONT_SMALL, FONT_MEDIUM, FONT_BIG

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.current_state: BaseState = None
        self.network = NetworkManager()   # ← мережевий менеджер

        pygame.font.init()
        global FONT_SMALL, FONT_MEDIUM, FONT_BIG
        FONT_SMALL = pygame.font.SysFont("Arial", 24)
        FONT_MEDIUM = pygame.font.SysFont("Arial", 32, bold=True)
        FONT_BIG = pygame.font.SysFont("Arial", 48, bold=True)

        self.change_state(MenuState(self))

    def change_state(self, new_state: BaseState):
        self.current_state = new_state

    def handle_event(self, event):
        if self.current_state:
            self.current_state.handle_event(event)

    def update(self):
        if self.current_state:
            self.current_state.update()

    def draw(self):
        self.screen.fill((10, 25, 45))
        if self.current_state:
            self.current_state.draw(self.screen)