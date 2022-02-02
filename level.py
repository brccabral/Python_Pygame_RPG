from random import choice
from debug import debug
import pygame
from settings import *
from support import import_csv_layout, import_folder
from tile import Tile
from player import Player
from ui import UI
from weapon import Weapon
from enemy import Enemy

class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
    
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv'),
        }
        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for column_index, column in enumerate(row):
                    if column != '-1':
                        x = column_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacles_sprites], 'invisible')
                        elif style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y), [self.visible_sprites, self.obstacles_sprites], 'grass', random_grass_image)
                        elif style == 'object':
                            obj_surface = graphics['objects'][int(column)]
                            Tile((x,y), [self.visible_sprites, self.obstacles_sprites], 'object', obj_surface)
                        elif style == 'entities':
                            if column == '394':
                                self.player = Player(
                                                (x, y), 
                                                [self.visible_sprites], 
                                                self.obstacles_sprites, 
                                                self.create_attack, 
                                                self.destroy_attack,
                                                self.create_magic)
                            else:
                                enemy = Enemy('monster', (x, y), [self.visible_sprites])

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def create_magic(self, style, strength, cost):
        print(f'{style=}')
        print(f'{strength=}')
        print(f'{cost=}')

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        # update and draw the level
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)
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

        # creating the floor
        self.floor_surface = pygame.image.load('graphics/tilemap/ground.png').convert_alpha()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
    
    def custom_draw(self, player: Player):

        # get the offset from player's current position
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # move all sprites accordingly to player position
        # sorted makes sure that sprites on top of the screen 
        # are drawn behind 
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

if __name__ == '__main__':
    from main import run_game
    run_game()
