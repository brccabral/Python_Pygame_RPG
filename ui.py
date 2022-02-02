from typing import List
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

        # convert weapon dict
        self.weapon_graphics: List[pygame.Surface] = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon_image = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon_image)

    def show_bar(self, current: int, max_amount: int, bg_rect: pygame.Rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # draw the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surface = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x, y = self.display_surface.get_size()
        x -= 20
        y -= 20
        text_rect = text_surface.get_rect(bottomright = (x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surface, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left: int, top: int):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index):
        bg_rect = self.selection_box(10, 630)
        weapon_surface = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surface.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_surface, weapon_rect)

    def display(self, player: Player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_index)
        self.selection_box(80, 635) # magic

if __name__ == '__main__':
    from main import run_game
    run_game()
