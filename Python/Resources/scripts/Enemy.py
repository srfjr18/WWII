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
        self.mainx = 295
        self.mainy = 215
        self.enemyposX = 10000000
        self.enemyposY = 10000000
        self.enemy_shot = 0
        
        self.midway = False
        self.health = 100
        
        self.shoot = False
        self.spawned = False
        self.stop_all = self.online_paused = self.titlescreen = False #online vars that we have to set to false to play offline
        self.counter = 0
        self.before_sees_you = 0
        self.before_accurate = 0
        self.alreadycollided = False
        self.gun = enemy_gun
        self.enemy_reloading = 0
        self.pushed_backX, self.pushed_backY = 0, 0
        Gun_Types.__init__(self)
        Setup.__init__(self)
        self.backup = self.enemy = pygame.image.load(path+'enemy.png')
        self.plane = pygame.image.load(path+'japanplane.png')
        self.hitmarker = pygame.image.load(path+'hitmarker.png')
        self.enemy_firerate, self.enemy_action, self.enemy_stk, self.enemy_mag, self.enemy_reloadtime, recoil = self.getrand_gun_or_blit()
        if self.enemy_action == "semi-auto":
            self.enemy_firerate = 30
    
    def blit_enemy(self, collision, imagesx, imagesy, angle=None, gun=None, types=None):
     
    
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
            if types == "plane":
                japan = pygame.transform.rotate(self.plane, self.enemy_angle)
                screen.blit(japan, (self.enemyposX - imagesx, self.enemyposY - imagesy))
            else:
                screen.blit(self.enemy, (self.enemyposX - imagesx, self.enemyposY - imagesy))
                self.getrand_gun_or_blit(self.rand_num, self.enemy_angle, self.enemyposX - imagesx, self.enemyposY - imagesy)
                       
                
        
        
        if collision:
            screen.blit(self.hitmarker, (self.enemyposX - imagesx + (self.backup.get_size()[0] / 2.5), self.enemyposY - imagesy + (self.backup.get_size()[1] / 2.5))) 

        
        
        
        if angle != None:
            self.enemy_angle = angle
        
        bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
        
        
        green = int(self.health * 2.55)
        red = 255 - green
        
        pygame.draw.rect(bg, (0, 0, 0), (0, 20, 8, 25)) 
        pygame.draw.rect(bg, (red, green, 0), (0, 20, 8, self.health / 4)) 
        pygame.draw.rect(bg, (0, 0, 0), (0, 20, 8, self.health / 4), 3) 
        
        
        bg = pygame.transform.rotate(bg, self.enemy_angle)
        screen.blit(bg, (self.enemyposX - imagesx - 25, self.enemyposY - imagesy - 25))
        
        

        
        
    def AI(self, imagesx, imagesy, collision_list, loadout_number, internalclock, pos=None, map_choice=None): #pos will put an enemy at a specific position and make them unable to move
    
        if self.midway or map_choice == "MIDWAY":
            self.enemy_firerate, self.enemy_action, self.enemy_stk, self.enemy_mag, self.enemy_reloadtime = 8, "full-auto", 70, 1000000, 0 
            self.shotgun = False
            #sys.exit()
    
        if self.enemyposX == 100000000 or pos != None and not (840 > pos[0] - imagesx > -200 and 680 > pos[1] - imagesy > -200): #setting pos to this kills the enemy in campaign mode BUT THIS REALLY DOESN'T EVEN WORK 
            return
        self.perks(loadout_number)
        #Core of our enemies's AI          
        try:
            self.enemyposX
        except:
            self.enemyposX, self.enemyposY = 0, 0 
        
                
        # modify the randint to change speed enemies spawn         
        if self.midway or (pos != None and 840 > pos[0] - imagesx > -200 and 680 > pos[1] - imagesy > -200 and not self.spawned) or (not 640 > self.enemyposX - imagesx > 0 and not 480 > self.enemyposY - imagesy > 0 and not self.spawned and pos == None) or self.proper_spawn(self.enemyposX - imagesx, self.enemyposY - imagesy, collision_list) and not self.spawned and pos == None:
            
            if pos != None and not self.midway:
                if map_choice == "MIDWAY":
                    self.midway = True
                self.spawned = True
                self.enemyposX = pos[0]
                self.enemyposY = pos[1]
            
            """if randint(1, 500) != 1:
                 return"""
            
            
           
            
            #choose random gun for enemy
            if not self.midway and map_choice != "MIDWAY":
                self.enemy_firerate, self.enemy_action, self.enemy_stk, self.enemy_mag, self.enemy_reloadtime, recoil = self.getrand_gun_or_blit() #recoil is just neglected because badaim usually makes up for it or more
            
            
            if self.enemy_action == "semi-auto":
                self.enemy_firerate = 30
            #makes enemies kill you faster
            self.enemy_stk *= 0.8
            
            if map_choice == "MIDWAY" or map_choice == "D-DAY":
                if self.enemy_stk < 7:
                    self.enemy_stk = 7
            
            if self.midway or map_choice == "MIDWAY":
                self.enemy_stk *= 7
            if map_choice == "D-DAY":
                self.enemy_stk *= 5
            
            
            if self.midway:
                pos = None
            
            
            if self.stealer:
                if self.enemy_mag > 1:
                    self.enemy_mag *= 0.7
                    self.enemy_mag = int(self.enemy_mag)
            
            # enemies need 1.1 times more shots if medic perk is used    
            if self.medic:
                self.enemy_stk *= 1.1
            if pos == None and not self.midway:
                self.spawn(imagesx, imagesy, collision_list)
            self.alreadycollided = False
            #makes enemy aim less precise
            # if distraction perk is enabled, make early enemy shots even less accurate
            if self.distraction:
                self.badaim = randint(2, 6)
            else:
                self.badaim = randint(0, 5)
            self.before_sees_you = randint(0, 30)
            self.before_accurate = randint(0, 60)
            if self.before_accurate < 30:
                self.badaim *= -1 # doing this just to switch up the direction half the time without allowing the enemy to be too accurate in the middle with distraction
        
        
        
        #allows enemy to move again if our position means they wouldn't be colliding with a wall if they moved towards us
        if self.alreadycollided:
            testY = self.enemyposY + self.pushed_backY + ((self.mainy + imagesy - self.enemyposY) / 100)
            testX = self.enemyposX + self.pushed_backX + ((self.mainx + imagesx - self.enemyposX)/ 100)
            if not self.proper_spawn(testX - imagesx, testY - imagesy, collision_list):
                self.alreadycollided = False
            
        #if enemy hasn't collided with an object and alpha perk is off, then move towards you            
        if not self.alreadycollided and not self.alpha and pos == None:      
            self.enemyposY += (self.mainy + imagesy - self.enemyposY) / 100
            self.enemyposX += (self.mainx + imagesx - self.enemyposX)/ 100
           
            
            
            #self.enemy = pygame.transform.rotate(self.backup, math.degrees(math.atan((self.enemyposY) / (self.enemyposX)) + 0))
        
        #if alpha is on, move slower
        if not self.alreadycollided and self.alpha and pos == None: 
            self.enemyposY += (self.mainy + imagesy - self.enemyposY) / 150
            self.enemyposX += (self.mainx + imagesx - self.enemyposX)/ 150
            
            
            
            
            
            if self.midway or map_choice == "MIDWAY":
                self.enemyposY += (self.mainy + imagesy - self.enemyposY) / 100
                self.enemyposX += (self.mainx + imagesx - self.enemyposX)/ 100
            
            
            if self.enemyposX == 0:
                self.enemyposX = 1
            self.enemy = pygame.transform.rotate(self.backup, math.degrees(math.atan((self.enemyposY) / (self.enemyposX)) + 0))
       
        #checks for a collision and kicks the enemy back to a permenant position if it returns True      
        if self.proper_spawn(self.enemyposX - imagesx, self.enemyposY - imagesy, collision_list) and not self.alreadycollided: 
            self.pushed_backY = 10 * ((self.mainy + imagesy - self.enemyposY) / 100)
            self.pushed_backX = 10 * ((self.mainx + imagesx - self.enemyposX) / 100)
                   
            self.enemyposY -= 10 * ((self.mainy + imagesy - self.enemyposY) / 100)
            self.enemyposX -= 10 * ((self.mainx + imagesx - self.enemyposX) / 100)
            
            
            self.alreadycollided = True
        
        #if the enemy is on our screen or a little outside
        if 740 > self.enemyposX - imagesx > -100 and 580 > self.enemyposY - imagesy > -100:
    
            #count the frames that the enemy is on our screen
            self.counter += 1
        
            if self.counter > self.before_sees_you:
                self.turn_to_you(imagesx, imagesy)
        
            if self.counter > self.before_sees_you and self.counter < self.before_accurate and internalclock % self.enemy_firerate == 0 and self.enemy_shot <= self.enemy_mag:
                self.enemy_shot += 1
                
                if self.shotgun:
                    self.gun.shotgun_create_shot(self.enemyposX, self.enemyposY, imagesx, imagesy, self.badaim, self.enemy_angle)
                else:
                    self.gun.shoot_you(self.enemyposX, self.enemyposY, imagesx, imagesy, self.badaim, self.enemy_angle)
            if self.counter > self.before_accurate and internalclock % self.enemy_firerate == 0:
                #makes enemy firerate more accurate if the gun is semi-auto
                if self.enemy_firerate >= 30  and self.enemy_shot <= self.enemy_mag - 1:
                    self.enemy_shot += 1
                
                    # distraction perk making shots slightly less accurate
                    if self.distraction:
                        if self.shotgun:
                            self.gun.shotgun_create_shot(self.enemyposX, self.enemyposY, imagesx, imagesy, randint(-2,2), self.enemy_angle)
                        else:
                            self.gun.shoot_you(self.enemyposX, self.enemyposY, imagesx, imagesy, randint(-2,2), self.enemy_angle)
                    else:
                        if self.shotgun:
                            self.gun.shotgun_create_shot(self.enemyposX, self.enemyposY, imagesx, imagesy, randint(-1,1), self.enemy_angle)
                        else:
                            self.gun.shoot_you(self.enemyposX, self.enemyposY, imagesx, imagesy, randint(-1,1), self.enemy_angle)
                    
                elif not self.enemy_firerate >= 30 and self.enemy_shot <= self.enemy_mag - 1:
                    self.enemy_shot += 1
                
                    #same for full auto with the distraction perk
                    if self.distraction:
                        if self.shotgun:
                            self.gun.shotgun_create_shot(self.enemyposX, self.enemyposY, imagesx, imagesy, randint(-4,4), self.enemy_angle)
                        else:
                            self.gun.shoot_you(self.enemyposX, self.enemyposY, imagesx, imagesy, randint(-4,4), self.enemy_angle)
                    else:
                        if self.shotgun:
                            self.gun.shotgun_create_shot(self.enemyposX, self.enemyposY, imagesx, imagesy, randint(-3,3), self.enemy_angle)
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
            if self.proper_spawn(spawnpointX - imagesx, spawnpointY - imagesy, collision_list) or 640 > spawnpointX - imagesx > 0 and 480 > spawnpointY - imagesy > 0 or spawnpointX - imagesx == 0:
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
        self.flame = pygame.image.load(path+'flame.png')  
        
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
                    
    def blit_shot(self, flame=False):
        for rise, run, brise, brun in zip(self.enemy_shotrise_list, self.enemy_shotrun_list, self.enemy_backup_shotrise, self.enemy_backup_shotrun):
            self.enemy_shotrise_list.remove(rise)
            self.enemy_shotrun_list.remove(run)
            self.enemy_shotrise_list.append(rise + brise)
            self.enemy_shotrun_list.append(run + brun)
            if flame:
                screen.blit(self.flame, (run, rise))
            else:
                screen.blit(self.bullet, (run, rise))   
    
    
    
    
    def shotgun_create_shot(self, enemy_posX, enemy_posY, imagesx, imagesy, badaim, angle):
        ang = -37
        for i in range(8):
            ang += 7
            if angle + ang < 0:
                pos = 360 - (angle + ang)
            elif angle + ang > 360:
                pos = 360 - angle + ang
            else:
                pos = angle + ang
            
            if pos > 360 or pos < 0:
                continue    
            self.shoot_you(enemy_posX, enemy_posY, imagesx, imagesy, badaim, pos)
    
            
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
        
        
        if int(angle) == 0:
            mousepos = (enemy_posX - imagesx - self.mainx + 170, enemy_posY - imagesy - self.mainy +  19)
        if int(angle) == 32:
            mousepos = (enemy_posX - imagesx - self.mainx + 637, enemy_posY - imagesy - self.mainy +  60)
        if int(angle) == 294:
            mousepos = (enemy_posX - imagesx - self.mainx + 637, enemy_posY - imagesy - self.mainy +  60)
        if int(angle) == 217:
            mousepos = (enemy_posX - imagesx - self.mainx + 432, enemy_posY - imagesy - self.mainy +  479)
        if int(angle) == 207:
            mousepos = (enemy_posX - imagesx - self.mainx + 425, enemy_posY - imagesy - self.mainy +  479)
        if int(angle) == 206:
            mousepos = (enemy_posX - imagesx - self.mainx + 425, enemy_posY - imagesy - self.mainy +  479)
        if int(angle) == 205:
            mousepos = (enemy_posX - imagesx - self.mainx + 422, enemy_posY - imagesy - self.mainy +  479)
        if int(angle) == 204:
            mousepos = (enemy_posX - imagesx - self.mainx + 405, enemy_posY - imagesy - self.mainy +  479)
        if int(angle) == 202:
            mousepos = (enemy_posX - imagesx - self.mainx + 399, enemy_posY - imagesy - self.mainy +  479)
        if int(angle) == 201:
            mousepos = (enemy_posX - imagesx - self.mainx + 398, enemy_posY - imagesy - self.mainy +  479)
        if int(angle) == 200:
            mousepos = (enemy_posX - imagesx - self.mainx + 396, enemy_posY - imagesy - self.mainy +  479)
        if int(angle) == 199:
            mousepos = (enemy_posX - imagesx - self.mainx + 367, enemy_posY - imagesy - self.mainy +  479)
        if int(angle) == 195:
            mousepos = (enemy_posX - imagesx - self.mainx + 360, enemy_posY - imagesy - self.mainy +  479)
        if int(angle) == 193:
            mousepos = (enemy_posX - imagesx - self.mainx + 357, enemy_posY - imagesy - self.mainy +  479)
        if int(angle) == 192:
            mousepos = (enemy_posX - imagesx - self.mainx + 355, enemy_posY - imagesy - self.mainy +  479)
        if int(angle) == 191:
            mousepos = (enemy_posX - imagesx - self.mainx + 346, enemy_posY - imagesy - self.mainy +  479)
        if int(angle) == 190:
            mousepos = (enemy_posX - imagesx - self.mainx + 346, enemy_posY - imagesy - self.mainy +  479)
        if int(angle) == 196:
            mousepos = (enemy_posX - imagesx - self.mainx + 368, enemy_posY - imagesy - self.mainy +  467)
        if int(angle) == 197:
            mousepos = (enemy_posX - imagesx - self.mainx + 374, enemy_posY - imagesy - self.mainy +  466)
        if int(angle) == 194:
            mousepos = (enemy_posX - imagesx - self.mainx + 356, enemy_posY - imagesy - self.mainy +  466)
        if int(angle) == 189:
            mousepos = (enemy_posX - imagesx - self.mainx + 336, enemy_posY - imagesy - self.mainy +  470)
        if int(angle) == 187:
            mousepos = (enemy_posX - imagesx - self.mainx + 328, enemy_posY - imagesy - self.mainy +  472)
        if int(angle) == 185:
            mousepos = (enemy_posX - imagesx - self.mainx + 320, enemy_posY - imagesy - self.mainy +  472)
        if int(angle) == 184:
            mousepos = (enemy_posX - imagesx - self.mainx + 316, enemy_posY - imagesy - self.mainy +  472)
        if int(angle) == 183:
            mousepos = (enemy_posX - imagesx - self.mainx + 312, enemy_posY - imagesy - self.mainy +  472)
        if int(angle) == 182:
            mousepos = (enemy_posX - imagesx - self.mainx + 304, enemy_posY - imagesy - self.mainy +  472)
        if int(angle) == 181:
            mousepos = (enemy_posX - imagesx - self.mainx + 298, enemy_posY - imagesy - self.mainy +  472)
        if int(angle) == 180:
            mousepos = (enemy_posX - imagesx - self.mainx + 298, enemy_posY - imagesy - self.mainy +  472)
        if int(angle) == 179:
            mousepos = (enemy_posX - imagesx - self.mainx + 288, enemy_posY - imagesy - self.mainy +  468)
        if int(angle) == 178:
            mousepos = (enemy_posX - imagesx - self.mainx + 284, enemy_posY - imagesy - self.mainy +  466)
        if int(angle) == 177:
            mousepos = (enemy_posX - imagesx - self.mainx + 280, enemy_posY - imagesy - self.mainy +  466)
        if int(angle) == 176:
            mousepos = (enemy_posX - imagesx - self.mainx + 278, enemy_posY - imagesy - self.mainy +  466)
        if int(angle) == 174:
            mousepos = (enemy_posX - imagesx - self.mainx + 266, enemy_posY - imagesy - self.mainy +  466)
        if int(angle) == 173:
            mousepos = (enemy_posX - imagesx - self.mainx + 264, enemy_posY - imagesy - self.mainy +  468)
        if int(angle) == 172:
            mousepos = (enemy_posX - imagesx - self.mainx + 258, enemy_posY - imagesy - self.mainy +  466)
        if int(angle) == 171:
            mousepos = (enemy_posX - imagesx - self.mainx + 257, enemy_posY - imagesy - self.mainy +  466)
        if int(angle) == 186:
            mousepos = (enemy_posX - imagesx - self.mainx + 324, enemy_posY - imagesy - self.mainy +  472)
        if int(angle) == 188:
            mousepos = (enemy_posX - imagesx - self.mainx + 334, enemy_posY - imagesy - self.mainy +  470)
        if int(angle) == 198:
            mousepos = (enemy_posX - imagesx - self.mainx + 378, enemy_posY - imagesy - self.mainy +  464)
        if int(angle) == 203:
            mousepos = (enemy_posX - imagesx - self.mainx + 395, enemy_posY - imagesy - self.mainy +  447)
        if int(angle) == 208:
            mousepos = (enemy_posX - imagesx - self.mainx + 418, enemy_posY - imagesy - self.mainy +  441)
        if int(angle) == 209:
            mousepos = (enemy_posX - imagesx - self.mainx + 420, enemy_posY - imagesy - self.mainy +  440)
        if int(angle) == 210:
            mousepos = (enemy_posX - imagesx - self.mainx + 427, enemy_posY - imagesy - self.mainy +  437)
        if int(angle) == 211:
            mousepos = (enemy_posX - imagesx - self.mainx + 428, enemy_posY - imagesy - self.mainy +  434)
        if int(angle) == 212:
            mousepos = (enemy_posX - imagesx - self.mainx + 434, enemy_posY - imagesy - self.mainy +  432)
        if int(angle) == 213:
            mousepos = (enemy_posX - imagesx - self.mainx + 437, enemy_posY - imagesy - self.mainy +  433)
        if int(angle) == 214:
            mousepos = (enemy_posX - imagesx - self.mainx + 440, enemy_posY - imagesy - self.mainy +  428)
        if int(angle) == 215:
            mousepos = (enemy_posX - imagesx - self.mainx + 445, enemy_posY - imagesy - self.mainy +  427)
        if int(angle) == 216:
            mousepos = (enemy_posX - imagesx - self.mainx + 450, enemy_posY - imagesy - self.mainy +  426)
        if int(angle) == 218:
            mousepos = (enemy_posX - imagesx - self.mainx + 456, enemy_posY - imagesy - self.mainy +  418)
        if int(angle) == 219:
            mousepos = (enemy_posX - imagesx - self.mainx + 460, enemy_posY - imagesy - self.mainy +  418)
        if int(angle) == 220:
            mousepos = (enemy_posX - imagesx - self.mainx + 464, enemy_posY - imagesy - self.mainy +  414)
        if int(angle) == 221:
            mousepos = (enemy_posX - imagesx - self.mainx + 468, enemy_posY - imagesy - self.mainy +  412)
        if int(angle) == 222:
            mousepos = (enemy_posX - imagesx - self.mainx + 469, enemy_posY - imagesy - self.mainy +  407)
        if int(angle) == 223:
            mousepos = (enemy_posX - imagesx - self.mainx + 469, enemy_posY - imagesy - self.mainy +  401)
        if int(angle) == 224:
            mousepos = (enemy_posX - imagesx - self.mainx + 472, enemy_posY - imagesy - self.mainy +  398)
        if int(angle) == 225:
            mousepos = (enemy_posX - imagesx - self.mainx + 476, enemy_posY - imagesy - self.mainy +  396)
        if int(angle) == 226:
            mousepos = (enemy_posX - imagesx - self.mainx + 479, enemy_posY - imagesy - self.mainy +  391)
        if int(angle) == 227:
            mousepos = (enemy_posX - imagesx - self.mainx + 484, enemy_posY - imagesy - self.mainy +  390)
        if int(angle) == 228:
            mousepos = (enemy_posX - imagesx - self.mainx + 487, enemy_posY - imagesy - self.mainy +  387)
        if int(angle) == 229:
            mousepos = (enemy_posX - imagesx - self.mainx + 493, enemy_posY - imagesy - self.mainy +  385)
        if int(angle) == 230:
            mousepos = (enemy_posX - imagesx - self.mainx + 496, enemy_posY - imagesy - self.mainy +  381)
        if int(angle) == 231:
            mousepos = (enemy_posX - imagesx - self.mainx + 498, enemy_posY - imagesy - self.mainy +  378)
        if int(angle) == 232:
            mousepos = (enemy_posX - imagesx - self.mainx + 501, enemy_posY - imagesy - self.mainy +  375)
        if int(angle) == 233:
            mousepos = (enemy_posX - imagesx - self.mainx + 506, enemy_posY - imagesy - self.mainy +  368)
        if int(angle) == 234:
            mousepos = (enemy_posX - imagesx - self.mainx + 506, enemy_posY - imagesy - self.mainy +  366)
        if int(angle) == 235:
            mousepos = (enemy_posX - imagesx - self.mainx + 512, enemy_posY - imagesy - self.mainy +  364)
        if int(angle) == 236:
            mousepos = (enemy_posX - imagesx - self.mainx + 513, enemy_posY - imagesy - self.mainy +  359)
        if int(angle) == 237:
            mousepos = (enemy_posX - imagesx - self.mainx + 514, enemy_posY - imagesy - self.mainy +  354)
        if int(angle) == 238:
            mousepos = (enemy_posX - imagesx - self.mainx + 516, enemy_posY - imagesy - self.mainy +  350)
        if int(angle) == 239:
            mousepos = (enemy_posX - imagesx - self.mainx + 519, enemy_posY - imagesy - self.mainy +  347)
        if int(angle) == 240:
            mousepos = (enemy_posX - imagesx - self.mainx + 520, enemy_posY - imagesy - self.mainy +  340)
        if int(angle) == 241:
            mousepos = (enemy_posX - imagesx - self.mainx + 523, enemy_posY - imagesy - self.mainy +  335)
        if int(angle) == 242:
            mousepos = (enemy_posX - imagesx - self.mainx + 523, enemy_posY - imagesy - self.mainy +  335)
        if int(angle) == 243:
            mousepos = (enemy_posX - imagesx - self.mainx + 526, enemy_posY - imagesy - self.mainy +  329)
        if int(angle) == 244:
            mousepos = (enemy_posX - imagesx - self.mainx + 527, enemy_posY - imagesy - self.mainy +  327)
        if int(angle) == 245:
            mousepos = (enemy_posX - imagesx - self.mainx + 530, enemy_posY - imagesy - self.mainy +  320)
        if int(angle) == 246:
            mousepos = (enemy_posX - imagesx - self.mainx + 531, enemy_posY - imagesy - self.mainy +  319)
        if int(angle) == 247:
            mousepos = (enemy_posX - imagesx - self.mainx + 534, enemy_posY - imagesy - self.mainy +  314)
        if int(angle) == 248:
            mousepos = (enemy_posX - imagesx - self.mainx + 537, enemy_posY - imagesy - self.mainy +  311)
        if int(angle) == 249:
            mousepos = (enemy_posX - imagesx - self.mainx + 540, enemy_posY - imagesy - self.mainy +  306)
        if int(angle) == 250:
            mousepos = (enemy_posX - imagesx - self.mainx + 543, enemy_posY - imagesy - self.mainy +  303)
        if int(angle) == 251:
            mousepos = (enemy_posX - imagesx - self.mainx + 543, enemy_posY - imagesy - self.mainy +  299)
        if int(angle) == 252:
            mousepos = (enemy_posX - imagesx - self.mainx + 543, enemy_posY - imagesy - self.mainy +  295)
        if int(angle) == 253:
            mousepos = (enemy_posX - imagesx - self.mainx + 545, enemy_posY - imagesy - self.mainy +  291)
        if int(angle) == 254:
            mousepos = (enemy_posX - imagesx - self.mainx + 545, enemy_posY - imagesy - self.mainy +  285)
        if int(angle) == 255:
            mousepos = (enemy_posX - imagesx - self.mainx + 545, enemy_posY - imagesy - self.mainy +  281)
        if int(angle) == 256:
            mousepos = (enemy_posX - imagesx - self.mainx + 547, enemy_posY - imagesy - self.mainy +  277)
        if int(angle) == 257:
            mousepos = (enemy_posX - imagesx - self.mainx + 547, enemy_posY - imagesy - self.mainy +  273)
        if int(angle) == 258:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  267)
        if int(angle) == 259:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  263)
        if int(angle) == 260:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  253)
        if int(angle) == 261:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  253)
        if int(angle) == 262:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  249)
        if int(angle) == 263:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  245)
        if int(angle) == 264:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  241)
        if int(angle) == 265:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  237)
        if int(angle) == 266:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  231)
        if int(angle) == 267:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  227)
        if int(angle) == 268:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  223)
        if int(angle) == 269:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  219)
        if int(angle) == 270:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  215)
        if int(angle) == 271:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  209)
        if int(angle) == 272:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  205)
        if int(angle) == 273:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  201)
        if int(angle) == 274:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  197)
        if int(angle) == 275:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  191)
        if int(angle) == 276:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  187)
        if int(angle) == 277:
            mousepos = (enemy_posX - imagesx - self.mainx + 550, enemy_posY - imagesy - self.mainy +  183)
        if int(angle) == 278:
            mousepos = (enemy_posX - imagesx - self.mainx + 550, enemy_posY - imagesy - self.mainy +  178)
        if int(angle) == 279:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  173)
        if int(angle) == 280:
            mousepos = (enemy_posX - imagesx - self.mainx + 549, enemy_posY - imagesy - self.mainy +  169)
        if int(angle) == 281:
            mousepos = (enemy_posX - imagesx - self.mainx + 548, enemy_posY - imagesy - self.mainy +  164)
        if int(angle) == 282:
            mousepos = (enemy_posX - imagesx - self.mainx + 547, enemy_posY - imagesy - self.mainy +  161)
        if int(angle) == 283:
            mousepos = (enemy_posX - imagesx - self.mainx + 545, enemy_posY - imagesy - self.mainy +  157)
        if int(angle) == 284:
            mousepos = (enemy_posX - imagesx - self.mainx + 540, enemy_posY - imagesy - self.mainy +  147)
        if int(angle) == 285:
            mousepos = (enemy_posX - imagesx - self.mainx + 539, enemy_posY - imagesy - self.mainy +  143)
        if int(angle) == 286:
            mousepos = (enemy_posX - imagesx - self.mainx + 539, enemy_posY - imagesy - self.mainy +  143)
        if int(angle) == 287:
            mousepos = (enemy_posX - imagesx - self.mainx + 538, enemy_posY - imagesy - self.mainy +  140)
        if int(angle) == 288:
            mousepos = (enemy_posX - imagesx - self.mainx + 530, enemy_posY - imagesy - self.mainy +  138)
        if int(angle) == 289:
            mousepos = (enemy_posX - imagesx - self.mainx + 525, enemy_posY - imagesy - self.mainy +  133)
        if int(angle) == 291:
            mousepos = (enemy_posX - imagesx - self.mainx + 520, enemy_posY - imagesy - self.mainy +  128)
        if int(angle) == 292:
            mousepos = (enemy_posX - imagesx - self.mainx + 517, enemy_posY - imagesy - self.mainy +  125)
        if int(angle) == 295:
            mousepos = (enemy_posX - imagesx - self.mainx + 513, enemy_posY - imagesy - self.mainy +  111)
        if int(angle) == 296:
            mousepos = (enemy_posX - imagesx - self.mainx + 510, enemy_posY - imagesy - self.mainy +  106)
        if int(angle) == 297:
            mousepos = (enemy_posX - imagesx - self.mainx + 509, enemy_posY - imagesy - self.mainy +  105)
        if int(angle) == 298:
            mousepos = (enemy_posX - imagesx - self.mainx + 507, enemy_posY - imagesy - self.mainy +  101)
        if int(angle) == 299:
            mousepos = (enemy_posX - imagesx - self.mainx + 507, enemy_posY - imagesy - self.mainy +  97)
        if int(angle) == 300:
            mousepos = (enemy_posX - imagesx - self.mainx + 501, enemy_posY - imagesy - self.mainy +  87)
        if int(angle) == 301:
            mousepos = (enemy_posX - imagesx - self.mainx + 501, enemy_posY - imagesy - self.mainy +  87)
        if int(angle) == 302:
            mousepos = (enemy_posX - imagesx - self.mainx + 498, enemy_posY - imagesy - self.mainy +  86)
        if int(angle) == 303:
            mousepos = (enemy_posX - imagesx - self.mainx + 488, enemy_posY - imagesy - self.mainy +  82)
        if int(angle) == 304:
            mousepos = (enemy_posX - imagesx - self.mainx + 488, enemy_posY - imagesy - self.mainy +  82)
        if int(angle) == 305:
            mousepos = (enemy_posX - imagesx - self.mainx + 485, enemy_posY - imagesy - self.mainy +  81)
        if int(angle) == 306:
            mousepos = (enemy_posX - imagesx - self.mainx + 485, enemy_posY - imagesy - self.mainy +  75)
        if int(angle) == 307:
            mousepos = (enemy_posX - imagesx - self.mainx + 482, enemy_posY - imagesy - self.mainy +  70)
        if int(angle) == 308:
            mousepos = (enemy_posX - imagesx - self.mainx + 481, enemy_posY - imagesy - self.mainy +  69)
        if int(angle) == 309:
            mousepos = (enemy_posX - imagesx - self.mainx + 475, enemy_posY - imagesy - self.mainy +  61)
        if int(angle) == 310:
            mousepos = (enemy_posX - imagesx - self.mainx + 474, enemy_posY - imagesy - self.mainy +  60)
        if int(angle) == 311:
            mousepos = (enemy_posX - imagesx - self.mainx + 472, enemy_posY - imagesy - self.mainy +  60)
        if int(angle) == 313:
            mousepos = (enemy_posX - imagesx - self.mainx + 454, enemy_posY - imagesy - self.mainy +  60)
        if int(angle) == 314:
            mousepos = (enemy_posX - imagesx - self.mainx + 454, enemy_posY - imagesy - self.mainy +  60)
        if int(angle) == 315:
            mousepos = (enemy_posX - imagesx - self.mainx + 448, enemy_posY - imagesy - self.mainy +  58)
        if int(angle) == 316:
            mousepos = (enemy_posX - imagesx - self.mainx + 445, enemy_posY - imagesy - self.mainy +  55)
        if int(angle) == 317:
            mousepos = (enemy_posX - imagesx - self.mainx + 444, enemy_posY - imagesy - self.mainy +  54)
        if int(angle) == 318:
            mousepos = (enemy_posX - imagesx - self.mainx + 443, enemy_posY - imagesy - self.mainy +  47)
        if int(angle) == 312:
            mousepos = (enemy_posX - imagesx - self.mainx + 466, enemy_posY - imagesy - self.mainy +  59)
        if int(angle) == 320:
            mousepos = (enemy_posX - imagesx - self.mainx + 434, enemy_posY - imagesy - self.mainy +  47)
        if int(angle) == 321:
            mousepos = (enemy_posX - imagesx - self.mainx + 432, enemy_posY - imagesy - self.mainy +  44)
        if int(angle) == 322:
            mousepos = (enemy_posX - imagesx - self.mainx + 423, enemy_posY - imagesy - self.mainy +  37)
        if int(angle) == 324:
            mousepos = (enemy_posX - imagesx - self.mainx + 423, enemy_posY - imagesy - self.mainy +  37)
        if int(angle) == 325:
            mousepos = (enemy_posX - imagesx - self.mainx + 420, enemy_posY - imagesy - self.mainy +  34)
        if int(angle) == 326:
            mousepos = (enemy_posX - imagesx - self.mainx + 410, enemy_posY - imagesy - self.mainy +  30)
        if int(angle) == 328:
            mousepos = (enemy_posX - imagesx - self.mainx + 410, enemy_posY - imagesy - self.mainy +  30)
        if int(angle) == 329:
            mousepos = (enemy_posX - imagesx - self.mainx + 408, enemy_posY - imagesy - self.mainy +  26)
        if int(angle) == 330:
            mousepos = (enemy_posX - imagesx - self.mainx + 394, enemy_posY - imagesy - self.mainy +  26)
        if int(angle) == 332:
            mousepos = (enemy_posX - imagesx - self.mainx + 390, enemy_posY - imagesy - self.mainy +  26)
        if int(angle) == 333:
            mousepos = (enemy_posX - imagesx - self.mainx + 390, enemy_posY - imagesy - self.mainy +  26)
        if int(angle) == 327:
            mousepos = (enemy_posX - imagesx - self.mainx + 418, enemy_posY - imagesy - self.mainy +  28)
        if int(angle) == 323:
            mousepos = (enemy_posX - imagesx - self.mainx + 430, enemy_posY - imagesy - self.mainy +  33)
        if int(angle) == 331:
            mousepos = (enemy_posX - imagesx - self.mainx + 395, enemy_posY - imagesy - self.mainy +  25)
        if int(angle) == 334:
            mousepos = (enemy_posX - imagesx - self.mainx + 386, enemy_posY - imagesy - self.mainy +  22)
        if int(angle) == 335:
            mousepos = (enemy_posX - imagesx - self.mainx + 384, enemy_posY - imagesy - self.mainy +  22)
        if int(angle) == 337:
            mousepos = (enemy_posX - imagesx - self.mainx + 378, enemy_posY - imagesy - self.mainy +  18)
        if int(angle) == 338:
            mousepos = (enemy_posX - imagesx - self.mainx + 374, enemy_posY - imagesy - self.mainy +  18)
        if int(angle) == 339:
            mousepos = (enemy_posX - imagesx - self.mainx + 370, enemy_posY - imagesy - self.mainy +  16)
        if int(angle) == 340:
            mousepos = (enemy_posX - imagesx - self.mainx + 366, enemy_posY - imagesy - self.mainy +  14)
        if int(angle) == 341:
            mousepos = (enemy_posX - imagesx - self.mainx + 362, enemy_posY - imagesy - self.mainy +  14)
        if int(angle) == 336:
            mousepos = (enemy_posX - imagesx - self.mainx + 382, enemy_posY - imagesy - self.mainy +  16)
        if int(angle) == 342:
            mousepos = (enemy_posX - imagesx - self.mainx + 358, enemy_posY - imagesy - self.mainy +  14)
        if int(angle) == 343:
            mousepos = (enemy_posX - imagesx - self.mainx + 354, enemy_posY - imagesy - self.mainy +  14)
        if int(angle) == 344:
            mousepos = (enemy_posX - imagesx - self.mainx + 348, enemy_posY - imagesy - self.mainy +  14)
        if int(angle) == 345:
            mousepos = (enemy_posX - imagesx - self.mainx + 348, enemy_posY - imagesy - self.mainy +  14)
        if int(angle) == 346:
            mousepos = (enemy_posX - imagesx - self.mainx + 344, enemy_posY - imagesy - self.mainy +  14)
        if int(angle) == 347:
            mousepos = (enemy_posX - imagesx - self.mainx + 340, enemy_posY - imagesy - self.mainy +  14)
        if int(angle) == 348:
            mousepos = (enemy_posX - imagesx - self.mainx + 336, enemy_posY - imagesy - self.mainy +  14)
        if int(angle) == 349:
            mousepos = (enemy_posX - imagesx - self.mainx + 334, enemy_posY - imagesy - self.mainy +  14)
        if int(angle) == 351:
            mousepos = (enemy_posX - imagesx - self.mainx + 324, enemy_posY - imagesy - self.mainy +  10)
        if int(angle) == 352:
            mousepos = (enemy_posX - imagesx - self.mainx + 322, enemy_posY - imagesy - self.mainy +  10)
        if int(angle) == 353:
            mousepos = (enemy_posX - imagesx - self.mainx + 318, enemy_posY - imagesy - self.mainy +  10)
        if int(angle) == 350:
            mousepos = (enemy_posX - imagesx - self.mainx + 330, enemy_posY - imagesy - self.mainy +  8)
        if int(angle) == 354:
            mousepos = (enemy_posX - imagesx - self.mainx + 316, enemy_posY - imagesy - self.mainy +  8)
        if int(angle) == 355:
            mousepos = (enemy_posX - imagesx - self.mainx + 312, enemy_posY - imagesy - self.mainy +  8)
        if int(angle) == 356:
            mousepos = (enemy_posX - imagesx - self.mainx + 308, enemy_posY - imagesy - self.mainy +  8)
        if int(angle) == 357:
            mousepos = (enemy_posX - imagesx - self.mainx + 305, enemy_posY - imagesy - self.mainy +  7)
        if int(angle) == 358:
            mousepos = (enemy_posX - imagesx - self.mainx + 302, enemy_posY - imagesy - self.mainy +  6)
        if int(angle) == 359:
            mousepos = (enemy_posX - imagesx - self.mainx + 298, enemy_posY - imagesy - self.mainy +  6)
        if int(angle) == 1:
            mousepos = (enemy_posX - imagesx - self.mainx + 290, enemy_posY - imagesy - self.mainy +  8)
        if int(angle) == 2:
            mousepos = (enemy_posX - imagesx - self.mainx + 284, enemy_posY - imagesy - self.mainy +  8)
        if int(angle) == 3:
            mousepos = (enemy_posX - imagesx - self.mainx + 284, enemy_posY - imagesy - self.mainy +  8)
        if int(angle) == 4:
            mousepos = (enemy_posX - imagesx - self.mainx + 280, enemy_posY - imagesy - self.mainy +  8)
        if int(angle) == 5:
            mousepos = (enemy_posX - imagesx - self.mainx + 274, enemy_posY - imagesy - self.mainy +  8)
        if int(angle) == 6:
            mousepos = (enemy_posX - imagesx - self.mainx + 273, enemy_posY - imagesy - self.mainy +  7)
        if int(angle) == 7:
            mousepos = (enemy_posX - imagesx - self.mainx + 268, enemy_posY - imagesy - self.mainy +  10)
        if int(angle) == 8:
            mousepos = (enemy_posX - imagesx - self.mainx + 264, enemy_posY - imagesy - self.mainy +  10)
        if int(angle) == 9:
            mousepos = (enemy_posX - imagesx - self.mainx + 260, enemy_posY - imagesy - self.mainy +  10)
        if int(angle) == 10:
            mousepos = (enemy_posX - imagesx - self.mainx + 256, enemy_posY - imagesy - self.mainy +  12)
        if int(angle) == 11:
            mousepos = (enemy_posX - imagesx - self.mainx + 255, enemy_posY - imagesy - self.mainy +  13)
        if int(angle) == 12:
            mousepos = (enemy_posX - imagesx - self.mainx + 252, enemy_posY - imagesy - self.mainy +  21)
        if int(angle) == 13:
            mousepos = (enemy_posX - imagesx - self.mainx + 248, enemy_posY - imagesy - self.mainy +  22)
        if int(angle) == 14:
            mousepos = (enemy_posX - imagesx - self.mainx + 244, enemy_posY - imagesy - self.mainy +  24)
        if int(angle) == 15:
            mousepos = (enemy_posX - imagesx - self.mainx + 242, enemy_posY - imagesy - self.mainy +  24)
        if int(angle) == 16:
            mousepos = (enemy_posX - imagesx - self.mainx + 240, enemy_posY - imagesy - self.mainy +  24)
        if int(angle) == 17:
            mousepos = (enemy_posX - imagesx - self.mainx + 233, enemy_posY - imagesy - self.mainy +  29)
        if int(angle) == 18:
            mousepos = (enemy_posX - imagesx - self.mainx + 233, enemy_posY - imagesy - self.mainy +  29)
        if int(angle) == 20:
            mousepos = (enemy_posX - imagesx - self.mainx + 226, enemy_posY - imagesy - self.mainy +  34)
        if int(angle) == 19:
            mousepos = (enemy_posX - imagesx - self.mainx + 234, enemy_posY - imagesy - self.mainy +  32)
        if int(angle) == 21:
            mousepos = (enemy_posX - imagesx - self.mainx + 222, enemy_posY - imagesy - self.mainy +  28)
        if int(angle) == 22:
            mousepos = (enemy_posX - imagesx - self.mainx + 218, enemy_posY - imagesy - self.mainy +  30)
        if int(angle) == 23:
            mousepos = (enemy_posX - imagesx - self.mainx + 216, enemy_posY - imagesy - self.mainy +  32)
        if int(angle) == 24:
            mousepos = (enemy_posX - imagesx - self.mainx + 212, enemy_posY - imagesy - self.mainy +  32)
        if int(angle) == 25:
            mousepos = (enemy_posX - imagesx - self.mainx + 208, enemy_posY - imagesy - self.mainy +  34)
        if int(angle) == 26:
            mousepos = (enemy_posX - imagesx - self.mainx + 206, enemy_posY - imagesy - self.mainy +  34)
        if int(angle) == 27:
            mousepos = (enemy_posX - imagesx - self.mainx + 198, enemy_posY - imagesy - self.mainy +  38)
        if int(angle) == 28:
            mousepos = (enemy_posX - imagesx - self.mainx + 198, enemy_posY - imagesy - self.mainy +  38)
        if int(angle) == 29:
            mousepos = (enemy_posX - imagesx - self.mainx + 197, enemy_posY - imagesy - self.mainy +  39)
        if int(angle) == 30:
            mousepos = (enemy_posX - imagesx - self.mainx + 192, enemy_posY - imagesy - self.mainy +  44)
        if int(angle) == 31:
            mousepos = (enemy_posX - imagesx - self.mainx + 192, enemy_posY - imagesy - self.mainy +  44)
        if int(angle) == 33:
            mousepos = (enemy_posX - imagesx - self.mainx + 174, enemy_posY - imagesy - self.mainy +  52)
        if int(angle) == 36:
            mousepos = (enemy_posX - imagesx - self.mainx + 169, enemy_posY - imagesy - self.mainy +  57)
        if int(angle) == 38:
            mousepos = (enemy_posX - imagesx - self.mainx + 169, enemy_posY - imagesy - self.mainy +  57)
        if int(angle) == 37:
            mousepos = (enemy_posX - imagesx - self.mainx + 174, enemy_posY - imagesy - self.mainy +  54)
        if int(angle) == 35:
            mousepos = (enemy_posX - imagesx - self.mainx + 179, enemy_posY - imagesy - self.mainy +  51)
        if int(angle) == 34:
            mousepos = (enemy_posX - imagesx - self.mainx + 180, enemy_posY - imagesy - self.mainy +  50)
        if int(angle) == 39:
            mousepos = (enemy_posX - imagesx - self.mainx + 169, enemy_posY - imagesy - self.mainy +  63)
        if int(angle) == 40:
            mousepos = (enemy_posX - imagesx - self.mainx + 168, enemy_posY - imagesy - self.mainy +  64)
        if int(angle) == 41:
            mousepos = (enemy_posX - imagesx - self.mainx + 165, enemy_posY - imagesy - self.mainy +  69)
        if int(angle) == 42:
            mousepos = (enemy_posX - imagesx - self.mainx + 164, enemy_posY - imagesy - self.mainy +  70)
        if int(angle) == 43:
            mousepos = (enemy_posX - imagesx - self.mainx + 161, enemy_posY - imagesy - self.mainy +  73)
        if int(angle) == 44:
            mousepos = (enemy_posX - imagesx - self.mainx + 159, enemy_posY - imagesy - self.mainy +  75)
        if int(angle) == 45:
            mousepos = (enemy_posX - imagesx - self.mainx + 158, enemy_posY - imagesy - self.mainy +  80)
        if int(angle) == 46:
            mousepos = (enemy_posX - imagesx - self.mainx + 156, enemy_posY - imagesy - self.mainy +  82)
        if int(angle) == 47:
            mousepos = (enemy_posX - imagesx - self.mainx + 152, enemy_posY - imagesy - self.mainy +  84)
        if int(angle) == 48:
            mousepos = (enemy_posX - imagesx - self.mainx + 149, enemy_posY - imagesy - self.mainy +  87)
        if int(angle) == 49:
            mousepos = (enemy_posX - imagesx - self.mainx + 148, enemy_posY - imagesy - self.mainy +  90)
        if int(angle) == 50:
            mousepos = (enemy_posX - imagesx - self.mainx + 147, enemy_posY - imagesy - self.mainy +  91)
        if int(angle) == 51:
            mousepos = (enemy_posX - imagesx - self.mainx + 143, enemy_posY - imagesy - self.mainy +  93)
        if int(angle) == 52:
            mousepos = (enemy_posX - imagesx - self.mainx + 143, enemy_posY - imagesy - self.mainy +  99)
        if int(angle) == 53:
            mousepos = (enemy_posX - imagesx - self.mainx + 141, enemy_posY - imagesy - self.mainy +  101)
        if int(angle) == 54:
            mousepos = (enemy_posX - imagesx - self.mainx + 139, enemy_posY - imagesy - self.mainy +  103)
        if int(angle) == 55:
            mousepos = (enemy_posX - imagesx - self.mainx + 136, enemy_posY - imagesy - self.mainy +  105)
        if int(angle) == 56:
            mousepos = (enemy_posX - imagesx - self.mainx + 133, enemy_posY - imagesy - self.mainy +  107)
        if int(angle) == 57:
            mousepos = (enemy_posX - imagesx - self.mainx + 133, enemy_posY - imagesy - self.mainy +  113)
        if int(angle) == 58:
            mousepos = (enemy_posX - imagesx - self.mainx + 132, enemy_posY - imagesy - self.mainy +  116)
        if int(angle) == 59:
            mousepos = (enemy_posX - imagesx - self.mainx + 130, enemy_posY - imagesy - self.mainy +  117)
        if int(angle) == 60:
            mousepos = (enemy_posX - imagesx - self.mainx + 127, enemy_posY - imagesy - self.mainy +  119)
        if int(angle) == 61:
            mousepos = (enemy_posX - imagesx - self.mainx + 127, enemy_posY - imagesy - self.mainy +  125)
        if int(angle) == 63:
            mousepos = (enemy_posX - imagesx - self.mainx + 123, enemy_posY - imagesy - self.mainy +  129)
        if int(angle) == 62:
            mousepos = (enemy_posX - imagesx - self.mainx + 125, enemy_posY - imagesy - self.mainy +  125)
        if int(angle) == 64:
            mousepos = (enemy_posX - imagesx - self.mainx + 115, enemy_posY - imagesy - self.mainy +  129)
        if int(angle) == 66:
            mousepos = (enemy_posX - imagesx - self.mainx + 115, enemy_posY - imagesy - self.mainy +  135)
        if int(angle) == 67:
            mousepos = (enemy_posX - imagesx - self.mainx + 115, enemy_posY - imagesy - self.mainy +  139)
        if int(angle) == 68:
            mousepos = (enemy_posX - imagesx - self.mainx + 115, enemy_posY - imagesy - self.mainy +  143)
        if int(angle) == 69:
            mousepos = (enemy_posX - imagesx - self.mainx + 115, enemy_posY - imagesy - self.mainy +  147)
        if int(angle) == 65:
            mousepos = (enemy_posX - imagesx - self.mainx + 120, enemy_posY - imagesy - self.mainy +  136)
        if int(angle) == 70:
            mousepos = (enemy_posX - imagesx - self.mainx + 117, enemy_posY - imagesy - self.mainy +  151)
        if int(angle) == 71:
            mousepos = (enemy_posX - imagesx - self.mainx + 116, enemy_posY - imagesy - self.mainy +  162)
        if int(angle) == 73:
            mousepos = (enemy_posX - imagesx - self.mainx + 116, enemy_posY - imagesy - self.mainy +  162)
        if int(angle) == 74:
            mousepos = (enemy_posX - imagesx - self.mainx + 115, enemy_posY - imagesy - self.mainy +  165)
        if int(angle) == 75:
            mousepos = (enemy_posX - imagesx - self.mainx + 115, enemy_posY - imagesy - self.mainy +  171)
        if int(angle) == 76:
            mousepos = (enemy_posX - imagesx - self.mainx + 115, enemy_posY - imagesy - self.mainy +  171)
        if int(angle) == 72:
            mousepos = (enemy_posX - imagesx - self.mainx + 115, enemy_posY - imagesy - self.mainy +  159)
        if int(angle) == 77:
            mousepos = (enemy_posX - imagesx - self.mainx + 104, enemy_posY - imagesy - self.mainy +  174)
        if int(angle) == 78:
            mousepos = (enemy_posX - imagesx - self.mainx + 102, enemy_posY - imagesy - self.mainy +  176)
        if int(angle) == 79:
            mousepos = (enemy_posX - imagesx - self.mainx + 100, enemy_posY - imagesy - self.mainy +  178)
        if int(angle) == 80:
            mousepos = (enemy_posX - imagesx - self.mainx + 99, enemy_posY - imagesy - self.mainy +  181)
        if int(angle) == 81:
            mousepos = (enemy_posX - imagesx - self.mainx + 99, enemy_posY - imagesy - self.mainy +  185)
        if int(angle) == 82:
            mousepos = (enemy_posX - imagesx - self.mainx + 99, enemy_posY - imagesy - self.mainy +  189)
        if int(angle) == 83:
            mousepos = (enemy_posX - imagesx - self.mainx + 97, enemy_posY - imagesy - self.mainy +  193)
        if int(angle) == 84:
            mousepos = (enemy_posX - imagesx - self.mainx + 97, enemy_posY - imagesy - self.mainy +  195)
        if int(angle) == 85:
            mousepos = (enemy_posX - imagesx - self.mainx + 97, enemy_posY - imagesy - self.mainy +  201)
        if int(angle) == 86:
            mousepos = (enemy_posX - imagesx - self.mainx + 97, enemy_posY - imagesy - self.mainy +  203)
        if int(angle) == 87:
            mousepos = (enemy_posX - imagesx - self.mainx + 97, enemy_posY - imagesy - self.mainy +  205)
        if int(angle) == 88:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  213)
        if int(angle) == 89:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  217)
        if int(angle) == 90:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  221)
        if int(angle) == 91:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  221)
        if int(angle) == 92:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  223)
        if int(angle) == 93:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  227)
        if int(angle) == 94:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  229)
        if int(angle) == 95:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  233)
        if int(angle) == 96:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  239)
        if int(angle) == 97:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  243)
        if int(angle) == 98:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  245)
        if int(angle) == 99:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  253)
        if int(angle) == 100:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  253)
        if int(angle) == 101:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  255)
        if int(angle) == 102:
            mousepos = (enemy_posX - imagesx - self.mainx + 93, enemy_posY - imagesy - self.mainy +  261)
        if int(angle) == 103:
            mousepos = (enemy_posX - imagesx - self.mainx + 93, enemy_posY - imagesy - self.mainy +  267)
        if int(angle) == 104:
            mousepos = (enemy_posX - imagesx - self.mainx + 93, enemy_posY - imagesy - self.mainy +  267)
        if int(angle) == 105:
            mousepos = (enemy_posX - imagesx - self.mainx + 93, enemy_posY - imagesy - self.mainy +  271)
        if int(angle) == 106:
            mousepos = (enemy_posX - imagesx - self.mainx + 94, enemy_posY - imagesy - self.mainy +  274)
        if int(angle) == 107:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  279)
        if int(angle) == 108:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  282)
        if int(angle) == 109:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  285)
        if int(angle) == 110:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  291)
        if int(angle) == 111:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  295)
        if int(angle) == 112:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  299)
        if int(angle) == 113:
            mousepos = (enemy_posX - imagesx - self.mainx + 95, enemy_posY - imagesy - self.mainy +  303)
        if int(angle) == 114:
            mousepos = (enemy_posX - imagesx - self.mainx + 97, enemy_posY - imagesy - self.mainy +  307)
        if int(angle) == 116:
            mousepos = (enemy_posX - imagesx - self.mainx + 101, enemy_posY - imagesy - self.mainy +  315)
        if int(angle) == 117:
            mousepos = (enemy_posX - imagesx - self.mainx + 101, enemy_posY - imagesy - self.mainy +  317)
        if int(angle) == 118:
            mousepos = (enemy_posX - imagesx - self.mainx + 103, enemy_posY - imagesy - self.mainy +  323)
        if int(angle) == 119:
            mousepos = (enemy_posX - imagesx - self.mainx + 103, enemy_posY - imagesy - self.mainy +  323)
        if int(angle) == 120:
            mousepos = (enemy_posX - imagesx - self.mainx + 105, enemy_posY - imagesy - self.mainy +  331)
        if int(angle) == 121:
            mousepos = (enemy_posX - imagesx - self.mainx + 105, enemy_posY - imagesy - self.mainy +  333)
        if int(angle) == 122:
            mousepos = (enemy_posX - imagesx - self.mainx + 105, enemy_posY - imagesy - self.mainy +  338)
        if int(angle) == 123:
            mousepos = (enemy_posX - imagesx - self.mainx + 105, enemy_posY - imagesy - self.mainy +  341)
        if int(angle) == 124:
            mousepos = (enemy_posX - imagesx - self.mainx + 107, enemy_posY - imagesy - self.mainy +  347)
        if int(angle) == 125:
            mousepos = (enemy_posX - imagesx - self.mainx + 107, enemy_posY - imagesy - self.mainy +  347)
        if int(angle) == 126:
            mousepos = (enemy_posX - imagesx - self.mainx + 108, enemy_posY - imagesy - self.mainy +  354)
        if int(angle) == 127:
            mousepos = (enemy_posX - imagesx - self.mainx + 110, enemy_posY - imagesy - self.mainy +  356)
        if int(angle) == 128:
            mousepos = (enemy_posX - imagesx - self.mainx + 113, enemy_posY - imagesy - self.mainy +  359)
        if int(angle) == 129:
            mousepos = (enemy_posX - imagesx - self.mainx + 116, enemy_posY - imagesy - self.mainy +  363)
        if int(angle) == 130:
            mousepos = (enemy_posX - imagesx - self.mainx + 119, enemy_posY - imagesy - self.mainy +  369)
        if int(angle) == 131:
            mousepos = (enemy_posX - imagesx - self.mainx + 122, enemy_posY - imagesy - self.mainy +  372)
        if int(angle) == 132:
            mousepos = (enemy_posX - imagesx - self.mainx + 125, enemy_posY - imagesy - self.mainy +  373)
        if int(angle) == 133:
            mousepos = (enemy_posX - imagesx - self.mainx + 128, enemy_posY - imagesy - self.mainy +  374)
        if int(angle) == 134:
            mousepos = (enemy_posX - imagesx - self.mainx + 131, enemy_posY - imagesy - self.mainy +  377)
        if int(angle) == 135:
            mousepos = (enemy_posX - imagesx - self.mainx + 134, enemy_posY - imagesy - self.mainy +  381)
        if int(angle) == 136:
            mousepos = (enemy_posX - imagesx - self.mainx + 138, enemy_posY - imagesy - self.mainy +  386)
        if int(angle) == 137:
            mousepos = (enemy_posX - imagesx - self.mainx + 139, enemy_posY - imagesy - self.mainy +  387)
        if int(angle) == 138:
            mousepos = (enemy_posX - imagesx - self.mainx + 141, enemy_posY - imagesy - self.mainy +  391)
        if int(angle) == 115:
            mousepos = (enemy_posX - imagesx - self.mainx + 106, enemy_posY - imagesy - self.mainy +  304)
        if int(angle) == 139:
            mousepos = (enemy_posX - imagesx - self.mainx + 144, enemy_posY - imagesy - self.mainy +  390)
        if int(angle) == 140:
            mousepos = (enemy_posX - imagesx - self.mainx + 148, enemy_posY - imagesy - self.mainy +  394)
        if int(angle) == 141:
            mousepos = (enemy_posX - imagesx - self.mainx + 150, enemy_posY - imagesy - self.mainy +  396)
        if int(angle) == 142:
            mousepos = (enemy_posX - imagesx - self.mainx + 154, enemy_posY - imagesy - self.mainy +  398)
        if int(angle) == 143:
            mousepos = (enemy_posX - imagesx - self.mainx + 158, enemy_posY - imagesy - self.mainy +  398)
        if int(angle) == 144:
            mousepos = (enemy_posX - imagesx - self.mainx + 162, enemy_posY - imagesy - self.mainy +  400)
        if int(angle) == 145:
            mousepos = (enemy_posX - imagesx - self.mainx + 166, enemy_posY - imagesy - self.mainy +  402)
        if int(angle) == 146:
            mousepos = (enemy_posX - imagesx - self.mainx + 170, enemy_posY - imagesy - self.mainy +  402)
        if int(angle) == 147:
            mousepos = (enemy_posX - imagesx - self.mainx + 175, enemy_posY - imagesy - self.mainy +  407)
        if int(angle) == 148:
            mousepos = (enemy_posX - imagesx - self.mainx + 176, enemy_posY - imagesy - self.mainy +  411)
        if int(angle) == 149:
            mousepos = (enemy_posX - imagesx - self.mainx + 178, enemy_posY - imagesy - self.mainy +  412)
        if int(angle) == 150:
            mousepos = (enemy_posX - imagesx - self.mainx + 182, enemy_posY - imagesy - self.mainy +  415)
        if int(angle) == 151:
            mousepos = (enemy_posX - imagesx - self.mainx + 183, enemy_posY - imagesy - self.mainy +  419)
        if int(angle) == 152:
            mousepos = (enemy_posX - imagesx - self.mainx + 186, enemy_posY - imagesy - self.mainy +  420)
        if int(angle) == 153:
            mousepos = (enemy_posX - imagesx - self.mainx + 190, enemy_posY - imagesy - self.mainy +  424)
        if int(angle) == 154:
            mousepos = (enemy_posX - imagesx - self.mainx + 195, enemy_posY - imagesy - self.mainy +  425)
        if int(angle) == 155:
            mousepos = (enemy_posX - imagesx - self.mainx + 198, enemy_posY - imagesy - self.mainy +  426)
        if int(angle) == 156:
            mousepos = (enemy_posX - imagesx - self.mainx + 204, enemy_posY - imagesy - self.mainy +  426)
        if int(angle) == 157:
            mousepos = (enemy_posX - imagesx - self.mainx + 206, enemy_posY - imagesy - self.mainy +  426)
        if int(angle) == 158:
            mousepos = (enemy_posX - imagesx - self.mainx + 214, enemy_posY - imagesy - self.mainy +  426)
        if int(angle) == 159:
            mousepos = (enemy_posX - imagesx - self.mainx + 216, enemy_posY - imagesy - self.mainy +  426)
        if int(angle) == 160:
            mousepos = (enemy_posX - imagesx - self.mainx + 222, enemy_posY - imagesy - self.mainy +  426)
        if int(angle) == 161:
            mousepos = (enemy_posX - imagesx - self.mainx + 224, enemy_posY - imagesy - self.mainy +  427)
        if int(angle) == 162:
            mousepos = (enemy_posX - imagesx - self.mainx + 228, enemy_posY - imagesy - self.mainy +  428)
        if int(angle) == 163:
            mousepos = (enemy_posX - imagesx - self.mainx + 232, enemy_posY - imagesy - self.mainy +  430)
        if int(angle) == 164:
            mousepos = (enemy_posX - imagesx - self.mainx + 234, enemy_posY - imagesy - self.mainy +  430)
        if int(angle) == 165:
            mousepos = (enemy_posX - imagesx - self.mainx + 238, enemy_posY - imagesy - self.mainy +  430)
        if int(angle) == 166:
            mousepos = (enemy_posX - imagesx - self.mainx + 244, enemy_posY - imagesy - self.mainy +  430)
        if int(angle) == 167:
            mousepos = (enemy_posX - imagesx - self.mainx + 246, enemy_posY - imagesy - self.mainy +  430)
        if int(angle) == 168:
            mousepos = (enemy_posX - imagesx - self.mainx + 249, enemy_posY - imagesy - self.mainy +  433)
        if int(angle) == 169:
            mousepos = (enemy_posX - imagesx - self.mainx + 252, enemy_posY - imagesy - self.mainy +  444)
        if int(angle) == 170:
            mousepos = (enemy_posX - imagesx - self.mainx + 258, enemy_posY - imagesy - self.mainy +  444)
        if int(angle) == 175:
            mousepos = (enemy_posX - imagesx - self.mainx + 274, enemy_posY - imagesy - self.mainy +  456)
        if int(angle) == 293:
            mousepos = (enemy_posX - imagesx - self.mainx + 516, enemy_posY - imagesy - self.mainy +  120)
        if int(angle) == 290:
            mousepos = (enemy_posX - imagesx - self.mainx + 519, enemy_posY - imagesy - self.mainy +  137)
        if int(angle) == 319:
            mousepos = (enemy_posX - imagesx - self.mainx + 444, enemy_posY - imagesy - self.mainy +  45)
        
            
        mainy = mousepos[1] - blitY
        mainx = mousepos[0] - blitX
        
        
        enemy_shot_angley = -1 * ((enemy_posY - imagesy - mainy) / 10 + badaim)
        enemy_shot_anglex = -1 * ((enemy_posX - imagesx - mainx) / 10 + badaim)
    
        self.enemy_shotrun_list.append(enemy_shot_anglex + (enemy_posX - imagesx) + blitX)
        self.enemy_shotrise_list.append(enemy_shot_angley + (enemy_posY - imagesy) + blitY)
        self.enemy_backup_shotrun.append(enemy_shot_anglex)
        self.enemy_backup_shotrise.append(enemy_shot_angley) 
        
        pygame.mixer.Sound.play(self.gunshot)         

