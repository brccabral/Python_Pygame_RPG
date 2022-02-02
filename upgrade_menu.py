import pygame
from settings import *
from player import Player

class UpgradeMenu:
    def __init__(self, player: Player):
        
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
    
    def display(self):
        self.display_surface.fill('black')

if __name__ == '__main__':
    from main import run_game
    run_game()
