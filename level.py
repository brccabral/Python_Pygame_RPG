from random import choice, randint
from debug import debug
import pygame
from particles import AnimationController
from settings import *
from support import import_csv_layout, import_folder
from tile import Tile
from player import Player
from ui import UI
from weapon import Weapon
from enemy import Enemy
from magic import MagicController

class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

        # particles
        self.animation_controller = AnimationController()
        self.magic_controller = MagicController(self.animation_controller)
    
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
                            Tile(
                                (x,y), 
                                [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites], 
                                'grass', 
                                random_grass_image)
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
                                if   column == '390': monster_name = 'bamboo'
                                elif column == '391': monster_name = 'spirit'
                                elif column == '392': monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                enemy = Enemy(
                                            monster_name, 
                                            (x, y), 
                                            [self.visible_sprites, self.attackable_sprites], 
                                            self.obstacles_sprites,
                                            self.damge_player,
                                            self.trigger_death_particles)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_controller.heal(self.player, strength, cost, [self.visible_sprites])
        elif style == 'flame':
            pass

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3,6)):
                                self.animation_controller.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        elif target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damge_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # spawn particles
            self.animation_controller.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_controller.create_particles(particle_type, pos, [self.visible_sprites])

    def run(self):
        # update and draw the level
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
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

    def enemy_update(self, player: Player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') if sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

if __name__ == '__main__':
    from main import run_game
    run_game()
