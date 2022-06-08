import pygame
import config as cf
from random import choice, randint

class Explosion():
    def __init__(self, coord):
        self.visual = pygame.transform.scale(choice(cf.explosions), (round(8*randint(3, 8)*cf.sf), round(8*randint(3, 8)*cf.sf)))
        self.coord = coord
        self.explode_time = randint(2, 5)/10
        self.ended = False
        self.start_time = pygame.time.get_ticks()

    def Update(self):
        if pygame.time.get_ticks() - self.start_time > self.explode_time:
            self.ended = True