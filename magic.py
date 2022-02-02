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

    def flame(self):
        pass

if __name__ == '__main__':
    from main import run_game
    run_game()
