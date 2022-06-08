import pygame
from random import randint
import config as cf

class ExpOrb(pygame.sprite.Sprite):
    def __init__(self, xp_amount, coord):
        super().__init__()
        self.visual = pygame.transform.scale(pygame.image.load("visuals/Projectiles/xp_orb.png"), (8*(xp_amount/2)*cf.sf, 8*(xp_amount/2)*cf.sf))
        self.rect = self.visual.get_rect()
        self.rect.center = coord
        self.xp_amount = xp_amount
        self.taken = False

    def Update(self):
        self.rect.centerx -= randint(0, 15)
        self.rect.centery += randint(-10, 10)