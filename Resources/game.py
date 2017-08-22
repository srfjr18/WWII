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
reloading = semiauto = False
enemy_hit = kills = deaths = hit = shot = internalclock = 0 
setup = Setup()
maps = Maps(0, 0)
loadouts = Loadouts(False)
player = Player()
player_gun = Gun()

#titlescreen and main menu
Menu([]).TitleScreen()
player.update_rank(kills)
setup.MainMenu()


if setup.online:
    enemy_player = enemy_gun = online_mode()

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
while running:
  
    mousepos = pygame.mouse.get_pos()
    clock.tick(FPS)
    internalclock += 1
    
    player.set_angle(mousepos)
    
    #updating collisions based on our position
    collision_list = map_collisions_update(player.imagesx, player.imagesy, setup.map_choice)    
  
    #player gun
    hit_enemy = player_gun.enemy_collide(collision_list, pygame.Rect((enemy_player.enemyposX - player.imagesx, enemy_player.enemyposY - player.imagesy), enemy_player.backup.get_size()))   
    if hit_enemy:
        hit += 1
        if hit >= setup.stk:
            if not setup.online:
                enemy_gun = Enemy_Gun()
                enemy_player = Enemy(maps.spawnX, maps.spawnY, loadout_number, enemy_gun)
            """else:
                player.shotrise_list = player.shotrun_list = player.backup_shotrise = player.backup_shotrun = []"""
            hit = 0
            kills += 1
    
    #Checking for our shot's collisions with the wall
    player_gun.wall_collide(collision_list)
  
    #enemy gun
    if enemy_gun.collide_you(collision_list):
        enemy_hit += 1
        if enemy_hit >= enemy_player.enemy_stk:
            enemy_hit = 0
            player = Player()
            player.spawn(maps.spawnX, maps.spawnY, setup.map_choice)
            if not setup.online:
                enemy_gun = Enemy_Gun()
                enemy_player = Enemy(maps.spawnX, maps.spawnY, loadout_number, enemy_gun)
            deaths += 1
            
            #updating our loadout if we changed it at the pause menu
            try:
                online = setup.online
                setup = new_setup
                setup.online = online
            except:
                pass
            reloading = False
            shot = 0
            if not setup.online:
                Menu([]).killed()

    if setup.online:
        endcheck = enemy_player.send_receive(setup.stk, player.angle, player.imagesx, player.imagesy,  player_gun.shotrise_list, player_gun.shotrun_list) #means we are playing online
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
            #updating our xp
            player.update_rank(kills)                
            #reset all needed variables
            reloading = semiauto = False
            enemy_hit = kills = deaths = hit = shot = internalclock = 0 
            setup = Setup()
            setup.online = False
            maps = Maps(0, 0)
            loadouts = Loadouts(False)
            player = Player()
            player_gun = Gun()
            enemy_gun = Enemy_Gun()
            #pulling up the menu again
            player.update_rank(kills)
            setup.MainMenu()
            

            if setup.online:
                enemy_player = enemy_gun = online_mode()

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
            pygame.mixer.music.stop()
            pygame.mixer.music.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Resources', 'sounds', '')+'gamemusic.wav')
            pygame.mixer.music.play(-1)
    else:
        enemy_player.AI(player.imagesx, player.imagesy, collision_list, loadout_number, internalclock)         
    enemy_gun.wall_collide(collision_list)

    #key input

    if internalclock % setup.firerate == 0: #this sets up a proper delay between shots
        in_between_shots = True

    if pygame.mouse.get_pressed()[2] and not semiauto and not reloading and in_between_shots:
        recoil = randint(-1 * setup.recoil, setup.recoil)
        player_gun.create_shot(mousepos, recoil)
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
                    #updating our xp
                    player.update_rank(kills)                
                    #reset all needed variables
                    reloading = semiauto = False
                    enemy_hit = kills = deaths = hit = shot = internalclock = 0 
                    setup = Setup()
                    maps = Maps(0, 0)
                    loadouts = Loadouts(False)
                    player = Player()
                    player_gun = Gun()
                    enemy_gun = Enemy_Gun()
                    #pulling up the menu again
                    player.update_rank(kills)
                    setup.MainMenu()
                    

                    if setup.online:
                        enemy_player = enemy_gun = online_mode()

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
                    
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Resources', 'sounds', '')+'gamemusic.wav')
                    pygame.mixer.music.play(-1)
                    break
                        
    #images/rendering
    pygame.display.set_caption("WWII  FPS: " + str(int(clock.get_fps()))) #+ " " + str((player.imagesx + player.mainx, player.imagesy + player.mainy)))
    screen.blit(background, (0, 0))
    Maps(player.imagesx, player.imagesy).blit_map(setup.map_choice)
    player_gun.blit_shot()
    enemy_gun.blit_shot()
    if setup.online:
        enemy_player.blit_enemy(hit_enemy, player.imagesx, player.imagesy, enemy_player.angle) 
    else:
         enemy_player.blit_enemy(hit_enemy, player.imagesx, player.imagesy)             
    screen.blit(player.maincharacter, (player.mainx, player.mainy))   
    player.red_screen(setup.medic, enemy_player.enemy_stk, enemy_hit)
    player.ui(kills, deaths, setup.weapon, setup.mag, shot, reloading)    
    pygame.display.flip()
    
pygame.quit()
if setup.online:
    try:
        enemy_player.c.close
    except:
        enemy_player.s.close
sys.exit()
