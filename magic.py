import pygame
from settings import *
from particles import AnimationController
from player import Player

class MagicController:
    def __init__(self, animation_controller: AnimationController):
        self.animation_controller = animation_controller
    
    def heal(self, player: Player, strength, cost, groups):
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_controller.create_particles('aura', player.rect.center, groups)
            self.animation_controller.create_particles('heal', player.rect.center + pygame.math.Vector2(0, -60), groups)

    def flame(self):
        pass

if __name__ == '__main__':
    from main import run_game
    run_game()
