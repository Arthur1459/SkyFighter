import pygame, time, ClassPlane, ClassEnemy, ClassExplosion, ClassExpOrb, ClassAmbient, ClassPowers, ClassProjectile
import config as cf
import SoundsManagement as sm
from random import randint, choice

def main():

    ## ---------------- Initialisation ----------------- ##
    pygame.mixer.pre_init(44100, 16, 24)
    pygame.mixer.set_num_channels(32)
    pygame.init()

    clock = pygame.time.Clock()

    logo = pygame.image.load("visuals/GUI/logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("SkyFighter")

    screen = pygame.display.set_mode((cf.screenx, cf.screeny))

    if cf.start is False:
        startMenu(screen, clock)
        return

    fighter = ClassPlane.Plane("T1", cf.start_place)
    enemies = [ClassEnemy.Plane("T1")]
    explosion = []
    xp_orbs = []
    artefacts = []
    artefacts_before = []

    cf.score = 0
    cf.generation_time = 5
    cf.powers_unlocked = []
    cf.backcolor = [100, 100, 255]

    new_enemy_time = pygame.time.get_ticks()
    new_point_time = pygame.time.get_ticks()

    print("Game Started !", time.process_time(), "s")

    running = True
    sm.PlayMusic(1)

    nb_frames = 1
    time_fps = pygame.time.get_ticks()

    ## ---------------- Main Loop ----------------- ##
    while running:
        clock.tick(30)  # number of fps , update per seconds
        nb_frames += 1
        if nb_frames > 10000000:
            nb_frames = 1
            time_fps = pygame.time.get_ticks()
        fps = round((nb_frames/((pygame.time.get_ticks() - time_fps + 1)))*1000, 3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                Save()
            if event.type == pygame.MOUSEBUTTONUP:
                print(pygame.mouse.get_pos())
                sm.PlayEffect("sounds/selected.wav")
                cf.inputs["CLICK"] = True
                fighter.experience += 50   # Cheats
                cf.score += 50
            else:
                cf.inputs["CLICK"] = False

        getInputs()   # Get keyboard inputes
        if cf.inputs["ESCAPE"]:
            startMenu(screen, clock)
            return
        Calculation(fighter, enemies, explosion, xp_orbs, artefacts, artefacts_before)    # Calculation (collision, update...)

        if fighter.life <= 0:     # test if alive
            if randint(0, 1) == 1:
                explosion.append(ClassExplosion.Explosion((fighter.rect.centerx + randint(round(-15 * cf.sf),round(5 * cf.sf)),fighter.rect.centery + randint(round(-15 * cf.sf),round(5 * cf.sf)))))
                sm.PlayEffect("sounds/crash1.wav")
            if fighter.crashing is False:
                xp_orbs.append(ClassExpOrb.ExpOrb(randint(2, 5) + enemy.type, enemy.rect.center))
                fighter.crashing = True
            if fighter.rect.centery - fighter.rect.height >= cf.screeny:
                if cf.score > cf.best_score:
                    cf.best_score = cf.score
                print("You have lost.")
                sm.PlayEffect("sounds/gamelost.wav")
                startMenu(screen, clock)
                return

        for enemy in enemies:
            if enemy.life <= 0:
                if randint(0,1) == 1:
                    explosion.append(ClassExplosion.Explosion((enemy.rect.centerx + randint(round(-15*cf.sf), round(5*cf.sf)), enemy.rect.centery + randint(round(-15*cf.sf), round(5*cf.sf)))))
                if enemy.crashing is False:
                    if fighter.type < 7:
                        xp_orbs.append(ClassExpOrb.ExpOrb(randint(2, 5) + enemy.type, enemy.rect.center))
                    enemy.crashing = True
                if enemy.crashed:
                    cf.score += enemy.type + 1
                    enemies.remove(enemy)
                    cf.backcolor[0] += randint(20, 250)
                    cf.backcolor[1] += randint(-100, 0)
                    cf.backcolor[2] += randint(-200, -50)
                    if cf.backcolor[0] > 255: cf.backcolor[0] = 255
                    if cf.backcolor[1] < 0: cf.backcolor[1] = 0
                    if cf.backcolor[2] < 0: cf.backcolor[2] = 0

        DisplayUpdate(screen, fighter, enemies, explosion, xp_orbs, artefacts, artefacts_before, fps)   # ----- screen Update -------

        if pygame.time.get_ticks() - new_enemy_time > cf.generation_time*1000:
            if randint(0, 1) == 0 and cf.score < 100 and len(enemies) < cf.max_enemies:
                enemies.append(ClassEnemy.Plane("T1"))
            if randint(0, 3) == 0 and 10 < cf.score < 150 and len(enemies) < cf.max_enemies:
                enemies.append(ClassEnemy.Plane("T2"))
            if randint(0, 3) == 0 and 20 < cf.score < 200 and len(enemies) < cf.max_enemies:
                enemies.append(ClassEnemy.Plane("T3"))
            if randint(0, 3) == 0 and 50 < cf.score < 500 and len(enemies) < cf.max_enemies:
                enemies.append(ClassEnemy.Plane("T4"))
            if randint(0, 3) == 0 and 100 < cf.score < 800 and len(enemies) < cf.max_enemies:
                enemies.append(ClassEnemy.Plane("T5"))
            if randint(0, 3) == 0 and 200 < cf.score < 1000 and len(enemies) < cf.max_enemies:
                enemies.append(ClassEnemy.Plane("T6"))
            if randint(0, 3) == 0 and 450 < cf.score and len(enemies) < cf.max_enemies:
                enemies.append(ClassEnemy.Plane("T7"))
            if randint(0, 3) == 0 and 900 < cf.score and len(enemies) < cf.max_enemies:
                enemies.append(ClassEnemy.Plane("T8"))
            new_enemy_time = pygame.time.get_ticks()
            if cf.generation_time > 0.25:
                cf.generation_time = cf.generation_time*0.98
            if cf.max_enemy_add < cf.score:
                cf.max_enemy_add += 500
                cf.max_enemies += 1

        if pygame.time.get_ticks() - new_point_time > cf.generation_time*1000:
            cf.score += 1
            new_point_time = pygame.time.get_ticks()

        PlaneUpgrade(fighter)
        SettingsUpdate()

def Calculation(fighter, enemies, explosion, xp_orbs, artefacts, artefacts_before):
    fighter.Update()
    for enemy in enemies:
        enemy.Update()
    for orb in xp_orbs:
        orb.Update()
        if orb.rect.colliderect(fighter.rect):
            fighter.experience += orb.xp_amount
            sm.PlayEffect(choice(cf.xp_effect))
            xp_orbs.remove(orb)

    for enemy in enemies:
        for projectile in enemy.projectiles:
            if fighter.rect.colliderect(projectile.rect) and cf.hidden == False:
                fighter.life -= cf.projectile_damage[projectile.type]
                fighter.hit = True
                sm.PlayEffect(choice(cf.explosions_effect))
                enemy.projectiles.remove(projectile)
                explosion.append(ClassExplosion.Explosion(projectile.rect.center))
    for enemy in enemies:
        for projectile in fighter.projectiles:
            if enemy.rect.colliderect(projectile):
                enemy.life -= cf.projectile_damage[projectile.type]
                enemy.hit = True
                xp_orbs.append(ClassExpOrb.ExpOrb(randint(1, 3), enemy.rect.center))
                sm.PlayEffect(choice(cf.explosions_effect))
                fighter.projectiles.remove(projectile)
                explosion.append(ClassExplosion.Explosion(projectile.rect.center))
        for laser in cf.laser:
            if enemy.rect.colliderect(laser):
                enemy.life -= cf.projectile_damage[laser.type]
                enemy.hit = True
                xp_orbs.append(ClassExpOrb.ExpOrb(randint(1, 3), enemy.rect.center))
                sm.PlayEffect(choice(cf.explosions_effect))
                explosion.append(ClassExplosion.Explosion(enemy.rect.center))

    for Explosion in explosion:
        Explosion.Update()
        if Explosion.ended:
            explosion.remove(Explosion)

    if cf.details:
        if randint(0,2) == 1:
            artefacts.append(ClassAmbient.Artefact("speed_effect"))
        if randint(0, 20) == 1:
            artefacts.append(ClassAmbient.Artefact("cloud"))
            if randint(0,1) == 1:
                artefacts_before.append((ClassAmbient.Artefact("cloud")))

        for artefact in artefacts:
            artefact.Update()
            if artefact.coord[0] + artefact.visual.get_width() < 0:
                artefacts.remove(artefact)
        for artefact in artefacts_before:
            artefact.Update()
            if artefact.coord[0] + artefact.visual.get_width() < 0:
                artefacts_before.remove(artefact)

    for power in cf.powers_unlocked:
        power.Update()
        if power.name == "ultrafire":
            if power.isOn == 1:
                fighter.gun_reloading_time = cf.planes_reloading_time[fighter.type][0]/(12)
            else:
                fighter.gun_reloading_time = cf.planes_reloading_time[fighter.type][0]/fighter.guns
        if power.name == "phantom":
            if power.isOn == 1:
                cf.hidden = True
                fighter.visual = fighter.visual.convert_alpha()
                fighter.visual.set_alpha(50)
            else:
                cf.hidden = False
                fighter.visual =  pygame.transform.scale(fighter.visuals[0], (cf.plane_width, cf.plane_height))
                cf.life_base_phantom = 0
        if power.name == "laser":
            if power.isOn  == 1:
                cf.laser.append(ClassProjectile.Projectile("laser", [fighter.rect.centerx + cf.plane_width/2 + cf.projectiles_size[6][0]/2, fighter.rect.centery], "RIGHT", "ALLY"))
                power.isOn = 2
                sm.PlayEffect("sounds/Laser.wav")
            if len(cf.laser) != 0 and power.isOn == 3:
                cf.laser = []

    if cf.backcolor[0] < 100:
        cf.backcolor[0] += randint(-1, 4)
    if cf.backcolor[0] > 100:
        cf.backcolor[0] += randint(-4, 1)
    if cf.backcolor[1] < 100:
        cf.backcolor[1] += randint(-1, 4)
    if cf.backcolor[1] > 100:
        cf.backcolor[1] += randint(-4, 1)
    if cf.backcolor[2] < 255:
        cf.backcolor[2] += randint(-1, 4)
    if cf.backcolor[2] > 255:
        cf.backcolor[2] = 255

    for number in range(len(cf.backcolor)):
        if cf.backcolor[number] > 255:
            cf.backcolor[number] = 255
        if cf.backcolor[number] < 0:
            cf.backcolor[number] = 0


def DisplayUpdate(screen, fighter, enemies, explosion, xp_orbs, artefacts, artefacts_before, fps):
    screen.fill(pygame.Color(cf.backcolor))
    Text(("FPS : " + str(fps)), (cf.screenx - 128 * cf.sf, cf.screeny - 32 * cf.sf), round(12 * cf.sf), "black", screen)
    if cf.details:
        for artefact in artefacts:
            screen.blit(artefact.visual, artefact.coord)
    screen.blit(fighter.visual, [fighter.rect.centerx - cf.plane_width/2, fighter.rect.centery - cf.plane_height/2])
    for orb in xp_orbs:
        screen.blit(orb.visual, orb.rect.center)
    for enemy in enemies:
        screen.blit(enemy.visual, [enemy.rect.centerx - cf.plane_width/2, enemy.rect.centery - cf.plane_height/2])
        Text(str(enemy.life), [enemy.rect.centerx + cf.plane_width*cf.sf/6, enemy.rect.centery - cf.plane_height*cf.sf/1.8], 12, "black", screen)
        for projectile in enemy.projectiles:
            screen.blit(projectile.visual, [projectile.rect.centerx - cf.projectiles_size[projectile.type][0]/2, projectile.rect.centery - cf.projectiles_size[projectile.type][1]/2])
    for projectile in fighter.projectiles:
        screen.blit(pygame.transform.flip(projectile.visual, True, False), [projectile.rect.centerx - cf.projectiles_size[projectile.type][0]/2, projectile.rect.centery - cf.projectiles_size[projectile.type][1]/2])
    for laser in cf.laser:
        screen.blit(pygame.transform.flip(laser.visual, True, False), [laser.rect.centerx - cf.projectiles_size[laser.type][0]/2, laser.rect.centery - cf.projectiles_size[laser.type][1]/2])
    for Explosion in explosion:
        screen.blit(pygame.transform.scale(Explosion.visual, (randint(round(20*cf.sf), round(60*cf.sf)), randint(round(20*cf.sf), round(60*cf.sf)))), Explosion.coord)
    screen.blit(fighter.visual, [fighter.rect.centerx - cf.plane_width/2, fighter.rect.centery - cf.plane_height/2])
    Text("you", (fighter.rect.centerx - fighter.rect.width/4, fighter.rect.centery - fighter.rect.height/2), 12, "green", screen)
    if cf.details:
        for artefact in artefacts_before:
            screen.blit(artefact.visual, artefact.coord)
    Text("Status : " + str(fighter.life) + " / " + str(cf.planes_life[fighter.type]), (10, 10), round(24*cf.sf), "red", screen)
    Text("Score : " + str(cf.score), (cf.screenx*0.80, 10), round(24*cf.sf), "orange", screen)
    if fighter.type < 7:
        Text("XP : " + str(fighter.experience) + "/" + str(cf.plane_experience_by_lvl[fighter.type]), (cf.screenx/2.3, round(18*cf.sf)), round(30*cf.sf), "blue", screen)
    else:
        Text("XP : MAXED", (cf.screenx/2.3, round(18*cf.sf)), round(30*cf.sf), "blue", screen)
    for power in range(len(cf.powers_unlocked)):
        screen.blit(cf.powers_unlocked[power].visual, (round(42*(power+1)*cf.sf), round(cf.screeny - 64*cf.sf))) #
        if cf.powers_unlocked[power].time_left != cf.powers_unlocked[power].reloading_time:
            Text(str(round(cf.powers_unlocked[power].time_left/1000)), (round(42*(power+1)*cf.sf + 2*cf.sf), round(cf.screeny - 64*cf.sf)), round(16*cf.sf), "white", screen)
        Text(str(cf.powers_inputs[cf.powers_unlocked[power].type]), (round((42*(power+1)*cf.sf + 4*cf.sf)), round(cf.screeny - 32*cf.sf)), round(12*cf.sf), "black", screen)
    pygame.display.update()

def PlaneUpgrade(fighter):
    if fighter.type < 7:
        if fighter.experience >= cf.plane_experience_by_lvl[fighter.type]:
            sm.PlayEffect("sounds/lvlup.wav")
            fighter.Upgrade()
            if fighter.type > 2 and len(cf.powers_unlocked) == 0 :
                cf.powers_unlocked.append(ClassPowers.Power("ultrafire"))
            if fighter.type > 4 and len(cf.powers_unlocked) == 1 :
                cf.powers_unlocked.append(ClassPowers.Power("phantom"))
            if fighter.type > 6 and len(cf.powers_unlocked) == 2 :
                cf.powers_unlocked.append(ClassPowers.Power("laser"))

def getInputs():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        cf.inputs["RIGHT"] = True
    else:
        cf.inputs["RIGHT"] = False
    if keys[pygame.K_LEFT] or keys[pygame.K_q]:
        cf.inputs["LEFT"] = True
    else:
        cf.inputs["LEFT"] = False
    if keys[pygame.K_UP] or keys[pygame.K_z]:
        cf.inputs["UP"] = True
    else:
        cf.inputs["UP"] = False
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        cf.inputs["DOWN"] = True
    else:
        cf.inputs["DOWN"] = False
    if keys[pygame.K_SPACE]:
        cf.inputs["SPACE"] = True
    else:
        cf.inputs["SPACE"] = False
    if keys[pygame.K_ESCAPE]:
        cf.inputs["ESCAPE"] = True
    else:
        cf.inputs["ESCAPE"] = False
    if keys[pygame.K_i]:
        cf.inputs["I"] = True
    else:
        cf.inputs["I"] = False
    if keys[pygame.K_o]:
        cf.inputs["O"] = True
    else:
        cf.inputs["O"] = False
    if keys[pygame.K_u]:
        cf.inputs["U"] = True
    else:
        cf.inputs["U"] = False
    if keys[pygame.K_e]:
        cf.inputs["E"] = True
    else:
        cf.inputs["E"] = False
    if keys[pygame.K_r]:
        cf.inputs["R"] = True
    else:
        cf.inputs["R"] = False
    if keys[pygame.K_f]:
        cf.inputs["F"] = True
    else:
        cf.inputs["F"] = False

def Text(msg, coord, size, color, screen): # blit to the screen a text
    TextColor = pygame.Color(color) # set the color of the text
    font = pygame.font.Font("visuals/SPACE.ttf", size) # set the font
    return screen.blit(font.render(msg, True, TextColor), coord) # return and blit the text on the screen

def Save():
    data = open('data.txt', 'r')
    datas = data.readlines()
    old_score = int(datas[0])
    data.close()
    if cf.best_score > old_score:
        data = open("data.txt", 'w')
        datas[0] = str(cf.best_score)
        data.truncate()
        data.writelines(datas)
        data.close()

def SettingsUpdate():
    if pygame.time.get_ticks() - cf.settings_updated > 400:
        if cf.details and cf.inputs["U"]:
            cf.details = False
            cf.settings_updated = pygame.time.get_ticks()
        elif cf.details is False and cf.inputs["U"]:
            cf.details = True
            cf.settings_updated = pygame.time.get_ticks()
        if cf.sound_music and cf.inputs["I"]:
            cf.sound_music = False
            pygame.mixer.music.set_volume(0)
            cf.settings_updated = pygame.time.get_ticks()
        elif cf.sound_music is False and cf.inputs["I"]:
            cf.sound_music = True
            pygame.mixer.music.set_volume(0.5)
            cf.settings_updated = pygame.time.get_ticks()
        if cf.sound_effect and cf.inputs["O"]:
            cf.sound_effect = False
            cf.settings_updated = pygame.time.get_ticks()
        elif cf.sound_effect is False and cf.inputs["O"]:
            cf.sound_effect = True
            cf.settings_updated = pygame.time.get_ticks()


def startMenu(screen, clock):

    Save()
    running = True
    artefacts = []
    MenuDisplayUpdate(screen, artefacts)
    pygame.time.delay(500)
    sm.PlayMusic(0)

    while running:
        clock.tick(30)  # number of fps , update per seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                Save()
            if event.type == pygame.MOUSEBUTTONUP:
                print(pygame.mouse.get_pos())
                cf.inputs["CLICK"] = True
                sm.PlayEffect("sounds/selected.wav")
                cf.start = True
                main()
                return
            else:
                cf.inputs["CLICK"] = False

        getInputs()
        if cf.inputs["ESCAPE"]:
            running = False
        if cf.inputs["SPACE"]:
            sm.PlayEffect("sounds/selected.wav")
            cf.start = True
            main()
            return

        if cf.details:
            if randint(0, 20) == 1:
                artefacts.append(ClassAmbient.Artefact("cloud"))
            for artefact in artefacts:
                artefact.Update()
                if artefact.coord[0] + artefact.visual.get_width() < 0:
                    artefacts.remove(artefact)

        MenuDisplayUpdate(screen, artefacts)
        SettingsUpdate()


def MenuDisplayUpdate(screen, artefacts):
    screen.fill(pygame.Color(100, 100, 255))
    if cf.details:
        for artefact in artefacts:
            screen.blit(artefact.visual, artefact.coord)
    Text("SKYFIGHTER", (cf.screenx /4.8 + 150*cf.sf, cf.screeny / 3), round(45*cf.sf), "red", screen)
    Text("You are in the Menu", (cf.screenx/4.8, cf.screeny/2.3), round(45*cf.sf), "black", screen)
    Text("Click to Play or press SPACE", (cf.screenx/14, cf.screeny/2.3 + 50*cf.sf), round(45*cf.sf), "white", screen)
    Text("Best Score : " + str(cf.best_score), (cf.screenx /4.8 + 100*cf.sf, cf.screeny / 2.3 + 100*cf.sf), round(45*cf.sf), "grey", screen)
    Text("Score : " + str(cf.score), (cf.screenx / 4.8 + 170 * cf.sf, cf.screeny / 2.3 + 150 * cf.sf),round(60 * cf.sf), "orange", screen)
    Text("Press ESCAPE to QUIT", (10, 10), round(20*cf.sf), "black", screen)
    Text("Settings :", (cf.screenx*0.65, 10*cf.sf), round(24 * cf.sf), "black", screen)
    if cf.sound_effect:
        Text("Press O : SFX (ON)", (cf.screenx * 0.65, 40*cf.sf), round(20 * cf.sf), "black", screen)
    else:
        Text("Press O : SFX (OFF)", (cf.screenx * 0.65, 40*cf.sf), round(20 * cf.sf), "black", screen)
    if cf.sound_music:
        Text("Press I : Music (ON)", (cf.screenx * 0.65, 70*cf.sf), round(20 * cf.sf), "black", screen)
    else:
        Text("Press I : Music (OFF)", (cf.screenx * 0.65, 70*cf.sf), round(20 * cf.sf), "black", screen)
    if cf.details:
        Text("Press U : Details (ON)", (cf.screenx * 0.65, 100*cf.sf), round(20 * cf.sf), "black", screen)
    else:
        Text("Press U : Details (OFF)", (cf.screenx * 0.65, 100*cf.sf), round(20 * cf.sf), "black", screen)
    Text("Controls : ARROWS / ZQSD to move and SPACE to shoot", (0 + round(16 * cf.sf), cf.screeny*0.95), round(16 * cf.sf), "black", screen)
    Text("Arthur1459", (cf.screenx*0.85, cf.screeny*0.95),round(16 * cf.sf), "black", screen)
    pygame.display.update()

if __name__ == "__main__" :  # begin the main function
    print("Program started !", time.process_time(), "s")
    main()