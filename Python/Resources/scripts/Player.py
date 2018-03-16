import pygame, os, math, sys
from Resources.scripts.Maps import *
from Resources.scripts.Creator import *
from random import randint
import pickle

if __name__ == "__main__":
    sys.exit()
screen =  pygame.display.set_mode((640,480))
path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1]), 'images', '')
soundpath = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1]), 'sounds', '')
class Player(object):
    def __init__(self, custom_map=False):
        if custom_map != False:
            self.custom_map = Play_Maps(custom_map)
        else:
            self.custom_map = False
        self.mainx = 295
        self.mainy = 215
        self.imagesx = 0
        self.imagesy = 0
        self.angle = 0
        
        self.health = 100
        
        self.maincharacter = self.backup = pygame.image.load(path+'character.png')
        self.plane = pygame.image.load(path+'usplane.png')
        self.font = pygame.font.SysFont(None, 25)
        self.smallfont = pygame.font.SysFont(None, 20)
        
        self.angle_list = []
        self.pos_list = []
    
    def test(self, mousepos):
        """not called anymore, used to generate consistent shot speeds"""
        if not int(self.angle) in self.angle_list: 
            self.angle_list.append(int(self.angle))
            self.pos_list.append(mousepos)
        print(str(len(self.angle_list)))
        if len(self.angle_list) == 360:
            with open("test", "w+") as file:
                for angle, pos in zip(self.angle_list, self.pos_list):
                    file.write("        if int(angle) == "+str(angle)+":\n")
                    file.write("            mousepos = "+str(pos)+"\n")
            sys.exit()
    
    def test_2(self, mousepos):
        """not called anymore, used to generate consistent shot starting position"""
        if not int(self.angle) in self.angle_list: 
            self.angle_list.append(int(self.angle))
            self.pos_list.append(mousepos)
        print(str(len(self.angle_list)))
        if len(self.angle_list) == 360:
            with open("test", "w+") as file:
                for angle, pos in zip(self.angle_list, self.pos_list):
                    file.write("        if int(angle) == "+str(angle)+":\n")
                    file.write("            self.mainx, self.mainy = "+str(pos)+"\n")
            sys.exit()
    
    def proper_spawn(self, collision_list):
        main_collision = pygame.Rect((self.mainx, self.mainy), (self.backup.get_size()[0] * 2, self.backup.get_size()[1] * 2)) 
            
        for collisions in collision_list[:]:
            if main_collision.colliderect(collisions):
                return True
        return False

    def spawn(self, spawnarea_x, spawnarea_y, map_choice):
        self.imagesx = randint(spawnarea_x[0], spawnarea_x[1]) #- imagesx
        self.imagesy = randint(spawnarea_y[0], spawnarea_y[1]) #- imagesy
        
        if self.custom_map == False:
            collision_list = map_collisions_update(self.imagesx, self.imagesy, map_choice) 
        else:
            collision_list = self.custom_map.map_collisions_update(self.imagesx, self.imagesy)


        while True:
            if self.custom_map == False:
                collision_list = map_collisions_update(self.imagesx, self.imagesy, map_choice) 
            else:
                collision_list = self.custom_map.map_collisions_update(self.imagesx, self.imagesy)
            if self.proper_spawn(collision_list):
                self.imagesx = randint(spawnarea_x[0], spawnarea_x[1]) #(spawnarea)
                self.imagesy = randint(spawnarea_y[0], spawnarea_y[1]) #(spawnarea)
            else:
                break
    
    
    def update_rank(self, kills):
        path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', '')
        """with open(path+'data', 'r+') as file:
            name, rank = file.readlines()
        os.remove(path+'data')
        with open(path+'data', 'w+') as file:
            file.write(name+str(int(rank) + kills))"""
        
        with open(path+"userdata", "rb") as file:
            data = pickle.load(file)
            
        rank = data["rank"]
        
        data["rank"] = int(rank) + kills
        
        if int(int(rank) / 25 - int(rank) / 100) == 25: #if already equals 25, don't bother with the rest
            return
        with open(path+"userdata", "wb+") as file:
            if data["rank"] > 834:
                data["rank"] = 834
            pickle.dump(data, file, protocol=2)
         
        #this does absolutely nothing looking back at this project 1 month after I abandoned it. Why is this here?    
        self.rank = int((int(rank) + kills) / 25 - (int(rank) + kills) / 100)
        
    def ui(self, kills, deaths, weapon, mag, shot, reloading, max_kills):
        try:
            int(kills)
            kd_bg = pygame.Surface((100,30), pygame.SRCALPHA)
            kd_bg.fill((211,211,211,180))
            screen.blit(kd_bg, (540,0))
            pygame.draw.rect(screen, (0, 0, 0), (540, 0, 100, 30), 3)    
            text = self.font.render("K: " + str(kills) + " D: " + str(deaths),1,(0,0,0))
            screen.blit(text, (550, 5))
        except:
            pass
            
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
        
        if max_kills < 1000:
            playto_bg = pygame.Surface((200,30), pygame.SRCALPHA)
            playto_bg.fill((211,211,211,180))
            screen.blit(playto_bg, (0,450))
            pygame.draw.rect(screen, (0, 0, 0), (0, 450, 200, 30), 3)    
            text = self.font.render("PLAYING TO "+str(max_kills)+" K/Ds",1,(0,0,0))
            screen.blit(text, (5, 455))
        
    def red_screen(self):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        alpha = (100 - self.health) * 1.3
        overlay.fill((255,0,0, alpha))
        screen.blit(overlay, (0,0))
        
    def set_angle(self, mousepos, types=None):
    
        self.angle = 90 + 360 - (math.degrees(math.atan2(self.mainy - mousepos[1], self.mainx - mousepos[0])))

        if self.angle >= 360:
            self.angle -= 360
        elif self.angle <= 0:
            self.angle += 360
        if types == "plane":
            self.maincharacter = pygame.transform.rotate(self.plane, self.angle)
        else:
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

        if map_choice == "MIDWAY":
            self.moveX *= 1.3
            self.moveY *= 1.3

        self.imagesy += self.moveY
        self.imagesx += self.moveX 
        
        
        
        if map_choice == "MIDWAY" or map_choice == "D-DAY":
            if self.collision(map_collisions_update(self.imagesx, self.imagesy, map_choice)):
                self.imagesy -= self.moveY
                self.imagesx -= self.moveX 
                self.moveX = (mousepos[0] - self.mainx) / 100
                self.moveY = (mousepos[1] - self.mainy) / 100
                self.imagesy += self.moveY
                self.imagesx += self.moveX 
        
        
        
        if self.custom_map == False:
            self.fix_go_thru_corners(map_collisions_update(self.imagesx, self.imagesy, map_choice)) 
        else:
            self.fix_go_thru_corners(self.custom_map.map_collisions_update(self.imagesx, self.imagesy))              
        #updating our collision value after we modified imagesx and y
        
        if self.custom_map == False:
            collision = map_collisions_update(self.imagesx, self.imagesy, map_choice) 
        else:
            collision = self.custom_map.map_collisions_update(self.imagesx, self.imagesy)
                    
        if self.collision(collision):
            
            self.imagesy += self.moveY
            self.imagesx -= self.moveX 
            
            if self.custom_map == False:
                collision = map_collisions_update(self.imagesx, self.imagesy, map_choice)
            else:
                collision = self.custom_map.map_collisions_update(self.imagesx, self.imagesy)
                
            if self.collision(collision):
                self.imagesy -= self.moveY * 2
                self.imagesx += self.moveX * 2
                

class Gun(object):
    def __init__(self):
        self.gunshot = pygame.mixer.Sound(soundpath+"gunshot.wav")
        self.mainx = 295
        self.mainy = 215       
        self.shotrun_list = []
        self.shotrise_list = []
        self.backup_shotrise = []
        self.backup_shotrun = []
        self.bullet = pygame.image.load(path+'bullet.png')
        self.flame = pygame.image.load(path+'flame.png')     
       
    def blit_shot(self, flame=False):
        for rise, run, brise, brun in zip(self.shotrise_list, self.shotrun_list, self.backup_shotrise, self.backup_shotrun):
            self.shotrise_list.remove(rise)
            self.shotrun_list.remove(run)
            self.shotrise_list.append(rise + brise)
            self.shotrun_list.append(run + brun)
            if flame:
                screen.blit(self.flame, (run, rise))
            else:
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
    
    
    def shotgun_create_shot(self, recoil, angle):
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
            self.create_shot(recoil, pos)

                   
    def create_shot(self, recoil, angle):
        """makes gunshot speeds consistent"""
        if int(angle) == 0:
            mousepos = (170, 19)
        if int(angle) == 32:
            mousepos = (637, 60)
        if int(angle) == 294:
            mousepos = (637, 60)
        if int(angle) == 217:
            mousepos = (432, 479)
        if int(angle) == 207:
            mousepos = (425, 479)
        if int(angle) == 206:
            mousepos = (425, 479)
        if int(angle) == 205:
            mousepos = (422, 479)
        if int(angle) == 204:
            mousepos = (405, 479)
        if int(angle) == 202:
            mousepos = (399, 479)
        if int(angle) == 201:
            mousepos = (398, 479)
        if int(angle) == 200:
            mousepos = (396, 479)
        if int(angle) == 199:
            mousepos = (367, 479)
        if int(angle) == 195:
            mousepos = (360, 479)
        if int(angle) == 193:
            mousepos = (357, 479)
        if int(angle) == 192:
            mousepos = (355, 479)
        if int(angle) == 191:
            mousepos = (346, 479)
        if int(angle) == 190:
            mousepos = (346, 479)
        if int(angle) == 196:
            mousepos = (368, 467)
        if int(angle) == 197:
            mousepos = (374, 466)
        if int(angle) == 194:
            mousepos = (356, 466)
        if int(angle) == 189:
            mousepos = (336, 470)
        if int(angle) == 187:
            mousepos = (328, 472)
        if int(angle) == 185:
            mousepos = (320, 472)
        if int(angle) == 184:
            mousepos = (316, 472)
        if int(angle) == 183:
            mousepos = (312, 472)
        if int(angle) == 182:
            mousepos = (304, 472)
        if int(angle) == 181:
            mousepos = (298, 472)
        if int(angle) == 180:
            mousepos = (298, 472)
        if int(angle) == 179:
            mousepos = (288, 468)
        if int(angle) == 178:
            mousepos = (284, 466)
        if int(angle) == 177:
            mousepos = (280, 466)
        if int(angle) == 176:
            mousepos = (278, 466)
        if int(angle) == 174:
            mousepos = (266, 466)
        if int(angle) == 173:
            mousepos = (264, 468)
        if int(angle) == 172:
            mousepos = (258, 466)
        if int(angle) == 171:
            mousepos = (257, 466)
        if int(angle) == 186:
            mousepos = (324, 472)
        if int(angle) == 188:
            mousepos = (334, 470)
        if int(angle) == 198:
            mousepos = (378, 464)
        if int(angle) == 203:
            mousepos = (395, 447)
        if int(angle) == 208:
            mousepos = (418, 441)
        if int(angle) == 209:
            mousepos = (420, 440)
        if int(angle) == 210:
            mousepos = (427, 437)
        if int(angle) == 211:
            mousepos = (428, 434)
        if int(angle) == 212:
            mousepos = (434, 432)
        if int(angle) == 213:
            mousepos = (437, 433)
        if int(angle) == 214:
            mousepos = (440, 428)
        if int(angle) == 215:
            mousepos = (445, 427)
        if int(angle) == 216:
            mousepos = (450, 426)
        if int(angle) == 218:
            mousepos = (456, 418)
        if int(angle) == 219:
            mousepos = (460, 418)
        if int(angle) == 220:
            mousepos = (464, 414)
        if int(angle) == 221:
            mousepos = (468, 412)
        if int(angle) == 222:
            mousepos = (469, 407)
        if int(angle) == 223:
            mousepos = (469, 401)
        if int(angle) == 224:
            mousepos = (472, 398)
        if int(angle) == 225:
            mousepos = (476, 396)
        if int(angle) == 226:
            mousepos = (479, 391)
        if int(angle) == 227:
            mousepos = (484, 390)
        if int(angle) == 228:
            mousepos = (487, 387)
        if int(angle) == 229:
            mousepos = (493, 385)
        if int(angle) == 230:
            mousepos = (496, 381)
        if int(angle) == 231:
            mousepos = (498, 378)
        if int(angle) == 232:
            mousepos = (501, 375)
        if int(angle) == 233:
            mousepos = (506, 368)
        if int(angle) == 234:
            mousepos = (506, 366)
        if int(angle) == 235:
            mousepos = (512, 364)
        if int(angle) == 236:
            mousepos = (513, 359)
        if int(angle) == 237:
            mousepos = (514, 354)
        if int(angle) == 238:
            mousepos = (516, 350)
        if int(angle) == 239:
            mousepos = (519, 347)
        if int(angle) == 240:
            mousepos = (520, 340)
        if int(angle) == 241:
            mousepos = (523, 335)
        if int(angle) == 242:
            mousepos = (523, 335)
        if int(angle) == 243:
            mousepos = (526, 329)
        if int(angle) == 244:
            mousepos = (527, 327)
        if int(angle) == 245:
            mousepos = (530, 320)
        if int(angle) == 246:
            mousepos = (531, 319)
        if int(angle) == 247:
            mousepos = (534, 314)
        if int(angle) == 248:
            mousepos = (537, 311)
        if int(angle) == 249:
            mousepos = (540, 306)
        if int(angle) == 250:
            mousepos = (543, 303)
        if int(angle) == 251:
            mousepos = (543, 299)
        if int(angle) == 252:
            mousepos = (543, 295)
        if int(angle) == 253:
            mousepos = (545, 291)
        if int(angle) == 254:
            mousepos = (545, 285)
        if int(angle) == 255:
            mousepos = (545, 281)
        if int(angle) == 256:
            mousepos = (547, 277)
        if int(angle) == 257:
            mousepos = (547, 273)
        if int(angle) == 258:
            mousepos = (549, 267)
        if int(angle) == 259:
            mousepos = (549, 263)
        if int(angle) == 260:
            mousepos = (549, 253)
        if int(angle) == 261:
            mousepos = (549, 253)
        if int(angle) == 262:
            mousepos = (549, 249)
        if int(angle) == 263:
            mousepos = (549, 245)
        if int(angle) == 264:
            mousepos = (549, 241)
        if int(angle) == 265:
            mousepos = (549, 237)
        if int(angle) == 266:
            mousepos = (549, 231)
        if int(angle) == 267:
            mousepos = (549, 227)
        if int(angle) == 268:
            mousepos = (549, 223)
        if int(angle) == 269:
            mousepos = (549, 219)
        if int(angle) == 270:
            mousepos = (549, 215)
        if int(angle) == 271:
            mousepos = (549, 209)
        if int(angle) == 272:
            mousepos = (549, 205)
        if int(angle) == 273:
            mousepos = (549, 201)
        if int(angle) == 274:
            mousepos = (549, 197)
        if int(angle) == 275:
            mousepos = (549, 191)
        if int(angle) == 276:
            mousepos = (549, 187)
        if int(angle) == 277:
            mousepos = (550, 183)
        if int(angle) == 278:
            mousepos = (550, 178)
        if int(angle) == 279:
            mousepos = (549, 173)
        if int(angle) == 280:
            mousepos = (549, 169)
        if int(angle) == 281:
            mousepos = (548, 164)
        if int(angle) == 282:
            mousepos = (547, 161)
        if int(angle) == 283:
            mousepos = (545, 157)
        if int(angle) == 284:
            mousepos = (540, 147)
        if int(angle) == 285:
            mousepos = (539, 143)
        if int(angle) == 286:
            mousepos = (539, 143)
        if int(angle) == 287:
            mousepos = (538, 140)
        if int(angle) == 288:
            mousepos = (530, 138)
        if int(angle) == 289:
            mousepos = (525, 133)
        if int(angle) == 291:
            mousepos = (520, 128)
        if int(angle) == 292:
            mousepos = (517, 125)
        if int(angle) == 295:
            mousepos = (513, 111)
        if int(angle) == 296:
            mousepos = (510, 106)
        if int(angle) == 297:
            mousepos = (509, 105)
        if int(angle) == 298:
            mousepos = (507, 101)
        if int(angle) == 299:
            mousepos = (507, 97)
        if int(angle) == 300:
            mousepos = (501, 87)
        if int(angle) == 301:
            mousepos = (501, 87)
        if int(angle) == 302:
            mousepos = (498, 86)
        if int(angle) == 303:
            mousepos = (488, 82)
        if int(angle) == 304:
            mousepos = (488, 82)
        if int(angle) == 305:
            mousepos = (485, 81)
        if int(angle) == 306:
            mousepos = (485, 75)
        if int(angle) == 307:
            mousepos = (482, 70)
        if int(angle) == 308:
            mousepos = (481, 69)
        if int(angle) == 309:
            mousepos = (475, 61)
        if int(angle) == 310:
            mousepos = (474, 60)
        if int(angle) == 311:
            mousepos = (472, 60)
        if int(angle) == 313:
            mousepos = (454, 60)
        if int(angle) == 314:
            mousepos = (454, 60)
        if int(angle) == 315:
            mousepos = (448, 58)
        if int(angle) == 316:
            mousepos = (445, 55)
        if int(angle) == 317:
            mousepos = (444, 54)
        if int(angle) == 318:
            mousepos = (443, 47)
        if int(angle) == 312:
            mousepos = (466, 59)
        if int(angle) == 320:
            mousepos = (434, 47)
        if int(angle) == 321:
            mousepos = (432, 44)
        if int(angle) == 322:
            mousepos = (423, 37)
        if int(angle) == 324:
            mousepos = (423, 37)
        if int(angle) == 325:
            mousepos = (420, 34)
        if int(angle) == 326:
            mousepos = (410, 30)
        if int(angle) == 328:
            mousepos = (410, 30)
        if int(angle) == 329:
            mousepos = (408, 26)
        if int(angle) == 330:
            mousepos = (394, 26)
        if int(angle) == 332:
            mousepos = (390, 26)
        if int(angle) == 333:
            mousepos = (390, 26)
        if int(angle) == 327:
            mousepos = (418, 28)
        if int(angle) == 323:
            mousepos = (430, 33)
        if int(angle) == 331:
            mousepos = (395, 25)
        if int(angle) == 334:
            mousepos = (386, 22)
        if int(angle) == 335:
            mousepos = (384, 22)
        if int(angle) == 337:
            mousepos = (378, 18)
        if int(angle) == 338:
            mousepos = (374, 18)
        if int(angle) == 339:
            mousepos = (370, 16)
        if int(angle) == 340:
            mousepos = (366, 14)
        if int(angle) == 341:
            mousepos = (362, 14)
        if int(angle) == 336:
            mousepos = (382, 16)
        if int(angle) == 342:
            mousepos = (358, 14)
        if int(angle) == 343:
            mousepos = (354, 14)
        if int(angle) == 344:
            mousepos = (348, 14)
        if int(angle) == 345:
            mousepos = (348, 14)
        if int(angle) == 346:
            mousepos = (344, 14)
        if int(angle) == 347:
            mousepos = (340, 14)
        if int(angle) == 348:
            mousepos = (336, 14)
        if int(angle) == 349:
            mousepos = (334, 14)
        if int(angle) == 351:
            mousepos = (324, 10)
        if int(angle) == 352:
            mousepos = (322, 10)
        if int(angle) == 353:
            mousepos = (318, 10)
        if int(angle) == 350:
            mousepos = (330, 8)
        if int(angle) == 354:
            mousepos = (316, 8)
        if int(angle) == 355:
            mousepos = (312, 8)
        if int(angle) == 356:
            mousepos = (308, 8)
        if int(angle) == 357:
            mousepos = (305, 7)
        if int(angle) == 358:
            mousepos = (302, 6)
        if int(angle) == 359:
            mousepos = (298, 6)
        if int(angle) == 1:
            mousepos = (290, 8)
        if int(angle) == 2:
            mousepos = (284, 8)
        if int(angle) == 3:
            mousepos = (284, 8)
        if int(angle) == 4:
            mousepos = (280, 8)
        if int(angle) == 5:
            mousepos = (274, 8)
        if int(angle) == 6:
            mousepos = (273, 7)
        if int(angle) == 7:
            mousepos = (268, 10)
        if int(angle) == 8:
            mousepos = (264, 10)
        if int(angle) == 9:
            mousepos = (260, 10)
        if int(angle) == 10:
            mousepos = (256, 12)
        if int(angle) == 11:
            mousepos = (255, 13)
        if int(angle) == 12:
            mousepos = (252, 21)
        if int(angle) == 13:
            mousepos = (248, 22)
        if int(angle) == 14:
            mousepos = (244, 24)
        if int(angle) == 15:
            mousepos = (242, 24)
        if int(angle) == 16:
            mousepos = (240, 24)
        if int(angle) == 17:
            mousepos = (233, 29)
        if int(angle) == 18:
            mousepos = (233, 29)
        if int(angle) == 20:
            mousepos = (226, 34)
        if int(angle) == 19:
            mousepos = (234, 32)
        if int(angle) == 21:
            mousepos = (222, 28)
        if int(angle) == 22:
            mousepos = (218, 30)
        if int(angle) == 23:
            mousepos = (216, 32)
        if int(angle) == 24:
            mousepos = (212, 32)
        if int(angle) == 25:
            mousepos = (208, 34)
        if int(angle) == 26:
            mousepos = (206, 34)
        if int(angle) == 27:
            mousepos = (198, 38)
        if int(angle) == 28:
            mousepos = (198, 38)
        if int(angle) == 29:
            mousepos = (197, 39)
        if int(angle) == 30:
            mousepos = (192, 44)
        if int(angle) == 31:
            mousepos = (192, 44)
        if int(angle) == 33:
            mousepos = (174, 52)
        if int(angle) == 36:
            mousepos = (169, 57)
        if int(angle) == 38:
            mousepos = (169, 57)
        if int(angle) == 37:
            mousepos = (174, 54)
        if int(angle) == 35:
            mousepos = (179, 51)
        if int(angle) == 34:
            mousepos = (180, 50)
        if int(angle) == 39:
            mousepos = (169, 63)
        if int(angle) == 40:
            mousepos = (168, 64)
        if int(angle) == 41:
            mousepos = (165, 69)
        if int(angle) == 42:
            mousepos = (164, 70)
        if int(angle) == 43:
            mousepos = (161, 73)
        if int(angle) == 44:
            mousepos = (159, 75)
        if int(angle) == 45:
            mousepos = (158, 80)
        if int(angle) == 46:
            mousepos = (156, 82)
        if int(angle) == 47:
            mousepos = (152, 84)
        if int(angle) == 48:
            mousepos = (149, 87)
        if int(angle) == 49:
            mousepos = (148, 90)
        if int(angle) == 50:
            mousepos = (147, 91)
        if int(angle) == 51:
            mousepos = (143, 93)
        if int(angle) == 52:
            mousepos = (143, 99)
        if int(angle) == 53:
            mousepos = (141, 101)
        if int(angle) == 54:
            mousepos = (139, 103)
        if int(angle) == 55:
            mousepos = (136, 105)
        if int(angle) == 56:
            mousepos = (133, 107)
        if int(angle) == 57:
            mousepos = (133, 113)
        if int(angle) == 58:
            mousepos = (132, 116)
        if int(angle) == 59:
            mousepos = (130, 117)
        if int(angle) == 60:
            mousepos = (127, 119)
        if int(angle) == 61:
            mousepos = (127, 125)
        if int(angle) == 63:
            mousepos = (123, 129)
        if int(angle) == 62:
            mousepos = (125, 125)
        if int(angle) == 64:
            mousepos = (115, 129)
        if int(angle) == 66:
            mousepos = (115, 135)
        if int(angle) == 67:
            mousepos = (115, 139)
        if int(angle) == 68:
            mousepos = (115, 143)
        if int(angle) == 69:
            mousepos = (115, 147)
        if int(angle) == 65:
            mousepos = (120, 136)
        if int(angle) == 70:
            mousepos = (117, 151)
        if int(angle) == 71:
            mousepos = (116, 162)
        if int(angle) == 73:
            mousepos = (116, 162)
        if int(angle) == 74:
            mousepos = (115, 165)
        if int(angle) == 75:
            mousepos = (115, 171)
        if int(angle) == 76:
            mousepos = (115, 171)
        if int(angle) == 72:
            mousepos = (115, 159)
        if int(angle) == 77:
            mousepos = (104, 174)
        if int(angle) == 78:
            mousepos = (102, 176)
        if int(angle) == 79:
            mousepos = (100, 178)
        if int(angle) == 80:
            mousepos = (99, 181)
        if int(angle) == 81:
            mousepos = (99, 185)
        if int(angle) == 82:
            mousepos = (99, 189)
        if int(angle) == 83:
            mousepos = (97, 193)
        if int(angle) == 84:
            mousepos = (97, 195)
        if int(angle) == 85:
            mousepos = (97, 201)
        if int(angle) == 86:
            mousepos = (97, 203)
        if int(angle) == 87:
            mousepos = (97, 205)
        if int(angle) == 88:
            mousepos = (95, 213)
        if int(angle) == 89:
            mousepos = (95, 217)
        if int(angle) == 90:
            mousepos = (95, 221)
        if int(angle) == 91:
            mousepos = (95, 221)
        if int(angle) == 92:
            mousepos = (95, 223)
        if int(angle) == 93:
            mousepos = (95, 227)
        if int(angle) == 94:
            mousepos = (95, 229)
        if int(angle) == 95:
            mousepos = (95, 233)
        if int(angle) == 96:
            mousepos = (95, 239)
        if int(angle) == 97:
            mousepos = (95, 243)
        if int(angle) == 98:
            mousepos = (95, 245)
        if int(angle) == 99:
            mousepos = (95, 253)
        if int(angle) == 100:
            mousepos = (95, 253)
        if int(angle) == 101:
            mousepos = (95, 255)
        if int(angle) == 102:
            mousepos = (93, 261)
        if int(angle) == 103:
            mousepos = (93, 267)
        if int(angle) == 104:
            mousepos = (93, 267)
        if int(angle) == 105:
            mousepos = (93, 271)
        if int(angle) == 106:
            mousepos = (94, 274)
        if int(angle) == 107:
            mousepos = (95, 279)
        if int(angle) == 108:
            mousepos = (95, 282)
        if int(angle) == 109:
            mousepos = (95, 285)
        if int(angle) == 110:
            mousepos = (95, 291)
        if int(angle) == 111:
            mousepos = (95, 295)
        if int(angle) == 112:
            mousepos = (95, 299)
        if int(angle) == 113:
            mousepos = (95, 303)
        if int(angle) == 114:
            mousepos = (97, 307)
        if int(angle) == 116:
            mousepos = (101, 315)
        if int(angle) == 117:
            mousepos = (101, 317)
        if int(angle) == 118:
            mousepos = (103, 323)
        if int(angle) == 119:
            mousepos = (103, 323)
        if int(angle) == 120:
            mousepos = (105, 331)
        if int(angle) == 121:
            mousepos = (105, 333)
        if int(angle) == 122:
            mousepos = (105, 338)
        if int(angle) == 123:
            mousepos = (105, 341)
        if int(angle) == 124:
            mousepos = (107, 347)
        if int(angle) == 125:
            mousepos = (107, 347)
        if int(angle) == 126:
            mousepos = (108, 354)
        if int(angle) == 127:
            mousepos = (110, 356)
        if int(angle) == 128:
            mousepos = (113, 359)
        if int(angle) == 129:
            mousepos = (116, 363)
        if int(angle) == 130:
            mousepos = (119, 369)
        if int(angle) == 131:
            mousepos = (122, 372)
        if int(angle) == 132:
            mousepos = (125, 373)
        if int(angle) == 133:
            mousepos = (128, 374)
        if int(angle) == 134:
            mousepos = (131, 377)
        if int(angle) == 135:
            mousepos = (134, 381)
        if int(angle) == 136:
            mousepos = (138, 386)
        if int(angle) == 137:
            mousepos = (139, 387)
        if int(angle) == 138:
            mousepos = (141, 391)
        if int(angle) == 115:
            mousepos = (106, 304)
        if int(angle) == 139:
            mousepos = (144, 390)
        if int(angle) == 140:
            mousepos = (148, 394)
        if int(angle) == 141:
            mousepos = (150, 396)
        if int(angle) == 142:
            mousepos = (154, 398)
        if int(angle) == 143:
            mousepos = (158, 398)
        if int(angle) == 144:
            mousepos = (162, 400)
        if int(angle) == 145:
            mousepos = (166, 402)
        if int(angle) == 146:
            mousepos = (170, 402)
        if int(angle) == 147:
            mousepos = (175, 407)
        if int(angle) == 148:
            mousepos = (176, 411)
        if int(angle) == 149:
            mousepos = (178, 412)
        if int(angle) == 150:
            mousepos = (182, 415)
        if int(angle) == 151:
            mousepos = (183, 419)
        if int(angle) == 152:
            mousepos = (186, 420)
        if int(angle) == 153:
            mousepos = (190, 424)
        if int(angle) == 154:
            mousepos = (195, 425)
        if int(angle) == 155:
            mousepos = (198, 426)
        if int(angle) == 156:
            mousepos = (204, 426)
        if int(angle) == 157:
            mousepos = (206, 426)
        if int(angle) == 158:
            mousepos = (214, 426)
        if int(angle) == 159:
            mousepos = (216, 426)
        if int(angle) == 160:
            mousepos = (222, 426)
        if int(angle) == 161:
            mousepos = (224, 427)
        if int(angle) == 162:
            mousepos = (228, 428)
        if int(angle) == 163:
            mousepos = (232, 430)
        if int(angle) == 164:
            mousepos = (234, 430)
        if int(angle) == 165:
            mousepos = (238, 430)
        if int(angle) == 166:
            mousepos = (244, 430)
        if int(angle) == 167:
            mousepos = (246, 430)
        if int(angle) == 168:
            mousepos = (249, 433)
        if int(angle) == 169:
            mousepos = (252, 444)
        if int(angle) == 170:
            mousepos = (258, 444)
        if int(angle) == 175:
            mousepos = (274, 456)
        if int(angle) == 293:
            mousepos = (516, 120)
        if int(angle) == 290:
            mousepos = (519, 137)
        if int(angle) == 319:
            mousepos = (444, 45)
    
        sizeX, sizeY = Player().backup.get_size()
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
            
        mouseposX = mousepos[0] - blitX
        mouseposY = mousepos[1] - blitY
        
        self.shot_moveY = (mouseposY - self.mainy + recoil) / 10
        self.shot_moveX = (mouseposX - self.mainx + recoil) / 10
        
        self.shotrun_list.append(self.shot_moveX + self.mainx + blitX)
        self.shotrise_list.append(self.shot_moveY + self.mainy + blitY)
        self.backup_shotrun.append(self.shot_moveX)
        self.backup_shotrise.append(self.shot_moveY)
        
        pygame.mixer.Sound.play(self.gunshot)
        
        """if len(self.shotrun_list) > 40:
            self.shotrun_list = []
            self.shotrise_list = []
            self.backup_shotrun = []
            self.backup_shotrise = []"""
