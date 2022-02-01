from typing import List
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups: List[pygame.sprite.Group], obstacles_sprites: pygame.sprite.Group):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacles_sprites = obstacles_sprites
    
    def input(self):
        keys = pygame.key.get_pressed()

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
    
    def move(self, speed):
        # limit player speed when going diagonal
        # diagonal direction increases vector length
        # use normalize to set vector size to 1
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')
    
    def collision(self, direction: str):
        if direction == 'horizontal':
            for sprite in self.obstacles_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left # colliding from left to right
                    elif self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # moving right
                        self.rect.bottom = sprite.rect.top # colliding from left to right
                    elif self.direction.y < 0: # moving left
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.move(self.speed)