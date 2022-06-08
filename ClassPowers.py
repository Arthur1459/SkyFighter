import pygame
import config as cf
import SoundsManagement as sm

class Power():
    def __init__(self, name):
        self.name = name
        self.type = cf.powers[self.name]
        self.icons = cf.icons[self.type]
        self.visual = pygame.transform.scale(self.icons[1], (32*cf.sf, 32*cf.sf))
        self.reloading_time = cf.powers_reloading_time[self.type] * 1000
        self.isReady = False
        self.isOn = 3
        self.time_left = self.reloading_time
        self.reload = pygame.time.get_ticks()
        self.input = cf.powers_inputs[self.type]
        self.power_start_time = None
        self.power_duration = cf.powers_duration[self.type] * 1000

    def Update(self):
        if self.isReady is False:
            self.time_left = self.reloading_time - (pygame.time.get_ticks() - self.reload)
            if self.time_left <= 0:
                self.time_left = self.reloading_time
                self.isReady = True
                self.visual = pygame.transform.scale(self.icons[0], (32 * cf.sf, 32 * cf.sf))

        if self.isReady is True and cf.inputs[self.input]:
            if self.name == "ultrafire":
                sm.PlayEffect("sounds/ultrafire.wav")
            if self.name == "phantom":
                sm.PlayEffect("sounds/phantom.wav")
            if self.name == "laser":
                sm.PlayEffect("sounds/laser.wav")
            self.isOn = 1
            self.isReady = False
            self.reload = pygame.time.get_ticks()
            self.power_start_time = pygame.time.get_ticks()
            self.visual = pygame.transform.scale(self.icons[1], (32 * cf.sf, 32 * cf.sf))

        if self.isOn == 1 or self.isOn == 2:
            if self.power_duration < pygame.time.get_ticks() - self.power_start_time:
                self.isOn = 3
                if self.name == "phantom":
                    sm.PlayEffect("sounds/phantom_off.wav")