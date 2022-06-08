import pygame
import config as cf
import SoundsManagement as sm
import ClassProjectile
from random import randint, choice

class Plane(pygame.sprite.Sprite):
    def __init__(self, type, coord):
        super().__init__()
        self.type = cf.planes[type]
        self.visuals = cf.planes_visuals[self.type]
        self.visual = pygame.transform.scale(self.visuals[0], (cf.plane_width, cf.plane_height))
        self.rect = self.visual.get_rect()
        self.rect.center = coord
        self.agility = cf.planes_agility[self.type]
        self.fuel = cf.planes_fuel_capacity[self.type]
        self.life = cf.planes_life[self.type]

        self.guns = cf.planes_weapons[self.type][0]
        if self.guns != 0:
            self.gun_reloading_time = cf.planes_reloading_time[self.type][0]/self.guns
            self.gun_reload_time = pygame.time.get_ticks()

        self.missileT1_launchers = cf.planes_weapons[self.type][1]
        if self.missileT1_launchers != 0:
            self.missileT1_reloading_time = cf.planes_reloading_time[self.type][1]/self.missileT1_launchers
            self.missileT1_reload_time = pygame.time.get_ticks()

        self.missileT2_launchers = cf.planes_weapons[self.type][2]
        if self.missileT2_launchers != 0:
            self.missileT2_reloading_time = cf.planes_reloading_time[self.type][2]/self.missileT2_launchers
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

        self.laser_launchers = 0
        self.laser_reloading_time = 0.01
        self.laser_reload_time = pygame.time.get_ticks()

        self.hit = False
        self.hit_time = pygame.time.get_ticks()
        self.projectiles = []
        self.experience = 0
        self.crashed = False
        self.crashing = False

    def Update(self):

        if self.hit:
            self.visual = pygame.transform.scale(self.visuals[1], (cf.plane_width, cf.plane_height))
            self.hit_time = pygame.time.get_ticks()
            self.hit = False
        if pygame.time.get_ticks() - self.hit_time >= cf.hit_time*1000:
            self.visual = pygame.transform.scale(self.visuals[0], (cf.plane_width, cf.plane_height))

        if cf.inputs["RIGHT"] and self.rect.centerx + cf.plane_width/4 < cf.screenx:
            self.rect.centerx += self.agility
        if cf.inputs["LEFT"] and self.rect.centerx - cf.plane_width/4 > 0:
            self.rect.centerx -= self.agility
        if cf.inputs["UP"] and self.rect.centery - cf.plane_height/2 > 0:
            self.rect.centery -= self.agility
        if cf.inputs["DOWN"] and self.rect.centery + cf.plane_height < cf.screeny:
            self.rect.centery += self.agility

        if self.guns != 0:
            if cf.inputs["SPACE"] and pygame.time.get_ticks() - self.gun_reload_time > self.gun_reloading_time*1000:
                self.projectiles.append(ClassProjectile.Projectile("bullet", [self.rect.centerx + randint(-cf.accuracy[0], cf.accuracy[0]) + cf.plane_width/2, self.rect.centery + randint(-cf.accuracy[0], cf.accuracy[0])], "RIGHT", "ALLY"))
                self.gun_reload_time = pygame.time.get_ticks()
                sm.PlayEffect(choice(cf.bullet_effect))
        if self.missileT1_launchers != 0:
            if cf.inputs["SPACE"] and pygame.time.get_ticks() - self.missileT1_reload_time > self.missileT1_reloading_time*1000:
                self.projectiles.append(ClassProjectile.Projectile("missileT1", [self.rect.centerx + randint(-cf.accuracy[1], cf.accuracy[1]) + cf.plane_width/2, self.rect.centery + randint(-cf.accuracy[1], cf.accuracy[1])], "RIGHT", "ALLY"))
                self.missileT1_reload_time = pygame.time.get_ticks()
                sm.PlayEffect("sounds/missileT1.wav")
        if self.missileT2_launchers != 0:
            if cf.inputs["SPACE"] and pygame.time.get_ticks() - self.missileT2_reload_time > self.missileT2_reloading_time*1000:
                self.projectiles.append(ClassProjectile.Projectile("missileT2", [self.rect.centerx + randint(-cf.accuracy[2], cf.accuracy[2]) + cf.plane_width/2, self.rect.centery + randint(-cf.accuracy[2], cf.accuracy[2])], "RIGHT", "ALLY"))
                self.missileT2_reload_time = pygame.time.get_ticks()
                sm.PlayEffect("sounds/missileT2.wav")
        if self.missileT3_launchers != 0:
            if cf.inputs["SPACE"] and pygame.time.get_ticks() - self.missileT3_reload_time > self.missileT3_reloading_time*1000:
                self.projectiles.append(ClassProjectile.Projectile("missileT3", [self.rect.centerx + randint(-cf.accuracy[3], cf.accuracy[3]) + cf.plane_width/2, self.rect.centery + randint(-cf.accuracy[3], cf.accuracy[3])], "RIGHT", "ALLY"))
                self.missileT3_reload_time = pygame.time.get_ticks()
                sm.PlayEffect("sounds/missileT3.wav")
        if self.RocketT1_launchers != 0:
            if cf.inputs["SPACE"] and pygame.time.get_ticks() - self.RocketT1_reload_time > self.RocketT1_reloading_time*1000:
                self.projectiles.append(ClassProjectile.Projectile("RocketT1", [self.rect.centerx + randint(-cf.accuracy[4], cf.accuracy[4]) + cf.plane_width/2, self.rect.centery + randint(-cf.accuracy[4], cf.accuracy[4])], "RIGHT", "ALLY"))
                self.RocketT1_reload_time = pygame.time.get_ticks()
                sm.PlayEffect("sounds/RocketT1.wav")
        if self.bomb_launchers != 0:
            if cf.inputs["SPACE"] and pygame.time.get_ticks() - self.bomb_reload_time > self.bomb_reloading_time*1000:
                self.projectiles.append(ClassProjectile.Projectile("bomb", [self.rect.centerx + randint(-cf.accuracy[5], cf.accuracy[5]) + cf.plane_width/2, self.rect.centery + randint(-cf.accuracy[5], cf.accuracy[5])], "RIGHT", "ALLY"))
                self.bomb_reload_time = pygame.time.get_ticks()
                sm.PlayEffect("sounds/bomb.wav")
        if self.laser_launchers != 0:
            if cf.inputs["SPACE"] and pygame.time.get_ticks() - self.laser_reload_time > self.laser_reloading_time*1000:
                self.projectiles.append(ClassProjectile.Projectile("laser", [self.rect.centerx + randint(-cf.accuracy[6], cf.accuracy[6]) + cf.plane_width/2, self.rect.centery + randint(-cf.accuracy[6], cf.accuracy[6])], "RIGHT", "ALLY"))
                self.laser_reload_time = pygame.time.get_ticks()

        for projectile in self.projectiles:
            projectile.Update()
            if projectile.out:
                self.projectiles.remove(projectile)

        if self.life <= 0:
            self.rect.centery += (randint(12, 20) - self.life)*cf.sf
        if self.rect.centery - self.rect.height >= cf.screeny:
            sm.PlayEffect(choice(cf.eliminated_effect))
            self.crashed = True

        if cf.hidden is False:
            cf.enemy_target = [self.rect.centerx, self.rect.centery]

    def Upgrade(self):
        self.type += 1
        self.visuals = cf.planes_visuals[self.type]
        self.visual = pygame.transform.scale(self.visuals[0], (cf.plane_width, cf.plane_height))
        self.agility = cf.planes_agility[self.type]
        self.fuel = cf.planes_fuel_capacity[self.type]
        self.life = self.life + cf.planes_life[self.type]
        self.guns = cf.planes_weapons[self.type][0]
        self.guns = cf.planes_weapons[self.type][0]
        if self.guns != 0:
            self.gun_reloading_time = cf.planes_reloading_time[self.type][0] / self.guns
            self.gun_reload_time = pygame.time.get_ticks()

        self.missileT1_launchers = cf.planes_weapons[self.type][1]
        if self.missileT1_launchers != 0:
            self.missileT1_reloading_time = cf.planes_reloading_time[self.type][1] / self.missileT1_launchers
            self.missileT1_reload_time = pygame.time.get_ticks()

        self.missileT2_launchers = cf.planes_weapons[self.type][2]
        if self.missileT2_launchers != 0:
            self.missileT2_reloading_time = cf.planes_reloading_time[self.type][2] / self.missileT2_launchers
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

        self.experience = 0
        print("Plane Upgraded ! Plane Level : ", self.type + 1)