from typing import Callable, Dict, List, Tuple
import pygame
from settings import *
from entity import Entity
from support import import_folder
from player import Player

class Enemy(Entity):
    def __init__(self, 
            monster_name: str, 
            pos: Tuple, 
            groups: List[pygame.sprite.Group], 
            obstacles_sprites: pygame.sprite.Group, 
            damage_player: Callable,
            trigger_death_particles: Callable,
            add_exp: Callable):
        """Create an enemy

        Args:
            monster_name (str): kind of monster
            pos (tuple(int,int)): position x, y
            groups (list[pygame Group]): groups that this object belongs to, or game category
            obstacles_sprites (pygame Group): group that blocks movement
            damage_player (function): callback funtion to damage player
            trigger_death_particles (function): callback function to create particles when enemy dies
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
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_cooldown = 300

        # sounds
        self.death_sound = pygame.mixer.Sound('audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.2)
        self.hit_sound.set_volume(0.2)
        self.attack_sound.set_volume(0.3)

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
        
    def find_player(self, player: Player) -> Tuple[float, pygame.math.Vector2]:
        """get players distance and direction

        Args:
            player (Player): player object

        Returns:
            tuple(float, Vector2): distance, direction
        """
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()
        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def actions(self, player: Player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
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

        if not self.vulnerable:
            # flicker
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_cooldown:
                self.vulnerable = True

    def get_damage(self, player: Player, attack_type):
        if self.vulnerable:
            self.hit_sound.play()
            self.distance, self.direction = self.find_player(player)
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player: Player):
        self.get_status(player)
        self.actions(player)

if __name__ == '__main__':
    from main import run_game
    run_game()
