from typing import List
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
        self.max_values = list(player.max_stats.values())

        # selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_select = True

        # item dimensions
        self.width, self.height = self.display_surface.get_size()
        self.width = self.width // 6
        self.height = self.height * 0.8
        self.create_items()
    
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
                # print(self.selection_index)

    def selection_cooldown(self):
        if not self.can_select:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_select = True

    def create_items(self):
        self.item_list: List[Item] = []
        for item in range(self.attribute_number):
            index = item
            # horizontal position
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_number
            left = (item * increment) + (increment - self.width) // 2

            # vertical posistion
            top = self.display_surface.get_size()[1] * 0.1

            # create object
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)


    def display(self):
        # self.display_surface.fill('black')
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):

            # get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)

class Item:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font
    
    def display(self, surface, selection_num, name, value, max_value, cost):
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
        

if __name__ == '__main__':
    from main import run_game
    run_game()
