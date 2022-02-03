from typing import List
import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups: List[pygame.sprite.Group], sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        """Create a tile

        Args:
            pos (tuple(int, int)): position x, y
            groups (List[pygame.sprite.Group]): groups that this object belongs to, or game category
            sprite_type (str): type of tile
            surface (pygame.Surface, optional): pygame.Surface of tile image. Defaults to a black square.
        """
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE)) 
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, HITBOX_OFFSET[sprite_type]) # same center, but smaller Y size

if __name__ == '__main__':
    from main import run_game
    run_game()
