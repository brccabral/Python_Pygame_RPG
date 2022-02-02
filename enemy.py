import pygame
from settings import *
from entity import Entity
from support import import_folder

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.status = 'idle'
        self.import_graphics(monster_name)
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
    
    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        path = f'graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(path + animation)

if __name__ == '__main__':
    from main import run_game
    run_game()
