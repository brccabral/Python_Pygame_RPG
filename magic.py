import pygame
from settings import *
from particles import AnimationController

class MagicController:
    def __init__(self, animation_controller: AnimationController):
        self.animation_controller = animation_controller
    
    def heal(self):
        pass

    def flame(self):
        pass

if __name__ == '__main__':
    from main import run_game
    run_game()
