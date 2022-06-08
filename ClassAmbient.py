import pygame
from random import choice, randint
import config as cf

class Artefact():
    def __init__(self, type):
        self.type = type
        if self.type == "speed_effect":
            self.visual = pygame.transform.scale(pygame.image.load(choice(cf.artefact[self.type])), (randint(8, 128)*cf.sf, 1))
            self.speed = randint(round(80*cf.sf), round(100*cf.sf))
        else:
            self.visual = pygame.transform.scale(pygame.image.load(choice(cf.artefact[self.type])), (randint(75, 256)*cf.sf, randint(50, 150)*cf.sf))
            self.speed = randint(round(5*cf.sf), round(10*cf.sf))

        self.visual.convert_alpha()
        self.visual.set_alpha(randint(32, 255))
        self.coord = [cf.screenx + self.visual.get_width(), randint(0, cf.screeny)]

    def Update(self):
        self.coord[0] -= self.speed *cf.sf


