from typing import Dict, List
import pygame
from settings import *
from entity import Entity
from support import import_folder
from player import Player

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacles_sprites):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.status = 'idle'
        self.import_graphics(monster_name)
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacles_sprites = obstacles_sprites

		# stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

    def import_graphics(self, name):
        self.animations: Dict[str, List[pygame.Surface]] = {'idle': [], 'move': [], 'attack': []}
        path = f'graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(path + animation)

    def get_status(self, player: Player):
        distance, direction = self.find_player(player)

        if distance <= self.attack_radius:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
        
    def find_player(self, player: Player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()
        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def update(self):
        self.move(self.speed)
    
    def enemy_update(self, player: Player):
        self.get_status(player)

if __name__ == '__main__':
    from main import run_game
    run_game()
