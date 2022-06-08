import pygame, linecache
pygame.init()

## Screen
w_factor = pygame.display.Info().current_w/1280
h_factor = pygame.display.Info().current_h/700
if w_factor < h_factor:
    screen_factor = w_factor
else:
    screen_factor = h_factor

#screen_factor = 1   # Manualy
sf = screen_factor
screenx, screeny = round(1280*screen_factor), round(700*screen_factor)

## Planes
plane_width, plane_height = 96*screen_factor, 48*screen_factor
planes = {"T1":0, "T2":1, "T3":2, "T4":3, "T5":4, "T6":5, "T7":6, "T8":7}
planes_visuals = [[pygame.image.load("visuals/planes/plane1.png"), pygame.image.load("visuals/planes/plane1_hit.png")], [pygame.image.load("visuals/planes/plane2.png"), pygame.image.load("visuals/planes/plane2_hit.png")], [pygame.image.load("visuals/planes/plane3.png"), pygame.image.load("visuals/planes/plane3_hit.png")], [pygame.image.load("visuals/planes/plane4.png"), pygame.image.load("visuals/planes/plane4_hit.png")], [pygame.image.load("visuals/planes/plane5.png"), pygame.image.load("visuals/planes/plane5_hit.png")], [pygame.image.load("visuals/planes/plane6.png"), pygame.image.load("visuals/planes/plane6_hit.png")], [pygame.image.load("visuals/planes/plane7.png"), pygame.image.load("visuals/planes/plane7_hit.png")], [pygame.image.load("visuals/planes/plane8.png"), pygame.image.load("visuals/planes/plane8_hit.png")]]
#[bullet, missileT1, T2, T3, RocketT1, bomb]
planes_weapons = [[1, 0, 0, 0, 0, 0], [2, 1, 0, 0, 0, 0], [3, 1, 1, 0, 0, 0], [4, 2, 1, 0, 0, 0], [4, 3, 2, 0, 0, 0], [4, 4, 3, 0, 0, 0], [1, 4, 4, 1, 3, 0], [1, 5, 5, 2, 4, 1]]
planes_reloading_time = [[1, 3, 5, 7, 3, 10], [1, 3, 5, 7, 3, 10], [1, 3, 5, 7, 3, 10], [1, 3, 5, 7, 3, 10],[1, 3, 5, 7, 3, 10], [1, 3, 5, 7, 3, 10], [1, 3, 5, 7, 3, 10], [1, 3, 5, 7, 3, 10]]
planes_life = [10, 15, 20, 30, 40, 50, 75, 100]
planes_fuel_capacity = [30, 40, 50, 60, 70, 80, 90, 100]
planes_agility = [5*sf, 7*sf, 9*sf, 11*sf, 13*sf, 15*sf, 18*sf, 18*sf]
hit_time = 0.2

## Projectile
projectiles = {"bullet":0, "missileT1":1, "missileT2":2, "missileT3":3, "RocketT1":4, "bomb":5, "laser":6}
projectiles_size = [[16*sf, 8*sf], [32*sf, 16*sf], [48*sf, 24*sf], [55*sf, 28*sf], [44*sf, 18*sf], [64*sf, 32*sf], [screenx, 24*sf]]
projectiles_visual = [pygame.transform.scale(pygame.image.load("visuals/Projectiles/bullet.png"), projectiles_size[0]), pygame.transform.scale(pygame.image.load("visuals/Projectiles/missileT1.png"), projectiles_size[1]), pygame.transform.scale(pygame.image.load("visuals/Projectiles/missileT2.png"), projectiles_size[2]), pygame.transform.scale(pygame.image.load("visuals/Projectiles/missileT3.png"), projectiles_size[3]), pygame.transform.scale(pygame.image.load("visuals/Projectiles/RocketT1.png"), projectiles_size[4]), pygame.transform.scale(pygame.image.load("visuals/Projectiles/bomb.png"), projectiles_size[5]), pygame.transform.scale(pygame.image.load("visuals/Projectiles/laser.png"), projectiles_size[6])]
projectiles_speed = [25*sf, 20*sf, 15*sf, 14*sf, 28*sf, 10*sf, 0*sf]
accuracy = [round(5*sf), round(3*sf), round(2*sf), round(2*sf), round(0*sf), round(5*sf), round(0*sf)]
projectile_damage = [1, 5, 10, 15, 4, 20, 50]

explosions = [pygame.image.load("visuals/Projectiles/explosion1.png"), pygame.image.load("visuals/Projectiles/explosion2.png"), pygame.image.load("visuals/Projectiles/explosion3.png"), pygame.image.load("visuals/Projectiles/explosion4.png"), pygame.image.load("visuals/Projectiles/explosion5.png"), pygame.image.load("visuals/Projectiles/explosion6.png")]

# Powers
powers = {"ultrafire":0, "phantom":1, "laser":2}
powers_inputs = ["E", "R", "F"]
icons = [[pygame.image.load("visuals/GUI/powers/UltraFire_ready.png"), pygame.image.load("visuals/GUI/powers/UltraFire_reloading.png")], [pygame.image.load("visuals/GUI/powers/Phantom_ready.png"), pygame.image.load("visuals/GUI/powers/Phantom_reloading.png")], [pygame.image.load("visuals/GUI/powers/laser_ready.png"), pygame.image.load("visuals/GUI/powers/laser_reloading.png")]]
powers_reloading_time = [10, 14, 10]
powers_duration = [4, 4, 0.3]

## inGame settings
start_place = [screenx/4, screeny/2]
musics = [["musics/menu.wav"],["musics/MEKANIC.wav", "musics/Axe.wav", "musics/Carcharok.wav", "musics/Gemini.wav"]]
sound_music = True
eliminated_effect = ["sounds/crash1.wav"]
explosions_effect = ["sounds/explosion1.wav", "sounds/explosion2.wav", "sounds/explosion3.wav", "sounds/explosion4.wav", ]
bullet_effect = ["sounds/bullet1.wav", "sounds/bullet2.wav", "sounds/bullet3.wav"]
planes_effect = ["sounds/plane1.wav", "sounds/plane2.wav", "sounds/plane3.wav",]
xp_effect = ["sounds/xp1.wav", "sounds/xp2.wav"]
sound_effect = True
plane_experience_by_lvl = [10, 25, 50, 100, 200, 400, 800, "no limit !"]
max_enemies = 16
max_enemy_add = 1000
details = True
settings_updated = pygame.time.get_ticks()

## Artefact/Ambient
speed_effect = ["visuals/artefact/speed1.png", "visuals/artefact/speed2.png"]
cloud_effect = ["visuals/artefact/cloud1.png", "visuals/artefact/cloud2.png", "visuals/artefact/cloud3.png", "visuals/artefact/cloud4.png"]
artefact = {"speed_effect":speed_effect, "cloud":cloud_effect}

## cache
inputs = {"RIGHT":False, "LEFT":False, "UP":False, "DOWN":False, "SPACE":False, "CLICK":False, "ESPCAPE":False, "O":False, "I":False, "U":False, "F":False, "G":False, "H":False}
generation_time = 5
enemy_target = [screeny/2, 0]
powers_unlocked = []
hidden = False
laser = []
data = open("data.txt", 'r')
best_score = int(data.readlines()[0])
data.close()
score = 0
start = False
backcolor = [100, 100, 255]
color_momentum = -2
