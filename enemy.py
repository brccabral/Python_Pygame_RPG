from typing import Dict, List
import pygame
from settings import *
from entity import Entity
from support import import_folder
from player import Player

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacles_sprites):
        """Create an enemy

        Args:
            monster_name (str): kind of monster
            pos (tuple(int,int)): position x, y
            groups (list[pygame Group]): groups that this object belongs to, or game category
            obstacles_sprites (pygame Group): [description]
        """

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

        # player interation
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400

    def import_graphics(self, name):
        self.animations: Dict[str, List[pygame.Surface]] = {'idle': [], 'move': [], 'attack': []}
        path = f'graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(path + animation)

    def get_status(self, player: Player):
        distance, direction = self.find_player(player)

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
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
        self.animate()
        self.cooldowns()

    def actions(self, player: Player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
        elif self.status == 'move':
            self.distance, self.direction = self.find_player(player)
        else:
            self.direction = pygame.math.Vector2()
    
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def cooldowns(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

    def enemy_update(self, player: Player):
        self.get_status(player)
        self.actions(player)

if __name__ == '__main__':
    from main import run_game
    run_game()
