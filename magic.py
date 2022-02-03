from random import randint
import pygame
from settings import *
from particles import AnimationController
from player import Player


class MagicController:
    def __init__(self, animation_controller: AnimationController):
        self.animation_controller = animation_controller
        self.sounds = {
            'heal': pygame.mixer.Sound('audio/heal.wav'),
            'flame': pygame.mixer.Sound('audio/Fire.wav'),
        }

    def heal(self, player: Player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_controller.create_particles(
                'aura', player.rect.center, groups)
            self.animation_controller.create_particles(
                'heal', player.rect.center + pygame.math.Vector2(0, -60), groups)

    def flame(self, player: Player, cost, groups):
        if player.energy >= cost:
            self.sounds['flame'].play()
            player.energy -= cost
            player_direction = player.status.split('_')[0]
            if player_direction == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player_direction == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player_direction == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)
            # print(direction)
            self.animation_controller.create_particles(
                'aura', player.rect.center, groups)
            for i in range(1, 6):
                if direction.x:  # horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + \
                        randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + \
                        randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_controller.create_particles(
                        'flame', (x, y), groups)
                else:  # vertical
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + \
                        randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + \
                        randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_controller.create_particles(
                        'flame', (x, y), groups)


if __name__ == '__main__':
    from main import run_game
    run_game()
