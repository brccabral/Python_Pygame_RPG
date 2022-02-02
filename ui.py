import pygame
from settings import *
from player import Player

class UI():
    def __init__(self):
        
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def display(self, player: Player):
        pygame.draw.rect(self.display_surface, 'black', self.health_bar_rect)

if __name__ == '__main__':
    from main import run_game
    run_game()
