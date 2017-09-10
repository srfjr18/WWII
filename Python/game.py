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
def titlescreen_menu(start=False):
    global reloading, semiauto
    global enemy_hit, kills, deaths, hit, shot, internalclock
    global setup, maps, loadouts, player, player_gun
    global enemy_gun, enemy_player, loadout_number
    global background, in_between_shots, first_run, enemy_gun_online
    first_run = True
    reloading = semiauto = False
    enemy_hit = kills = deaths = hit = shot = internalclock = 0 
    try:
        setup = Setup(setup.map_choice, setup.custom)
    except:
        setup = Setup()
    maps = Maps(0, 0)
    if start:
        Menu([]).TitleScreen()
    loadouts = Loadouts(False)
    player = Player()
    player_gun = Gun()
    player.update_rank(kills)
    setup.MainMenu()

    if setup.online:
        enemy_player = enemy_gun = online_mode(setup.map_choice, setup.max_kills)
            
        setup.map_choice = enemy_player.online_map_choice
        setup.max_kills = enemy_gun.online_max_kills
        
        try:
            maps.background_color(setup.map_choice)
        except ValueError: #host is using custom map
            setup.custom = True
        
        if enemy_player.back:
            titlescreen_menu()
    
    if setup.custom:
        maps = Play_Maps(setup.map_choice)
        player = Player(setup.map_choice)
    
    if setup.online:
        try:
            loadout_number, enemy_gun_online = Loadouts(False).display_loadout(enemy_player.c, "client")
        except:
            loadout_number, enemy_gun_online = Loadouts(False).display_loadout(enemy_player.s, "server")
    else:
        loadout_number = Loadouts(False).display_loadout()
    setup.guns(loadout_number)
    setup.perks(loadout_number)
    maps.spawn_area(setup.map_choice)

    if not setup.online:
        enemy_gun = Enemy_Gun()
        enemy_player = Enemy(maps.spawnX, maps.spawnY, loadout_number, enemy_gun)

    background = pygame.Surface(screen.get_size())
    background.fill(maps.background_color(setup.map_choice))
    background = background.convert()

    player.spawn(maps.spawnX, maps.spawnY, setup.map_choice)

    in_between_shots = False

    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Resources', 'sounds', '')+'gamemusic.wav')
    pygame.mixer.music.play(-1)


titlescreen_menu(True)
while running:
    
    mousepos = pygame.mouse.get_pos()
    clock.tick(FPS)
    internalclock += 1
    
    #player.test(mousepos)
    
    player.set_angle(mousepos)
    
    #updating collisions based on our position
    if setup.custom:
        collision_list = maps.map_collisions_update(player.imagesx, player.imagesy) 
    else:
        collision_list = map_collisions_update(player.imagesx, player.imagesy, setup.map_choice)    
  
    #player gun
    hit_enemy = player_gun.enemy_collide(collision_list, pygame.Rect((enemy_player.enemyposX - player.imagesx, enemy_player.enemyposY - player.imagesy), enemy_player.backup.get_size()))   
    if hit_enemy:
        hit += 1
        if hit >= setup.stk:
            if not setup.online:
                enemy_gun = Enemy_Gun()
                enemy_player = Enemy(maps.spawnX, maps.spawnY, loadout_number, enemy_gun)
            else:
                player.shotrise_list = player.shotrun_list = player.backup_shotrise = player.backup_shotrun = []
            hit = 0
            kills += 1
            if kills >= setup.max_kills:
                if setup.online:
                    try:
                        enemy_player.c.close
                    except:
                        enemy_player.s.close
                Menu([]).end_screen(kills, deaths)
                player.update_rank(kills)
                titlescreen_menu()
    
    #Checking for our shot's collisions with the wall
    player_gun.wall_collide(collision_list)
  
    #enemy gun
    if enemy_gun.collide_you(collision_list):
        enemy_hit += 1
        if enemy_hit >= enemy_player.enemy_stk:
            if setup.online:
                try:
                    Menu([]).killed(enemy_player.name, enemy_player.c, "client")
                except:
                    Menu([]).killed(enemy_player.name, enemy_player.s, "server")
            else:
                Menu([]).killed()

            enemy_hit = 0
            if setup.custom:
                player = Player(setup.map_choice)
            else:
                player = Player()
            player.spawn(maps.spawnX, maps.spawnY, setup.map_choice)
            if not setup.online:
                enemy_gun = Enemy_Gun()
                enemy_player = Enemy(maps.spawnX, maps.spawnY, loadout_number, enemy_gun)
            deaths += 1
            if deaths >= setup.max_kills:
                if setup.online:
                    try:
                        enemy_player.c.close
                    except:
                        enemy_player.s.close
                Menu([]).end_screen(kills, deaths)
                player.update_rank(kills)
                titlescreen_menu()
            
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
  
                if setup.online:
                    enemy_player.send_receive(setup.stk, player.angle, player.imagesx, player.imagesy, player_gun.shotrise_list, player_gun.shotrun_list, gun)
            except:
                pass
            reloading = False
            shot = 0

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
                enemy_player.c.close
            except:
                pass
            try:
                enemy_player.s.close 
            except:
                pass 
            endcheck = None
            Menu([]).end_screen(kills, deaths)
            player.update_rank(kills)
            titlescreen_menu()
    else:
        enemy_player.AI(player.imagesx, player.imagesy, collision_list, loadout_number, internalclock)         
    enemy_gun.wall_collide(collision_list)

    #key input

    if internalclock % setup.firerate == 0: #this sets up a proper delay between shots
        in_between_shots = True

    if pygame.mouse.get_pressed()[2] and not semiauto and not reloading and in_between_shots:
        recoil = randint(-1 * setup.recoil, setup.recoil)
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
                             
    if pygame.mouse.get_pressed()[1] and shot != 0:
        reloading = True
        internalclock = 0
        shot = 0
        
    if not pygame.mouse.get_pressed()[2] and setup.action == "semi-auto":
        semiauto = False 
            
    if pygame.mouse.get_pressed()[0]:     
        player.move(mousepos, setup.rations, setup.map_choice)
    
    
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_d:
                try:
                    if str(sys.argv[1]) == "-d": 
                        player.spawn(maps.spawnX, maps.spawnY, setup.map_choice) #use this to test spawns
                except:
                    pass
            elif event.key == pygame.K_RSHIFT:
                if setup.online:
                    try:
                        new_setup = setup.pause(setup, enemy_player.c, "client")
                    except:
                        new_setup = setup.pause(setup, enemy_player.s, "server")
                else:
                    new_setup = setup.pause(setup) #resume w/ changing loadout
                
                if new_setup == None: #resume w/o changing loadout
                    del(new_setup)          
                elif new_setup == "end": #end game
                    del(new_setup)
                    if setup.online:
                        try:
                            enemy_player.c.close
                        except:
                            enemy_player.s.close
                    Menu([]).end_screen(kills, deaths)
                    player.update_rank(kills)
                    titlescreen_menu()
                    break
                        
    #images/rendering
    pygame.display.set_caption("WWII  FPS: " + str(int(clock.get_fps()))) #+ " " + str((player.imagesx + player.mainx, player.imagesy + player.mainy)))
    screen.blit(background, (0, 0))
    if setup.custom:
        Play_Maps(setup.map_choice).blit_map(player.imagesx, player.imagesy)
    else:
        Maps(player.imagesx, player.imagesy).blit_map(setup.map_choice)
    player_gun.blit_shot()
    enemy_gun.blit_shot()
    if setup.online:
        enemy_player.blit_enemy(hit_enemy, player.imagesx, player.imagesy, enemy_player.angle, enemy_player.enemy_gun) 
    else:
         enemy_player.blit_enemy(hit_enemy, player.imagesx, player.imagesy)             
    screen.blit(player.maincharacter, (player.mainx, player.mainy))
    setup.guns(loadout_number, player.angle) #blitting our gun   
    player.red_screen(setup.medic, enemy_player.enemy_stk, enemy_hit)
    player.ui(kills, deaths, setup.weapon, setup.mag, shot, reloading, setup.max_kills) 
    #pygame.draw.circle(screen, (0, 0, 0), (screen.get_size()[0] / 2, screen.get_size()[1] / 2), screen.get_size()[1] / 2, 20)   
    pygame.display.flip()
    
pygame.quit()
if setup.online:
    try:
        enemy_player.c.close
    except:
        enemy_player.s.close
sys.exit()
