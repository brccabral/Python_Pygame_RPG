import pygame
from settings import *
from player import Player

class UpgradeMenu:
    def __init__(self, player: Player):
        
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_select = True
    
    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_select:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_number - 1:
                self.selection_index += 1
                self.can_select = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index > 0 and self.attribute_number >= 1:
                self.selection_index -= 1
                self.can_select = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_select = False
                self.selection_time = pygame.time.get_ticks()
                print(self.selection_index)

    def selection_cooldown(self):
        if not self.can_select:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_select = True

    def display(self):
        self.display_surface.fill('black')
        self.input()
        self.selection_cooldown()

if __name__ == '__main__':
    from main import run_game
    run_game()
