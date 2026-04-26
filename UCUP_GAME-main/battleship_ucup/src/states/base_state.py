# src/states/base_state.py
import pygame
from abc import ABC, abstractmethod

class BaseState(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass