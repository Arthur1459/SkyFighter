import pygame
from random import shuffle, randint
import config as cf

def PlayMusic(setting):  # play music
    pygame.mixer.music.fadeout(2) # stop music which is playing
    pygame.mixer.music.unload()
    shuffle(cf.musics[setting])
    for path in cf.musics[setting]:
        pygame.mixer.music.load(path)
    if cf.sound_music:
        pygame.mixer.music.set_volume(0.5) # set the volume of the music to 0.5
    pygame.mixer.music.play(-1) # Play it indefinitely (loop)

def PlayEffect(path):
    if cf.sound_effect:
        if cf.sound_effect:
            effect = pygame.mixer.Sound(path)
            effect.set_volume(randint(3, 4)/10)
            effect.play()