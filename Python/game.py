#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, sys, math, os
from random import randint, choice
from Resources.scripts.Maps import *
from Resources.scripts.Menus import *            
from Resources.scripts.Guns import *
from Resources.scripts.Player import *
from Resources.scripts.Enemy import *
from Resources.scripts.Online import *
from Resources.scripts.Creator import *
from Resources.scripts.Campaign import *
from threading import Thread

#fix __file__ error when compiled into exe
if getattr(sys, 'frozen', False):
    __file__ = os.path.join(os.path.dirname(sys.executable), "game.py")

#set icon
icon = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Resources', 'images', '')+'icon.png')
pygame.display.set_icon(icon)

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()    
pygame.init()
running = True
screen = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()
FPS = 60


"""sorry for using global variables, just call this so much that it makes it easier"""
def titlescreen_menu(start_at=None):
    global reloading, semiauto
    global enemy_hit, kills, deaths, hit, shot, internalclock
    global setup, maps, loadouts, player, player_gun
    global enemy_gun, enemy_player, loadout_number, campaign_text_check
    global background, in_between_shots, first_run, enemy_gun_online, enemy_pos_backup
    enemy_pos = None
    first_run = True
    reloading = semiauto = False
    campaign_text_check = []
    kills = deaths = shot = internalclock = 0 
    try:
        setup = Setup(setup.map_choice, setup.custom)
    except:
        setup = Setup()
    maps = Maps(0, 0)
    if start_at == "start":
        Menu([]).TitleScreen()
    loadouts = Loadouts(False)
    player = Player()
    player_gun = Gun()
    player.update_rank(kills)
    setup.MainMenu(start_at)
    
    if setup.campaign:
        enemy_pos_backup = maps.enemy_pos(setup.map_choice)
        setup.enemies = len(enemy_pos_backup)
    
    if setup.online:
        hit = 0
        enemy_hit = 0
        
        enemy_player = enemy_gun = online_mode(setup.map_choice, setup.max_kills)
        while True:
            if enemy_player.stop_all:
                if enemy_player.joins:
                    enemy_player = enemy_gun = online_mode(setup.map_choice, setup.max_kills, True)
                else:
                    enemy_player = enemy_gun = online_mode(setup.map_choice, setup.max_kills)
            else:
                break
        
        
            
        setup.map_choice = enemy_player.online_map_choice
        setup.max_kills = enemy_gun.online_max_kills
        
        try:
            maps.background_color(setup.map_choice)
        except ValueError: #host is using custom map
            setup.custom = True
        
        if enemy_player.back:
            titlescreen_menu()
    else:
        hit = []
        enemy_hit = []
        for i in range(0, setup.enemies):
            hit.append(0)
            enemy_hit.append(0)
    
    if setup.custom:
        maps = Play_Maps(setup.map_choice)
        player = Player(setup.map_choice)
    
    if setup.online:
        try:
            loadout_number, enemy_gun_online = Loadouts(False).display_loadout(enemy_player.c, "client")
        except:
            loadout_number, enemy_gun_online = Loadouts(False).display_loadout(enemy_player.s, "server")
    elif setup.campaign:
        loadout_number = "LOADOUT 6"
    else:
        loadout_number = Loadouts(False).display_loadout()
    setup.guns(loadout_number)
    setup.perks(loadout_number)
    maps.spawn_area(setup.map_choice)
    
    
    if not setup.online:
        enemy_gun = []
        enemy_player = []
        for i in range(0, setup.enemies):
            enemy_gun.append(Enemy_Gun())
            enemy_player.append(Enemy(maps.spawnX, maps.spawnY, loadout_number, enemy_gun[i]))

    background = pygame.Surface(screen.get_size())
    background.fill(maps.background_color(setup.map_choice))
    background = background.convert()

    player.spawn(maps.spawnX, maps.spawnY, setup.map_choice)
    
    in_between_shots = False
    
    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Resources', 'sounds', '')+'gamemusic.wav')
    pygame.mixer.music.play(-1)
            
titlescreen_menu("start")
while running:
    
    if setup.online:
        if enemy_player.titlescreen:
            Menu([]).end_screen(kills, deaths)
            player.update_rank(kills)
            titlescreen_menu("multiplayer")
        try:
            if enemy_player.stop_all:
                continue
        except:
            pass
    else:
        pass
        """#MY GUESS IS THIS IS HIGHLY UNESSECARRY AND ILL REMOVE IT LATER
        for i in range(0, setup.enemies):
            if enemy_player[i].titlescreen:
                Menu([]).end_screen(kills, deaths)
                player.update_rank(kills)
                titlescreen_menu()
    
        for i in range(0, setup.enemies):
            if enemy_player[i].stop_all:
                continue"""
    
    mousepos = pygame.mouse.get_pos()
    clock.tick(FPS)
    internalclock += 1
    
    
    #player.test(mousepos)
    

    #updating collisions based on our position
    if setup.custom:
        collision_list = maps.map_collisions_update(player.imagesx, player.imagesy) 
    else:
        collision_list = map_collisions_update(player.imagesx, player.imagesy, setup.map_choice)    
  
    #player gun
    if setup.online:
        hit_enemy = player_gun.enemy_collide(collision_list, pygame.Rect((enemy_player.enemyposX - player.imagesx, enemy_player.enemyposY - player.imagesy), enemy_player.backup.get_size()))   
        if hit_enemy:
            enemy_player.health -= 100 / setup.stk 
            if enemy_player.health <= 0:
                player.shotrise_list = player.shotrun_list = player.backup_shotrise = player.backup_shotrun = []
                #hit = 0
                kills += 1
                if kills >= setup.max_kills:
                    try:
                        enemy_player.c.close()
                    except:
                        enemy_player.s.close()
                    while enemy_player.online_paused:
                        pass
                    Menu([]).end_screen(kills, deaths)
                    player.update_rank(kills)
                    titlescreen_menu("multiplayer")
    else:
        hit_enemy = []
        for i in range(0, setup.enemies):
            hit_enemy.append(False)
        for i in range(0, setup.enemies):
            hit_enemy[i] = player_gun.enemy_collide(collision_list, pygame.Rect((enemy_player[i].enemyposX - player.imagesx, enemy_player[i].enemyposY - player.imagesy), enemy_player[i].backup.get_size()))   
            if hit_enemy[i]:
                enemy_player[i].health -= 100 / setup.stk
                if enemy_player[i].health <= 0:
                    if setup.campaign:
                        enemy_player[i].enemyposX = 100000000
                    else:
                        enemy_gun[i] = Enemy_Gun()
                        enemy_player[i] = Enemy(maps.spawnX, maps.spawnY, loadout_number, enemy_gun[i])
                    #hit[i] = 0
                    kills += 1
                    if kills >= setup.max_kills:
                        if setup.campaign:
                            titlescreen_menu("campaign")
                        else:
                            Menu([]).end_screen(kills, deaths)
                            player.update_rank(kills)
                            titlescreen_menu("multiplayer")
    
    #Checking for our shot's collisions with the wall
    player_gun.wall_collide(collision_list)
  
    #enemy gun
    if setup.online:
        if enemy_gun.collide_you(collision_list):
            player.health -= 100 / enemy_player.enemy_stk
            if player.health <= 0:
                if not enemy_player.online_paused:
                    try:
                        Menu([]).killed(enemy_player.name, enemy_player.c, "client")
                    except:
                        Menu([]).killed(enemy_player.name, enemy_player.s, "server")
                #enemy_hit = 0
                if setup.custom:
                    player = Player(setup.map_choice)
                else:
                    player = Player()
                player.spawn(maps.spawnX, maps.spawnY, setup.map_choice)
                deaths += 1
                if deaths >= setup.max_kills:
                    try:
                        enemy_player.c.close()
                    except:
                        enemy_player.s.close()
                    while enemy_player.online_paused:
                        pass
                    Menu([]).end_screen(kills, deaths)
                    player.update_rank(kills)
                    titlescreen_menu("multiplayer")
            
            #updating our loadout if we changed it at the pause menu
                try:
                    new_setup = enemy_player.new_setup
                    online = setup.online
                    custom = setup.custom
                    setup = new_setup
                    setup.online = online
                    setup.custom = custom
                    del(new_setup)
                    loadout_number = setup.loadout_number
                    gun = setup.gun
  
                    enemy_player.send_receive(setup.stk, player.angle, player.imagesx, player.imagesy, player_gun.shotrise_list, player_gun.shotrun_list, gun)
                except:
                    pass
                reloading = False
                shot = 0
    else:
        for i in range(0, setup.enemies):
            if enemy_gun[i].collide_you(collision_list):
                player.health -= 100 / enemy_player[i].enemy_stk
                #enemy_hit[i] += 1
                """for b in range(0, setup.enemies):
                    if enemy_player[b].enemy_stk > enemy_hit[b] + 1 and b != i:
                        enemy_hit[b] += 1 #shot from anyone causes damage for everyone"""
                if player.health <= 0:
                    if setup.campaign:
                        Menu([]).killed(campaign=True)
                        question = Menu([]).yes_no(" RESTART MISSION?", no="NO,EXIT")
                        if question == "yes":
                           titlescreen_menu("campaign_continue")
                        else:
                            titlescreen_menu("campaign")
                            break
                    else:
                        Menu([]).killed()
                    
                    enemy_hit = []
                    for c in range(0, setup.enemies):
                        enemy_hit.append(0)
                    if setup.custom:
                        player = Player(setup.map_choice)
                    else:
                        player = Player()
                    player.spawn(maps.spawnX, maps.spawnY, setup.map_choice)
                    deaths += 1
                    for b in range(0, setup.enemies):
                        enemy_gun[b].enemy_shotrun_list = []
                        enemy_gun[b].enemy_shotrise_list = []
                        enemy_gun[b].enemy_backup_shotrun = []
                        enemy_gun[b].enemy_backup_shotrise = []
                    reloading = False
                    shot = 0
                    if deaths >= setup.max_kills:
                        if setup.campaign:
                            titlescreen_menu("campaign")
                        else:
                            Menu([]).end_screen(kills, deaths)
                            player.update_rank(kills)
                            titlescreen_menu("multiplayer")
            
            #updating our loadout if we changed it at the pause menu
                    try:
                        online = setup.online
                        custom = setup.custom
                        setup = new_setup
                        setup.online = online
                        setup.custom = custom
                        del(new_setup)
                        loadout_number = setup.loadout_number
                        gun = setup.gun
                    except:
                        pass

    if setup.online:
        #sending gun model to other player if online and on first run
        if first_run:
            setup.guns(loadout_number, player.angle)
            first_run = False
            gun = setup.gun
            enemy_player.send_receive(setup.stk, player.angle, player.imagesx, player.imagesy,  player_gun.shotrise_list, player_gun.shotrun_list, gun)
        
        try:    
            endcheck = enemy_player.send_receive(setup.stk, player.angle, player.imagesx, player.imagesy,  player_gun.shotrise_list, player_gun.shotrun_list, enemy_gun=enemy_gun_online) #means we are playing online
            del(enemy_gun_online)
        except:
            endcheck = enemy_player.send_receive(setup.stk, player.angle, player.imagesx, player.imagesy,  player_gun.shotrise_list, player_gun.shotrun_list)
        if endcheck:
            try:
                enemy_player.c.close()
            except:
                pass
            try:
                enemy_player.s.close() 
            except:
                pass 
            endcheck = None
            while enemy_player.online_paused:
                pass
            Menu([]).end_screen(kills, deaths)
            player.update_rank(kills)
            titlescreen_menu("multiplayer")
    else:
        for i in range(0, setup.enemies):
            if setup.campaign:
                try:
                    if (840 > enemy_pos_backup[i][0] - player.imagesx > -200 and 680 > enemy_pos_backup[i][1] - player.imagesy > -200):
                        enemy_player[i].AI(player.imagesx, player.imagesy, collision_list, loadout_number, internalclock, enemy_pos_backup[i], setup.map_choice)
                except:
                    pass
            else:
                enemy_player[i].AI(player.imagesx, player.imagesy, collision_list, loadout_number, internalclock)         
            enemy_gun[i].wall_collide(collision_list)

    #key input

    if internalclock % setup.firerate == 0: #this sets up a proper delay between shots
        in_between_shots = True

    if pygame.mouse.get_pressed()[2] and not semiauto and not reloading and in_between_shots:
        recoil = randint(-1 * setup.recoil, setup.recoil)
        
        
        if setup.shotgun:
            player_gun.shotgun_create_shot(recoil, player.angle)
        else:
            player_gun.create_shot(recoil, player.angle)
        
        in_between_shots = False
        if setup.action == "semi-auto":
            semiauto = True
        
        #keep track of shots taken in current mag
        #if we've taken enough shots, then reload    
        shot += 1
        if shot >= setup.mag:
            reloading = True
            internalclock = 0
            shot = 0
            
    #if we've waited long enough, stop reloading
    if reloading and internalclock >= setup.reloadtime:
        reloading = False
    if setup.online:
        if enemy_player.online_paused:
            continue
    if setup.map_choice == "MIDWAY":
        player.set_angle(mousepos, "plane")
    else:
        player.set_angle(mousepos)
                             
    if pygame.mouse.get_pressed()[1] and shot != 0:
        reloading = True
        internalclock = 0
        shot = 0
        
    if not pygame.mouse.get_pressed()[2] and setup.action == "semi-auto":
        semiauto = False 
            
    if pygame.mouse.get_pressed()[0] or setup.map_choice == "MIDWAY": 
        #player.test_2(mousepos)    
        player.move(mousepos, setup.rations, setup.map_choice)
    """if pygame.mouse.get_pressed()[2]:
        if internalclock % 20 == 0:
            if player.angle == 360:
                player.angle = 0
            else:
                player.angle += 1
            player.maincharacter = pygame.transform.rotate(player.backup, player.angle)"""
    
    
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_q:
                try:
                    if str(sys.argv[1]) == "-d": 
                        player.spawn(maps.spawnX, maps.spawnY, setup.map_choice) #use this to test spawns
                except:
                    pass
            elif event.key == pygame.K_RSHIFT:
                if setup.online and not setup.fix_online:
                    enemy_player.online_paused = True
                    Thread(target=enemy_player.online_pause_thread, args=(0,setup,)).start()
                else:
                    if setup.online:
                        try:
                            new_setup = setup.pause(setup, enemy_player.s, "server")
                        except:
                           new_setup = setup.pause(setup, enemy_player.c, "client")
                    else:
                        new_setup = setup.pause(setup, campaign=setup.campaign) #resume w/ changing loadout
                
                    if new_setup == None: #resume w/o changing loadout
                        del(new_setup)          
                    elif new_setup == "end": #end game
                        del(new_setup)
                        if setup.online:
                            try:
                                enemy_player.c.close()
                            except:
                                enemy_player.s.close()
                        if setup.campaign:
                            titlescreen_menu("campaign")
                        else:
                            Menu([]).end_screen(kills, deaths)
                            player.update_rank(kills)
                            titlescreen_menu("multiplayer")
                       
    #images/rendering
    pygame.display.set_caption("WWII  FPS: " + str(int(clock.get_fps()))) #+ " " + str((player.imagesx + player.mainx, player.imagesy + player.mainy)))
    screen.blit(background, (0, 0))
    if setup.custom:
        Play_Maps(setup.map_choice).blit_map(player.imagesx, player.imagesy)
    else:
        """when in campaign mode, this system makes it so you can only hit text boxes once"""
        add = Maps(player.imagesx, player.imagesy, campaign_text_check).blit_map(setup.map_choice)
        
        if add == "DONE":
            Campaign().donescreen(kills, setup.map_choice)
            with open(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)), 'Data', '')+"userdata", "rb") as file:
                data = pickle.load(file)
            if not setup.map_choice in data["campaign"]:
                new = data["campaign"]
                new.append(setup.map_choice)
                data["campaign"] = new
                with open(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)), 'Data', '')+"userdata", "wb+") as file:
                    pickle.dump(data, file, protocol=2)
            titlescreen_menu("campaign")
        
        if add != None:
            campaign_text_check.append(add)
            
            
            
            
    if setup.shotgun and setup.flame:
        player_gun.blit_shot(True)
    else:
        player_gun.blit_shot()
    if setup.online:
        if enemy_player.shotgun and enemy_player.flame_thrower:
            enemy_gun.blit_shot(True)
        else:
            enemy_gun.blit_shot()
    else:
        for i in range(0, setup.enemies):
            if enemy_player[i].shotgun and enemy_player[i].flame:
                enemy_gun[i].blit_shot(True)
            else:
                enemy_gun[i].blit_shot()
    if setup.online:
        enemy_player.blit_enemy(hit_enemy, player.imagesx, player.imagesy, enemy_player.angle, enemy_player.enemy_gun) 
    else:
        for i in range(0, setup.enemies):
            try:
                if setup.campaign:
                    if (840 > enemy_pos_backup[i][0] - player.imagesx > -200 and 680 > enemy_pos_backup[i][1] - player.imagesy > -200):
                        if setup.map_choice == "MIDWAY":
                            enemy_player[i].blit_enemy(hit_enemy[i], player.imagesx, player.imagesy, types="plane")
                        else:
                            enemy_player[i].blit_enemy(hit_enemy[i], player.imagesx, player.imagesy) 
                        
                else:
                    enemy_player[i].blit_enemy(hit_enemy[i], player.imagesx, player.imagesy)             
            except:
                pass
                
                
                
    if setup.map_choice == "MIDWAY":
        screen.blit(player.maincharacter, (player.mainx, player.mainy))
    else:              
        screen.blit(player.maincharacter, (player.mainx, player.mainy))
        setup.guns(loadout_number, player.angle) #blitting our gun  
    player.red_screen()
    if setup.campaign:
        player.ui("campaign", deaths, setup.weapon, setup.mag, shot, reloading, setup.max_kills) 
    else:
        player.ui(kills, deaths, setup.weapon, setup.mag, shot, reloading, setup.max_kills) 
    #pygame.draw.circle(screen, (0, 0, 0), (screen.get_size()[0] / 2, screen.get_size()[1] / 2), screen.get_size()[1] / 2, 20)   
    pygame.display.flip()

pygame.quit()
if setup.online:
    try:
        enemy_player.c.close()
    except:
        enemy_player.s.close()
sys.exit()
