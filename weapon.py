import pygame
from player import Player

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player: Player, groups):
        super().__init__(groups)
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center = player.rect.center)

if __name__ == '__main__':
    from main import run_game
    run_game()
