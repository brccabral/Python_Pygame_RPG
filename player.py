from debug import debug
from typing import Callable, Dict, List
import pygame
from entity import Entity
from settings import *
from os import walk

from support import import_folder

class Player(Entity):
    def __init__(self, pos: tuple, groups: List[pygame.sprite.Group], 
                obstacles_sprites: pygame.sprite.Group, 
                create_attack: Callable, destroy_attack: Callable,
                create_magic: Callable):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player']) # same center, but smaller Y size

        # movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacles_sprites = obstacles_sprites

        # graphics setup
        self.import_player_assets()
        self.status = 'down'

        self.switch_cooldown = 200 # same for weapon and magic

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None

        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic' : 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic' : 100, 'speed': 100}
        self.health = self.stats['health']-50
        self.energy = self.stats['energy']-10
        self.exp = 10000

        # damge timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_cooldown = 500

        # import a sound
        self.weapon_attack_sound = pygame.mixer.Sound('audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

    def import_player_assets(self):
        character_path = 'graphics/player'
        self.animations: Dict[str, List[pygame.Surface]] = dict()
        _, animations, _ = next(walk(character_path))
        for animation in animations:
            for _, __, files in walk(character_path + '/' + animation):
                # print(f'{animation} {files}')
                self.animations[animation] = import_folder(character_path + '/' + animation)
        # print(self.animations)
        
    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def animate(self):
        animations = self.animations[self.status]
        
        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animations):
            self.frame_index = 0
        
        # set the image
        self.image = animations[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker if hit
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def input(self):
        if self.attacking:
            return
        
        keys = pygame.key.get_pressed()

        # move input
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0
        
        # attack input
        if keys[pygame.K_SPACE]:
            # print('attack')
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()
            self.weapon_attack_sound.play()
        
        # magic input
        if keys[pygame.K_LCTRL]:
            # print('magic')
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            style = list(magic_data.keys())[self.magic_index]
            strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
            cost = list(magic_data.values())[self.magic_index]['cost']
            self.create_magic(style, strength, cost)
        
        # change weapon
        if keys[pygame.K_q] and self.can_switch_weapon: 
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            if self.weapon_index >= len(list(weapon_data.keys())) - 1:
                self.weapon_index = 0
            else:
                self.weapon_index += 1
            self.weapon = list(weapon_data.keys())[self.weapon_index]

        # change magic
        if keys[pygame.K_e] and self.can_switch_magic: 
            self.can_switch_magic = False
            self.magic_switch_time = pygame.time.get_ticks()
            if self.magic_index >= len(list(magic_data.keys())) - 1:
                self.magic_index = 0
            else:
                self.magic_index += 1
            self.magic = list(magic_data.keys())[self.magic_index]

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()
        
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_cooldown:
                self.can_switch_weapon = True
        
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_cooldown:
                self.can_switch_magic = True
        
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_cooldown:
                self.vulnerable = True
    
    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['attack']
        magic_damage = magic_data[self.magic]['strength']
        return base_damage + magic_damage

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def update(self):
        self.input()
        self.move(self.stats['speed'])
        self.cooldowns()
        self.get_status()
        self.animate()
        self.energy_recovery()
        # debug(self.status)

if __name__ == '__main__':
    from main import run_game
    run_game()
