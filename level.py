from debug import debug
import pygame
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.create_map()
    
    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for column_index, column in enumerate(row):
                x = column_index * TILESIZE
                y = row_index * TILESIZE
                if column == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
                elif column == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites)


    def run(self):
        # update and draw the level
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        # debug(self.player.direction)

class YSortCameraGroup(pygame.sprite.Group):
    # overlap objects in Y corrdinate to create sense of depth

    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width, self.half_height = self.display_surface.get_size()
        self.half_width, self.half_height = self.half_width//2, self.half_height//2
        # offset is used to move the sprite to a new position
        self.offset = pygame.math.Vector2()
    
    def custom_draw(self, player: Player):

        # get the offset from player's current position
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # move all sprites accordingly to player position
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
