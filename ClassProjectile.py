import pygame
import config as cf

class Projectile(pygame.sprite.Sprite):
    def __init__(self, type, coord, direction, team):
        super().__init__()
        self.type = cf.projectiles[type]
        self.visual = cf.projectiles_visual[self.type]
        self.rect = self.visual.get_rect()
        self.rect.center = coord
        self.direction = direction
        self.team = team
        self.out = False

    def Update(self):
        if self.direction == "RIGHT":
            self.rect.centerx += cf.projectiles_speed[self.type]
        if self.direction == "LEFT":
            self.rect.centerx -= cf.projectiles_speed[self.type]

        if self.rect.centerx < 0 or self.rect.centerx > cf.screenx or self.rect.centery < 0 or self.rect.centery > cf.screeny:
            self.out = True