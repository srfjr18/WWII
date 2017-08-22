import pygame, os, math, sys
from Resources.scripts.Maps import *
from random import randint

if __name__ == "__main__":
    sys.exit()

path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1]), 'images', '')
soundpath = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1]), 'sounds', '')
class Player(object):
    def __init__(self):
        self.mainx = 300
        self.mainy = 240
        self.imagesx = 0
        self.imagesy = 0
        self.angle = 0
        self.maincharacter = self.backup = pygame.image.load(path+'character.png')
        self.font = pygame.font.SysFont(None, 25)
        self.smallfont = pygame.font.SysFont(None, 20)
    
    def proper_spawn(self, collision_list):
        main_collision = pygame.Rect((self.mainx, self.mainy), (self.backup.get_size()[0] * 2, self.backup.get_size()[1] * 2)) 
            
        for collisions in collision_list[:]:
            if main_collision.colliderect(collisions):
                return True
        return False

    def spawn(self, spawnarea_x, spawnarea_y, map_choice):
        self.imagesx = randint(spawnarea_x[0], spawnarea_x[1]) #- imagesx
        self.imagesy = randint(spawnarea_y[0], spawnarea_y[1]) #- imagesy
        collision_list = map_collisions_update(self.imagesx, self.imagesy, map_choice)
        while True:
            collision_list = map_collisions_update(self.imagesx, self.imagesy, map_choice)
            if self.proper_spawn(collision_list):
                self.imagesx = randint(spawnarea_x[0], spawnarea_x[1]) #(spawnarea)
                self.imagesy = randint(spawnarea_y[0], spawnarea_y[1]) #(spawnarea)
            else:
                break
    
    
    def update_rank(self, kills):
        path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', '')
        with open(path+'data', 'r+') as file:
            name, rank = file.readlines()
        os.remove(path+'data')
        with open(path+'data', 'w+') as file:
            file.write(name+str(int(rank) + kills))
            
        self.rank = int((int(rank) + kills) / 25)
        
    def ui(self, kills, deaths, weapon, mag, shot, reloading):
        kd_bg = pygame.Surface((100,30), pygame.SRCALPHA)
        kd_bg.fill((211,211,211,180))
        screen.blit(kd_bg, (540,0))
        pygame.draw.rect(screen, (0, 0, 0), (540, 0, 100, 30), 3)    
        text = self.font.render("K: " + str(kills) + " D: " + str(deaths),1,(0,0,0))
        screen.blit(text, (550, 5))
    
        gun_bg = pygame.Surface((205,50), pygame.SRCALPHA)
        gun_bg.fill((211,211,211,180))
        screen.blit(gun_bg, (435,440))
        pygame.draw.rect(screen, (0, 0, 0), (435, 440, 205, 50), 3) 
        if reloading:
            text = self.font.render(str(weapon),1,(0,0,0))
            screen.blit(self.smallfont.render("RELOADING",1,(0,0,0)), (550, 445))
        else:  
            if mag <= 30: 
                text = self.font.render(str(weapon) + " " + str("|" * (mag - shot)),1,(0,0,0))
            else:
                text = self.font.render(str(weapon) + "  AMMO: " + str(mag - shot),1,(0,0,0))
        screen.blit(text, (440, 445))
        
    def red_screen(self, medic, enemy_stk, enemy_hit):
        if medic:
            num = 125
        else:
            num = 100
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        if enemy_hit != 0:
            alpha = 255 * ((enemy_stk + enemy_hit) / num)
            if alpha < 50:
                alpha = 50
            if alpha > 125:
                alpha = 125
            overlay.fill((255,0,0, alpha))
            screen.blit(overlay, (0,0))
        
    def set_angle(self, mousepos):
        self.angle = 90 + 360 - (math.degrees(math.atan2(self.mainy - mousepos[1], self.mainx - mousepos[0])))
        if self.angle >= 360:
            self.angle -= 360
        elif self.angle <= 0:
            self.angle += 360
        self.maincharacter = pygame.transform.rotate(self.backup, self.angle)
        
    def collision(self, collision_list):
        main_collision = pygame.Rect((self.mainx, self.mainy), self.backup.get_size())
        for collisions in collision_list[:]:
            if main_collision.colliderect(collisions):               
                return True
        return False
        
    def fix_go_thru_corners(self, collision_list):
        main_collision = pygame.Rect((self.mainx, self.mainy), self.backup.get_size())
        for collisions in collision_list[:]:
            if main_collision.colliderect(collisions):               
                main_collision = pygame.Rect((self.mainx + self.moveX, self.mainy + self.moveY), (self.maincharacter.get_size()[0], self.maincharacter.get_size()[1]))
                for collisionsone in collision_list[:]:
                    if main_collision.colliderect(collisionsone) and collisionsone != collisions:
                        self.imagesx -= self.moveX #* 2
                
                        
    def move(self, mousepos, rations, map_choice):
        self.moveX = (mousepos[0] - self.mainx) / 30
        self.moveY = (mousepos[1] - self.mainy) / 30
        
        #rations is the speed perk
        if rations:
            self.moveX *= 1.25
            self.moveY *= 1.25  

        self.imagesy += self.moveY
        self.imagesx += self.moveX 
        self.fix_go_thru_corners(map_collisions_update(self.imagesx, self.imagesy, map_choice))                 
        #updating our collision value after we modified imagesx and y            
        if self.collision(map_collisions_update(self.imagesx, self.imagesy, map_choice)):
            self.imagesy += self.moveY
            self.imagesx -= self.moveX     
            if self.collision(map_collisions_update(self.imagesx, self.imagesy, map_choice)):
                self.imagesy -= self.moveY * 2
                self.imagesx += self.moveX * 2
                

class Gun(object):
    def __init__(self):
        self.gunshot = pygame.mixer.Sound(soundpath+"gunshot.wav")
        self.mainx = 300
        self.mainy = 240       
        self.shotrun_list = []
        self.shotrise_list = []
        self.backup_shotrise = []
        self.backup_shotrun = []
        self.bullet = pygame.image.load(path+'bullet.png')     
        
    def blit_shot(self):
        for rise, run, brise, brun in zip(self.shotrise_list, self.shotrun_list, self.backup_shotrise, self.backup_shotrun):
            self.shotrise_list.remove(rise)
            self.shotrun_list.remove(run)
            self.shotrise_list.append(rise + brise)
            self.shotrun_list.append(run + brun)
            screen.blit(self.bullet, (run, rise))            
            
    def wall_collide(self, collision_list):
        for rise, run, brise, brun in zip(self.shotrise_list, self.shotrun_list, self.backup_shotrise, self.backup_shotrun):
            for collisions in collision_list[:]:
                if pygame.Rect((run,rise), self.bullet.get_size()).colliderect(collisions):
                    try:                  
                        self.shotrise_list.remove(rise)
                        self.shotrun_list.remove(run)
                        self.backup_shotrise.remove(brise)
                        self.backup_shotrun.remove(brun)
                    except:
                        pass
                        """I have literally no fucking idea how the hell these values aren't in the fucking list sometimes. ITS LITERALLY THE EXACT SAME VALUE FROM THE DAMN LIST. IT IS IMPOSSIBLE FOR IT TO NOT BE IN THE LIST"""   
                        
    def enemy_collide(self, collision_list, enemy_rect):
        for rise, run, brise, brun in zip(self.shotrise_list, self.shotrun_list, self.backup_shotrise, self.backup_shotrun):
            for collisions in collision_list[:]:
                if pygame.Rect((run,rise), self.bullet.get_size()).colliderect(enemy_rect):
                    return True
                   
    def create_shot(self, mousepos, recoil):
        self.shot_moveY = (mousepos[1] - self.mainy + recoil) / 10
        self.shot_moveX = (mousepos[0] - self.mainx + recoil) / 10
        
        self.shotrun_list.append(self.shot_moveX + self.mainx)
        self.shotrise_list.append(self.shot_moveY + self.mainy)
        self.backup_shotrun.append(self.shot_moveX)
        self.backup_shotrise.append(self.shot_moveY)
        
        pygame.mixer.Sound.play(self.gunshot)
        
        """if len(self.shotrun_list) > 40:
            self.shotrun_list = []
            self.shotrise_list = []
            self.backup_shotrun = []
            self.backup_shotrise = []"""
