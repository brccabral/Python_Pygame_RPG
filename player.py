from typing import List
import pygame
from settings import *
from os import walk

from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups: List[pygame.sprite.Group], obstacles_sprites: pygame.sprite.Group):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26) # same center, but smaller Y size

        # moviment
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacles_sprites = obstacles_sprites

        # graphics setup
        self.import_player_assets()
    
    def import_player_assets(self):
        character_path = 'graphics/player'
        self.animations = dict()
        _, animations, _ = next(walk(character_path))
        for animation in animations:
            for _, __, files in walk(character_path + '/' + animation):
                # print(f'{animation} {files}')
                self.animations[animation] = import_folder(character_path + '/' + animation)
        # print(self.animations)
        


    def input(self):
        keys = pygame.key.get_pressed()

        # move input
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        
        # attack input
        if keys[pygame.K_SPACE] and not self.attacking:
            print('attack')
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
        
        # magic input
        if keys[pygame.K_LCTRL] and not self.attacking:
            print('magic')
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
    
    def move(self, speed):
        # limit player speed when going diagonal
        # diagonal direction increases vector length
        # use normalize to set vector size to 1
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center
    
    def collision(self, direction: str):
        if direction == 'horizontal':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left # colliding from left to right
                    elif self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving right
                        self.hitbox.bottom = sprite.hitbox.top # colliding from left to right
                    elif self.direction.y < 0: # moving left
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.input()
        self.move(self.speed)
        self.cooldowns()

if __name__ == '__main__':
    from main import run_game
    run_game()
