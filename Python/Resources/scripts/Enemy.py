from Resources.scripts.Menus import *   
from random import randint
import math, pygame, sys

if __name__ == "__main__":
    sys.exit()
screen =  pygame.display.set_mode((640,480))
path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1]), 'images', '')
soundpath = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1]), 'sounds', '')
class Enemy(Setup, Gun_Types):
    def __init__(self, spawnarea_x, spawnarea_y, loadout_number, enemy_gun):
        self.spawnarea_x = spawnarea_x
        self.spawnarea_y = spawnarea_y
        self.mainx = 300
        self.mainy = 240
        self.enemyposX = 0
        self.enemyposY = 0
        self.enemy_shot = 0
        self.shoot = False
        self.counter = 0
        self.before_sees_you = 0
        self.before_accurate = 0
        self.alreadycollided = False
        self.gun = enemy_gun
        self.enemy_reloading = 0
        Gun_Types.__init__(self)
        Setup.__init__(self)
        self.backup = self.enemy = pygame.image.load(path+'enemy.png')
        self.hitmarker = pygame.image.load(path+'hitmarker.png')
        self.enemy_firerate, self.enemy_action, self.enemy_stk, self.enemy_mag, self.enemy_reloadtime, recoil = self.getrand_gun_or_blit()
        if self.enemy_action == "semi-auto":
            self.enemy_firerate = 30
    
    def blit_enemy(self, collision, imagesx, imagesy, angle=None, gun=None):
        if angle != None and gun != None:
            self.enemy = pygame.transform.rotate(self.backup, angle)
            gun = pygame.transform.rotate(gun, angle)
            
            screen.blit(self.enemy, (self.enemyposX - imagesx, self.enemyposY - imagesy))
            screen.blit(gun, (self.enemyposX - imagesx - 25, self.enemyposY - imagesy - 25))
        else: # AI enemy
            try:
                self.enemy_angle
            except:
                self.enemy_angle = 0
            screen.blit(self.enemy, (self.enemyposX - imagesx, self.enemyposY - imagesy))
            self.getrand_gun_or_blit(self.rand_num, self.enemy_angle, self.enemyposX - imagesx, self.enemyposY - imagesy)
        if collision:
            screen.blit(self.hitmarker, (self.enemyposX - imagesx + (self.backup.get_size()[0] / 2.5), self.enemyposY - imagesy + (self.backup.get_size()[1] / 2.5)))
    
    def AI(self, imagesx, imagesy, collision_list, loadout_number, internalclock):
        self.perks(loadout_number)
        #Core of our enemies's AI          
        try:
            self.enemyposX
        except:
            self.enemyposX, self.enemyposY = 0, 0 
                
        # modify the randint to change speed enemies spawn         
        if randint(1, 1) == 1 and not 640 > self.enemyposX - imagesx > 0 and not 480 > self.enemyposY - imagesy > 0 or self.proper_spawn(self.enemyposX - imagesx, self.enemyposY - imagesy, collision_list):
    
            #choose random gun for enemy
            self.enemy_firerate, self.enemy_action, self.enemy_stk, self.enemy_mag, self.enemy_reloadtime, recoil = self.getrand_gun_or_blit() #recoil is just neglected because badaim usually makes up for it or more
            if self.enemy_action == "semi-auto":
                self.enemy_firerate = 30
        
            # enemies need 1.5 times more shots if medic perk is used    
            if self.medic:
                self.enemy_stk *= 1.5
            self.spawn(imagesx, imagesy, collision_list)
            self.alreadycollided = False
            #makes enemy aim less precise
            # if distraction perk is enabled, make early enemy shots even less accurate
            if self.distraction:
                self.badaim = randint(2, 6)
            else:
                self.badaim = randint(0, 5)
            self.before_sees_you = randint(0, 30)
            self.before_accurate = randint(51, 120)
            if self.before_accurate < 75:
                self.badaim *= -1 # doing this just to switch up the direction half the time without allowing the enemy to be too accurate in the middle with distraction
            
        #if enemy hasn't collided with an object and alpha perk is off, then move towards you            
        if not self.alreadycollided and not self.alpha:      
            self.enemyposY += (self.mainy + imagesy - self.enemyposY) / 100
            self.enemyposX += (self.mainx + imagesx - self.enemyposX)/ 100
            #self.enemy = pygame.transform.rotate(self.backup, math.degrees(math.atan((self.enemyposY) / (self.enemyposX)) + 0))
        
        #if alpha is on, move slower
        if not self.alreadycollided and self.alpha: 
            self.enemyposY += (self.mainy + imagesy - self.enemyposY) / 150
            self.enemyposX += (self.mainx + imagesx - self.enemyposX)/ 150
            if self.enemyposX == 0:
                self.enemyposX = 1
            self.enemy = pygame.transform.rotate(self.backup, math.degrees(math.atan((self.enemyposY) / (self.enemyposX)) + 0))
       
        #checks for a collision and kicks the enemy back to a permenant position if it returns True      
        if self.proper_spawn(self.enemyposX - imagesx, self.enemyposY - imagesy, collision_list) and not self.alreadycollided:            
            self.enemyposY -= 10 * ((self.mainy + imagesy - self.enemyposY) / 100)
            self.enemyposX -= 10 * ((self.mainx + imagesx - self.enemyposX) / 100)
            self.alreadycollided = True
        
        #if the enemy is on our screen
        if 640 > self.enemyposX - imagesx > 0 and 480 > self.enemyposY - imagesy > 0:
    
            #count the frames that the enemy is on our screen
            self.counter += 1
        
            if self.counter > self.before_sees_you:
                self.turn_to_you(imagesx, imagesy)
        
            if self.counter > self.before_sees_you and self.counter < self.before_accurate and internalclock % self.enemy_firerate == 0 and self.enemy_shot <= self.enemy_mag:
                self.enemy_shot += 1
                self.gun.shoot_you(self.enemyposX, self.enemyposY, imagesx, imagesy, self.badaim, self.enemy_angle)
            if self.counter > self.before_accurate and internalclock % self.enemy_firerate == 0:
                #makes enemy firerate more accurate if the gun is semi-auto
                if self.enemy_firerate >= 30  and self.enemy_shot <= self.enemy_mag:
                    self.enemy_shot += 1
                
                    # distraction perk making shots slightly less accurate
                    if self.distraction:
                        self.gun.shoot_you(self.enemyposX, self.enemyposY, imagesx, imagesy, randint(-2,2), self.enemy_angle)
                    else:
                        self.gun.shoot_you(self.enemyposX, self.enemyposY, imagesx, imagesy, randint(-1,1), self.enemy_angle)
                    
                elif not self.enemy_firerate >= 30 and self.enemy_shot <= self.enemy_mag:
                    self.enemy_shot += 1
                
                    #same for full auto with the distraction perk
                    if self.distraction:
                        self.gun.shoot_you(self.enemyposX, self.enemyposY, imagesx, imagesy, randint(-4,4), self.enemy_angle)
                    else:
                        self.gun.shoot_you(self.enemyposX, self.enemyposY, imagesx, imagesy, randint(-3,3), self.enemy_angle)
                    
                    
        # enemy reloads        
        if self.enemy_shot >= self.enemy_mag:
            self.enemy_reloading += 1
            if self.enemy_reloading >= self.enemy_reloadtime:
                self.enemy_shot = 0
                self.enemy_reloading = 0                   
    
        
    def proper_spawn(self, x, y, collision_list):
        main_collision = pygame.Rect((x, y), self.backup.get_size()) 
            
        for collisions in collision_list[:]:
            if main_collision.colliderect(collisions):
                return True

    def spawn(self, imagesx, imagesy, collision_list):
        spawnpointX = randint(self.spawnarea_x[0], self.spawnarea_x[1]) #- imagesx
        spawnpointY = randint(self.spawnarea_y[0], self.spawnarea_y[1]) #- imagesy
        while True:
            if self.proper_spawn(spawnpointX - imagesx, spawnpointY - imagesy, collision_list) or 640 > spawnpointX - imagesx > 0 and 480 > spawnpointY - imagesy > 0:
                spawnpointX = randint(self.spawnarea_x[0], self.spawnarea_x[1]) #(spawnarea)
                spawnpointY = randint(self.spawnarea_y[0], self.spawnarea_y[1]) #(spawnarea)
            else:
                self.enemyposX = spawnpointX
                self.enemyposY = spawnpointY
                break
                
    def turn_to_you(self, imagesx, imagesy):
        enemy_angle = 90 + 360 - (math.degrees(math.atan2(self.enemyposY - self.mainy - imagesy, self.enemyposX - self.mainx - imagesx)))
        if enemy_angle >= 360:
            enemy_angle -= 360
        elif enemy_angle <= 0:
            enemy_angle += 360           
        self.enemy = pygame.transform.rotate(self.backup, enemy_angle)
        
        self.enemy_angle = enemy_angle
        

           
class Enemy_Gun(object):
    def __init__(self): 
        self.gunshot = pygame.mixer.Sound(soundpath+"gunshot.wav")  
        self.mainx = 300
        self.mainy = 240
        self.backup = pygame.image.load(path+'character.png')  
        self.enemy_shotrun_list = []
        self.enemy_shotrise_list = []
        self.enemy_backup_shotrise = []
        self.enemy_backup_shotrun = [] 
        self.bullet = pygame.image.load(path+'bullet.png')    
        
    def wall_collide(self, collision_list):
        for rise, run, brise, brun in zip(self.enemy_shotrise_list, self.enemy_shotrun_list, self.enemy_backup_shotrise, self.enemy_backup_shotrun):
            for collisions in collision_list[:]:
                if pygame.Rect((run,rise), self.bullet.get_size()).colliderect(collisions):
                    try:                  
                        self.enemy_shotrise_list.remove(rise)
                        self.enemy_shotrun_list.remove(run)
                        self.enemy_backup_shotrise.remove(brise)
                        self.enemy_backup_shotrun.remove(brun)
                    except:
                        pass
                        """AGAIN I HAVE NO CLUE WHY THE FUCK THIS HAPPENS"""    
                    
    def collide_you(self, collision_list):
        main_collision = pygame.Rect((self.mainx, self.mainy), self.backup.get_size())
        for rise, run, brise, brun in zip(self.enemy_shotrise_list, self.enemy_shotrun_list, self.enemy_backup_shotrise, self.enemy_backup_shotrun):
            for collisions in collision_list[:]:
                if pygame.Rect((run,rise), self.bullet.get_size()).colliderect(main_collision):
                    return True
                    
    def blit_shot(self):
        for rise, run, brise, brun in zip(self.enemy_shotrise_list, self.enemy_shotrun_list, self.enemy_backup_shotrise, self.enemy_backup_shotrun):
            self.enemy_shotrise_list.remove(rise)
            self.enemy_shotrun_list.remove(run)
            self.enemy_shotrise_list.append(rise + brise)
            self.enemy_shotrun_list.append(run + brun)
            screen.blit(self.bullet, (run, rise))
            
    def shoot_you(self, enemy_posX, enemy_posY, imagesx, imagesy, badaim, angle):
            
        sizeX, sizeY = self.backup.get_size()
        gun_pos = 4 - (angle / 90)
        
        sizeX -= 10
        
        if gun_pos <= 1:
            blitX = sizeX
            blitY = sizeY * gun_pos
        elif gun_pos <= 2:
            blitX = (sizeX * 2) - (sizeX * gun_pos)
            blitY = (sizeY * (2 - gun_pos)) / 4 + 50
        elif gun_pos <= 3:
            blitX = (sizeX * 2) - (sizeX * gun_pos)
            if blitX < 0:
                blitX = 0
            blitY = sizeY * (3 - gun_pos)
        elif gun_pos <= 4:
            blitY = 0
            blitX = sizeX - ((sizeX * 4) - (sizeX * gun_pos))
            
        mainy = self.mainy - blitY
        mainx = self.mainx - blitX
        
        
        enemy_shot_angley = -1 * ((enemy_posY - imagesy - mainy) / 10 + badaim)
        enemy_shot_anglex = -1 * ((enemy_posX - imagesx - mainx) / 10 + badaim)
    
        self.enemy_shotrun_list.append(enemy_shot_anglex + (enemy_posX - imagesx) + blitX)
        self.enemy_shotrise_list.append(enemy_shot_angley + (enemy_posY - imagesy) + blitY)
        self.enemy_backup_shotrun.append(enemy_shot_anglex)
        self.enemy_backup_shotrise.append(enemy_shot_angley) 
        
        pygame.mixer.Sound.play(self.gunshot)         

