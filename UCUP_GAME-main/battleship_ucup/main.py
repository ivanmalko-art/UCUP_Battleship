# main.py
import pygame
import sys
from src.core.game import Game
import sys
import os

def resource_path(relative_path):
    """Получает правильный путь и в разработке, и в .exe"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Battleship UCUP-2026")
    clock = pygame.time.Clock()

    game = Game(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()