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
                self.item_list[self.selection_index].trigger(self.player)

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
    def __init__(self, left, top, width, height, index, font: pygame.font.Font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font
    
    def display_names(self, surface: pygame.Surface, name, cost, is_selected):
        color = TEXT_COLOR_SELECTED if is_selected else TEXT_COLOR
        
        # title
        title_surface = self.font.render(name, False, color)
        title_rect = title_surface.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))

        # cost
        cost_surface = self.font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surface.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))

        # draw
        surface.blit(title_surface, title_rect)
        surface.blit(cost_surface, cost_rect)

    def display_bar(self, surface: pygame.Surface, value, max_value, is_selected):
        
        # drawing setup
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if is_selected else BAR_COLOR

        # bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        # draw elements
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player: Player):
        upgrade_attributte = list(player.stats.keys())[self.index]
        
        if player.exp >= player.upgrade_cost[upgrade_attributte]:
            player.exp -= player.upgrade_cost[upgrade_attributte]
            player.stats[upgrade_attributte] *= 1.2
            player.upgrade_cost[upgrade_attributte] *= 1.4

    def display(self, surface: pygame.Surface, selection_num, name, value, max_value, cost):
        is_selected = self.index == selection_num
        if is_selected:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        self.display_names(surface, name, cost, is_selected)
        self.display_bar(surface, value, max_value, is_selected)
        

if __name__ == '__main__':
    from main import run_game
    run_game()
