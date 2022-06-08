import pygame
import config as cf
import SoundsManagement as sm
import ClassProjectile
from random import randint, choice

class Plane(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        sm.PlayEffect(choice(cf.planes_effect))
        self.type = cf.planes[type]
        self.visuals = cf.planes_visuals[self.type]
        self.visual = pygame.transform.flip(pygame.transform.scale(self.visuals[0], (cf.plane_width, cf.plane_height)), True, False)
        self.rect = self.visual.get_rect()
        self.rect.center = [cf.screenx + cf.plane_width, randint(32, round(cf.screeny - 32))]
        self.agility = round(cf.planes_agility[self.type]*0.6)
        self.fuel = cf.planes_fuel_capacity[self.type]
        self.life = round(cf.planes_life[self.type]*0.2)
        self.guns = cf.planes_weapons[self.type][0]
        if self.guns != 0:
            self.gun_reloading_time = cf.planes_reloading_time[self.type][0]
            self.gun_reload_time = pygame.time.get_ticks()
        self.missileT1_launcher = cf.planes_weapons[self.type][1]
        if self.missileT1_launcher != 0:
            self.missileT1_reloading_time = cf.planes_reloading_time[self.type][1]
            self.missileT1_reload_time = pygame.time.get_ticks()
        self.missileT2_launcher = cf.planes_weapons[self.type][2]
        if self.missileT2_launcher != 0:
            self.missileT2_reloading_time = cf.planes_reloading_time[self.type][2]
            self.missileT2_reload_time = pygame.time.get_ticks()
        self.missileT3_launchers = cf.planes_weapons[self.type][3]
        if self.missileT3_launchers != 0:
            self.missileT3_reloading_time = cf.planes_reloading_time[self.type][3] / self.missileT3_launchers
            self.missileT3_reload_time = pygame.time.get_ticks()

        self.RocketT1_launchers = cf.planes_weapons[self.type][4]
        if self.RocketT1_launchers != 0:
            self.RocketT1_reloading_time = cf.planes_reloading_time[self.type][4] / self.RocketT1_launchers
            self.RocketT1_reload_time = pygame.time.get_ticks()

        self.bomb_launchers = cf.planes_weapons[self.type][5]
        if self.bomb_launchers != 0:
            self.bomb_reloading_time = cf.planes_reloading_time[self.type][5] / self.bomb_launchers
            self.bomb_reload_time = pygame.time.get_ticks()
        self.projectiles = []
        self.patterny = 0
        self.patternx = 0
        self.ready = False
        self.hit = False
        self.hit_time = pygame.time.get_ticks()
        self.crashing = False
        self.crashed = False

    def Update(self):
        if self.ready:

            self.patterny += randint(-1, 2)
            if self.patterny > 1:
                self.rect.centery += self.agility
            elif self.patterny < -1:
                self.rect.centery -= self.agility
            if self.rect.centery <= cf.plane_height:
                self.patterny = 1
            elif self.rect.centery >= cf.screeny - cf.plane_height:
                self.patterny = -1

            self.patternx += randint(-1, 1)
            if self.patternx > 2:
                self.rect.centerx += self.agility
            elif self.patternx < -2:
                self.rect.centerx -= self.agility * 1.5
            if self.rect.centerx <= cf.plane_width:
                self.patternx = 2
            elif self.rect.centerx >= cf.screenx - cf.plane_width:
                self.patternx = -2

            if self.rect.centery < cf.enemy_target[1]:
                self.patterny += 1
            elif self.rect.centery > cf.enemy_target[1]:
                self.patterny -= 1
            if self.rect.centery < cf.enemy_target[0]:
                self.patternx += 2


            if self.guns != 0:
                if randint(0, 10) == 0 and pygame.time.get_ticks() - self.gun_reload_time > self.gun_reloading_time * 1000:
                    self.projectiles.append(ClassProjectile.Projectile("bullet", [self.rect.centerx + randint(-cf.accuracy[0], cf.accuracy[0]) - cf.plane_width/2, self.rect.centery + randint(-cf.accuracy[0], cf.accuracy[0])], "LEFT", "ENEMY"))
                    self.gun_reload_time = pygame.time.get_ticks()
                    sm.PlayEffect(choice(cf.bullet_effect))
            if self.missileT1_launcher != 0:
                if randint(0, 10) == 0 and pygame.time.get_ticks() - self.missileT1_reload_time > self.missileT1_reloading_time * 1000:
                    self.projectiles.append(ClassProjectile.Projectile("missileT1", [self.rect.centerx + randint(-cf.accuracy[1], cf.accuracy[1]) + cf.plane_width/2, self.rect.centery + randint(-cf.accuracy[1], cf.accuracy[1])], "LEFT", "ENEMY"))
                    self.missileT1_reload_time = pygame.time.get_ticks()
                    sm.PlayEffect("sounds/missileT1.wav")
            if self.missileT2_launcher != 0:
                if randint(0, 10) == 0 and pygame.time.get_ticks() - self.missileT2_reload_time > self.missileT2_reloading_time * 1000:
                    self.projectiles.append(ClassProjectile.Projectile("missileT2", [self.rect.centerx + randint(-cf.accuracy[2], cf.accuracy[2]) + cf.plane_width/2, self.rect.centery + randint(-cf.accuracy[2], cf.accuracy[2])], "LEFT", "ENEMY"))
                    self.missileT2_reload_time = pygame.time.get_ticks()
                    sm.PlayEffect("sounds/missileT2.wav")
            if self.missileT3_launchers != 0:
                if randint(0, 10) == 0 and pygame.time.get_ticks() - self.missileT3_reload_time > self.missileT3_reloading_time * 1000:
                    self.projectiles.append(ClassProjectile.Projectile("missileT3", [self.rect.centerx + randint(-cf.accuracy[3], cf.accuracy[3]) + cf.plane_width / 2,self.rect.centery + randint(-cf.accuracy[3], cf.accuracy[3])], "LEFT", "ENEMY"))
                    self.missileT3_reload_time = pygame.time.get_ticks()
                    sm.PlayEffect("sounds/missileT3.wav")
            if self.RocketT1_launchers != 0:
                if randint(0, 10) == 0 and pygame.time.get_ticks() - self.RocketT1_reload_time > self.RocketT1_reloading_time * 1000:
                    self.projectiles.append(ClassProjectile.Projectile("RocketT1", [self.rect.centerx + randint(-cf.accuracy[4], cf.accuracy[4]) + cf.plane_width / 2,self.rect.centery + randint(-cf.accuracy[4], cf.accuracy[4])], "LEFT", "ENEMY"))
                    self.RocketT1_reload_time = pygame.time.get_ticks()
                    sm.PlayEffect("sounds/RocketT1.wav")
            if self.bomb_launchers != 0:
                if randint(0, 10) == 0 and pygame.time.get_ticks() - self.bomb_reload_time > self.bomb_reloading_time * 1000:
                    self.projectiles.append(ClassProjectile.Projectile("bomb", [self.rect.centerx + randint(-cf.accuracy[5], cf.accuracy[5]) + cf.plane_width / 2,self.rect.centery + randint(-cf.accuracy[5], cf.accuracy[5])], "LEFT", "ENEMY"))
                    self.bomb_reload_time = pygame.time.get_ticks()
                    sm.PlayEffect("sounds/bomb.wav")


            for projectile in self.projectiles:
                projectile.Update()
                if projectile.out:
                    self.projectiles.remove(projectile)

            if self.life <= 0:
                self.rect.centery += (randint(10, 20) - self.life)*cf.sf
            if self.rect.centery - self.rect.height >= cf.screeny:
                sm.PlayEffect(choice(cf.eliminated_effect))
                self.crashed = True


        else:
            self.rect.centerx += self.agility
            if self.rect.centerx >= cf.plane_width*2:
                self.ready = True

        if self.hit:
            self.visual = pygame.transform.flip(pygame.transform.scale(self.visuals[1], (cf.plane_width, cf.plane_height)), True, False)
            self.hit_time = pygame.time.get_ticks()
            self.hit = False
        if pygame.time.get_ticks() - self.hit_time >= cf.hit_time*1000:
            self.visual = pygame.transform.flip(pygame.transform.scale(self.visuals[0], (cf.plane_width, cf.plane_height)), True, False)