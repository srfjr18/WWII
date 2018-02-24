import os, pygame, sys
from random import randint

path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', 'Creations', 'Maps', '')
gun_path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', 'Creations', 'Guns', '')

screen =  pygame.display.set_mode((640,480))

class Creator(object):
    def __init__(self):
        from Resources.scripts.Menus import Menu 
        self.menu = Menu([])
        self.character = pygame.image.load(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1]), 'images', '')+'character.png')
        self.slider_dict = {"damage": 0, "recoil": 0, "firerate": 0, "mag size": 0, "reload time": 0}
        
    def sliders(self, screen, x, y, name, max_num, textX=65):
        mousepos = pygame.mouse.get_pos()
        mouse_collision = pygame.Rect((mousepos[0], mousepos[1]), (1, 1))
    
        text = self.menu.font["small"].render(name,1,(255,255,255))
        screen.blit(text, (x + textX, y - 35))
    
        text = self.menu.font["small"].render("0",1,(255,255,255))
        screen.blit(text, (x - 20, y - 10))
        text = self.menu.font["small"].render(str(max_num),1,(255,255,255))
        screen.blit(text, (x + 10 + 200, y - 10))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 200, 1), 3)
        
        if pygame.mouse.get_pressed()[0]:
            if mouse_collision.colliderect(pygame.Rect((x, y - 10), (200, 20))):
                
                for i in range(0, max_num):

                    pos = 200 * (max_num * 0.01) * i
                    if mouse_collision.colliderect(pygame.Rect((x + pos, y - 20), (200 / max_num, 40))):
                        if self.points - (i - self.slider_dict[name]) >= 0:
                            self.slider_dict[name] = i
            elif mouse_collision.colliderect(pygame.Rect((x, y - 20), (220, 40))):
                if self.points - (max_num - self.slider_dict[name]) >= 0:
                    self.slider_dict[name] = max_num
        text = self.menu.font["small"].render(str(self.slider_dict[name]),1,(255,255,255))
        screen.blit(text, (x + 200 * 0.1 * self.slider_dict[name] - 5, y + 30))
        pygame.draw.rect(screen, (255, 255, 255), (x + 200 * 0.1 * self.slider_dict[name], y, 1, 30), 3)  
        
    def gun_builder(self):
        background = pygame.Surface(screen.get_size())
        background.fill((0,0,0))
        background = background.convert()
        
        pygame.time.delay(300)
        gun_name = self.menu.name(True, "GUN NAME:")
        
        semiauto = False
        fullauto = True
        shotgun = False
        hit = False
        while True:
            
            if semiauto:
                self.points = 30
            else:
                self.points = 25
            
            try:    
                for key, value in self.slider_dict.iteritems():
                    self.points -= value
            except: #python 3
                for key, value in self.slider_dict.items():
                    self.points -= value
                
            if self.points < 0:
                self.slider_dict = {"damage": 0, "recoil": 0, "firerate": 0, "mag size": 0, "reload time": 0}
        
            screen.blit(background, (0, 0))
            
            mousepos = pygame.mouse.get_pos()
            mouse_collision = pygame.Rect((mousepos[0], mousepos[1]), (1, 1))
            
            text = self.menu.font["medium"].render("WEAPON: "+gun_name,1,(255,255,255))
            screen.blit(text, (5, 5))
            
            text = self.menu.font["medium"].render("POINTS: "+str(self.points),1,(255,255,255))
            screen.blit(text, (400, 5))
            
            text = self.menu.font["smallish"].render("semi-auto",1,(255,255,255))
            screen.blit(text, (20, 70))
            
            text = self.menu.font["smallish"].render("full-auto",1,(255,255,255))
            screen.blit(text, (20, 90))
            
            text = self.menu.font["smallish"].render("shotgun?:",1,(255,255,255))
            screen.blit(text, (20, 110))
            
            
            #Done button
            pygame.draw.rect(screen, (255, 255, 255), (screen.get_size()[0] / 3, 400, screen.get_size()[0] / 3, 50), 2)
            text = self.menu.font["small"].render("DONE",1,(255,255,255))
            screen.blit(text, (screen.get_size()[0] / 3 + 25, 415))
            
            if semiauto:
                text = self.menu.font["smallish"].render("semi-auto",1,(255,165,0))
                screen.blit(text, (20, 70))
            else:
                text = self.menu.font["smallish"].render("full-auto",1,(255,165,0))
                screen.blit(text, (20, 90))
            
            if shotgun:
                text = self.menu.font["smallish"].render("Y",1,(255,255,255))
                screen.blit(text, (130, 110))
            else:
                text = self.menu.font["smallish"].render("N",1,(255,255,255))
                screen.blit(text, (130, 110))
            
            
            if mouse_collision.colliderect(pygame.Rect((20, 70), (120, 30))):
                text = self.menu.font["smallish"].render("semi-auto",1,(255,165,0))
                screen.blit(text, (20, 70))
            elif mouse_collision.colliderect(pygame.Rect((20, 90), (120, 30))):
                text = self.menu.font["smallish"].render("full-auto",1,(255,165,0))
                screen.blit(text, (20, 90))
            elif mouse_collision.colliderect(pygame.Rect((screen.get_size()[0] / 3, 400), (screen.get_size()[0] / 3, 50))):
                text = self.menu.font["small"].render("DONE",1,(255,165,0))
                screen.blit(text, (screen.get_size()[0] / 3 + 25, 415))
            elif mouse_collision.colliderect(pygame.Rect((110, 110), (60, 30))) and not hit:
                if not shotgun:
                    text = self.menu.font["smallish"].render("N",1,(0,0,0))
                    screen.blit(text, (130, 110))
                    text = self.menu.font["smallish"].render("Y",1,(255,165,0))
                    screen.blit(text, (130, 110))
                else:
                    text = self.menu.font["smallish"].render("Y",1,(0,0,0))
                    screen.blit(text, (130, 110))
                    text = self.menu.font["smallish"].render("N",1,(255,165,0))
                    screen.blit(text, (130, 110))
            
            #line under points and name
            pygame.draw.rect(screen, (255, 255, 255), (0, 60, 640, 1), 3)
            pygame.draw.rect(screen, (255, 255, 255), (0, 140, 150, 1), 3)
            pygame.draw.rect(screen, (255, 255, 255), (150, 60, 1, 80), 3)
            
            
            #sliders
            self.sliders(screen, 30, 200, "damage", 10)
            self.sliders(screen, 30, 300, "recoil", 10)
            self.sliders(screen, 350, 120, "firerate", 10, 50)
            self.sliders(screen, 350, 220, "mag size", 10, 50)
            self.sliders(screen, 350, 320, "reload time", 10, 25)
              
            
            if not pygame.mouse.get_pressed()[0] and not mouse_collision.colliderect(pygame.Rect((110, 110), (60, 30))):
                hit = False
                
            if pygame.mouse.get_pressed()[0]:
                if mouse_collision.colliderect(pygame.Rect((20, 70), (120, 30))):
                    semiauto = True
                    fullauto = False
                elif mouse_collision.colliderect(pygame.Rect((20, 90), (120, 30))):
                    semiauto = False
                    fullauto = True
                elif mouse_collision.colliderect(pygame.Rect((110, 110), (60, 30))) and not hit:
                    hit = True
                    if shotgun:
                        shotgun = False
                    else:
                        shotgun = True
                
                elif mouse_collision.colliderect(pygame.Rect((screen.get_size()[0] / 3, 400), (screen.get_size()[0] / 3, 50))):
                    self.map_builder(size=(50,50), build_gun=True, map_name=str(gun_name))
                    with open(gun_path+str(gun_name)+".py", 'w+') as gun:
                        gun.write("import pygame\n")
                        gun.write("from Resources.scripts.Menus import screen #so if display (full/windowed) stays the same\n")
                        if shotgun:
                            gun.write("shotgun=True\n")
                        else:
                            gun.write("shotgun=False\n")
                        gun.write("def gun():"+"\n")
                        if semiauto:
                            action = "semi-auto"
                        else:
                            action = "full-auto"
                              
                            
                        firerate = self.slider_dict["firerate"]
                        if firerate < 2:
                            firerate = 125 - (40 * firerate)
                        elif firerate < 5:
                            firerate = 125 - (firerate * 25)
                        elif firerate < 8:
                            firerate = 20 - (firerate * 2)
                        else:
                            firerate = 11 - firerate
                             
                        if firerate < 4 and not semiauto:
                            damage = str(50 - (self.slider_dict["damage"] * 2))
                        elif firerate < 12 and not semiauto:
                            damage = str(50 - (self.slider_dict["damage"] * 3))
                        elif firerate < 51 and not semiauto:
                            damage = str(50 - (self.slider_dict["damage"] * 4))
                        elif semiauto or firerate > 50:
                            damage = str(50 - int(self.slider_dict["damage"] * 4.9))
                        
                        if semiauto and int(damage) < 5:
                            firerate += 120
                               
                        mag = self.slider_dict["mag size"] * 5
                        if mag == 0:
                            mag = 1
                        mag = str(mag)
                        
                        if shotgun:
                            mag = self.slider_dict["mag size"]
                            if mag == 0:
                                mag = 1
                            mag = str(mag)
                           
                        reloadtime = str(300 - (20 * self.slider_dict["reload time"]))
                           
                        if firerate > 50:
                            recoil = 4 - self.slider_dict["recoil"]
                            if recoil < 0:
                                recoil = 0
                        elif semiauto:
                            recoil = 10 - self.slider_dict["recoil"]
                        elif firerate > 20:
                            recoil = 15 - self.slider_dict["recoil"]
                        else:
                            recoil = 20 - self.slider_dict["recoil"]
                        recoil = str(recoil)
                                
                                
                        firerate = str(firerate)
                                
                        gun.write('    return '+firerate+', "'+action+'", '+damage+', '+mag+', '+reloadtime+', '+recoil+'\n')
                        gun.write('def blit_gun(angle, mainx=295, mainy=215):\n')
                        gun.write('    bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)\n')
                        for i in self.rects:
                            gun.write('    pygame.draw.rect(bg, '+str(i[1])+', '+str(i[2])+')\n')
                        gun.write('    bg = pygame.transform.rotate(bg, angle)\n')
                        gun.write('    screen.blit(bg, (mainx - 25, mainy - 25))\n')
                        
                        gun.write("    return [")
                        for i in self.rects:
                            gun.write("(None, "+str(i[1])+", "+str(i[2])+"), ")
                            
                    with open(gun_path+str(gun_name)+".py", 'rb+') as gun:
                        gun.seek(-2, os.SEEK_END)
                        gun.truncate()
                    with open(gun_path+str(gun_name)+".py", 'a') as gun:
                        gun.write("]")
       
                    pygame.time.delay(300)    
                    while True:
                        screen.blit(background, (0, 0))
                        font = pygame.font.SysFont(None, 25)
                        text = font.render("GAME RESTART REQUIRED",1,(255,255,255))
                        screen.blit(text, (200, 200))
                        for event in pygame.event.get():  
                            if event.type == pygame.QUIT: 
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    sys.exit()
            
                        if pygame.mouse.get_pressed()[0]:
                            break        
                        if pygame.key.get_pressed()[pygame.K_RETURN]:
                            break
                        pygame.display.flip()
                        
                    pygame.display.set_mode((640,480))
                    try:
                        os.execv(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'game.py'), sys.argv)
                    except OSError: #using embedded python 3 windows version
                        sys.exit()
                
                    
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
            pygame.display.flip()
                    
            
    
    def map_builder(self, size=(640,480), build_gun=False, map_name=None):
        clock = pygame.time.Clock()
        if build_gun:
            FPS = 30
        else:
            FPS = 80

        collision_list = []

        red = list(range(0, 1000))
        green = list(range(0, 1000))
        blue = list(range(0, 1000))
        x = list(range(0, 1000))
        y = list(range(0, 1000))
        width = list(range(0, 1000))
        height = list(range(0, 1000))
        collision = list(range(0, 1000))
        for num in range(1, 1000):
            red[num] = 1
            green[num] = 1
            blue[num] = 1
            x[num] = 1
            y[num] = 1
            width[num] = 1
            height[num] = 1
            collision[num] = True 
    
        scrollscreenx, scrollscreeny = 0, 0


        number_of_images = 0

        font = pygame.font.SysFont(None, 25)
        
        pygame.time.delay(300)
        while True:
            tempbackground = pygame.Surface(screen.get_size())
            tempbackground.fill((0,0,0))
            tempbackground = tempbackground.convert()
            screen.blit(tempbackground, (0, 0))
            text = font.render("CONTROLS: R=INCREASE RED",1,(255,255,255))
            screen.blit(text, (100, 5))
            text = font.render("G=INCREASE GREEN",1,(255,255,255))
            screen.blit(text, (100, 50))
            text = font.render("B=INCREASE BLUE",1,(255,255,255))
            screen.blit(text, (100, 100))
            text = font.render("ARROW KEYS=CHANGE SELECTED OPTION",1,(255,255,255))
            screen.blit(text, (100, 150))
            text = font.render("RETURN=CREATE NEW BLOCK",1,(255,255,255))
            screen.blit(text, (100, 200))
            text = font.render("RIGHT SHIFT=FINISH",1,(255,255,255))
            screen.blit(text, (100, 250))
            text = font.render("LEFT SHIFT=EDIT PREVIOUS BLOCK",1,(255,255,255))
            screen.blit(text, (100, 300))
            text = font.render("BACKSPACE=DELETE CURRENT BLOCK",1,(255,255,255))
            screen.blit(text, (100, 350))
            pygame.display.flip()
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            
            if pygame.mouse.get_pressed()[0]:
                campaign = False
                break
            if pygame.mouse.get_pressed()[1]:
                campaign = True
                break
           
        pygame.time.delay(300)
        if not build_gun:
            map_name = self.menu.name(True, "MAP NAME:")
        
        bred = bgreen = bblue = 0
        
        pygame.time.delay(300)
        while True:
            if build_gun:
                bred = bgreen = bblue = 255
                tempbackground = pygame.Surface(size)
                tempbackground.fill((bred,bgreen,bblue))
                tempbackground = tempbackground.convert()
                screen.blit(tempbackground, (0, 0))
                break
            tempbackground = pygame.Surface(screen.get_size())
            tempbackground.fill((bred,bgreen,bblue))
            tempbackground = tempbackground.convert()
            screen.blit(tempbackground, (0, 0))
            text = font.render("BACKGROUND COLOR",1,(255,255,255))
            screen.blit(text, (200, 200))
            if pygame.key.get_pressed()[pygame.K_r]:
                bred += 1
                if bred > 255:
                    bred = 0
            if pygame.key.get_pressed()[pygame.K_g]:
                bgreen += 1
                if bgreen > 255:
                    bgreen = 0
            if pygame.key.get_pressed()[pygame.K_b]:
                bblue += 1
                if bblue > 255:
                    bblue = 0
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            
            if pygame.mouse.get_pressed()[0]:
                break        
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                break
            pygame.display.flip()
        
        
        
        
        background = pygame.Surface(screen.get_size())
        background.fill((100,100,100))
        background = background.convert()
        if not build_gun:
            background = tempbackground

        change = "pos"
        ai = []
        ai_blit = []
        texts = []  
        texts_blitx = []
        texts_blity = []  
        ai_enemy = []
        pressedone, pressedtwo = False, False
                   
        while True:
            milliseconds = clock.tick(FPS)
            screen.blit(background, (0, 0))
    
    
            mousepos = pygame.mouse.get_pos()
            mouse_collision = pygame.Rect((mousepos[0], mousepos[1]), (1, 1))
    
            
            
            
            
            
            
            
            
            
            
            
            
            """pygame.draw.rect(screen, (42, 43, 43), (-266 - scrollscreenx, -556 - scrollscreeny, 521, 656))
            pygame.draw.rect(screen, (0, 0, 0), (-266 - scrollscreenx, -556 - scrollscreeny, 521, 656), 3)
            pygame.draw.rect(screen, (42, 43, 43), (-224 - scrollscreenx, 100 - scrollscreeny, 420, 68))
            pygame.draw.rect(screen, (0, 0, 0), (-224 - scrollscreenx, 100 - scrollscreeny, 420, 68), 3)
            pygame.draw.rect(screen, (42, 43, 43), (-173 - scrollscreenx, 169 - scrollscreeny, 316, 57))
            pygame.draw.rect(screen, (0, 0, 0), (-173 - scrollscreenx, 169 - scrollscreeny, 316, 57), 3)
            pygame.draw.rect(screen, (42, 43, 43), (-225 - scrollscreenx, -622 - scrollscreeny, 423, 66))
            pygame.draw.rect(screen, (0, 0, 0), (-225 - scrollscreenx, -622 - scrollscreeny, 423, 66), 3)
            pygame.draw.rect(screen, (42, 43, 43), (-171 - scrollscreenx, -677 - scrollscreeny, 310, 57))
            pygame.draw.rect(screen, (0, 0, 0), (-171 - scrollscreenx, -677 - scrollscreeny, 310, 57), 3)
            pygame.draw.rect(screen, (5, 4, 6), (-193 - scrollscreenx, -501 - scrollscreeny, 362, 530))
            pygame.draw.rect(screen, (0, 0, 0), (-193 - scrollscreenx, -501 - scrollscreeny, 362, 530), 3)
            pygame.draw.rect(screen, (251, 241, 6), (-28 - scrollscreenx, -473 - scrollscreeny, 20, 49))
            pygame.draw.rect(screen, (0, 0, 0), (-28 - scrollscreenx, -473 - scrollscreeny, 20, 49), 3)
            pygame.draw.rect(screen, (251, 241, 6), (-28 - scrollscreenx, -372 - scrollscreeny, 20, 55))
            pygame.draw.rect(screen, (0, 0, 0), (-28 - scrollscreenx, -372 - scrollscreeny, 20, 55), 3)
            pygame.draw.rect(screen, (251, 241, 6), (-28 - scrollscreenx, -280 - scrollscreeny, 21, 64))
            pygame.draw.rect(screen, (0, 0, 0), (-28 - scrollscreenx, -280 - scrollscreeny, 21, 64), 3)
            pygame.draw.rect(screen, (251, 241, 6), (-28 - scrollscreenx, -163 - scrollscreeny, 22, 67))
            pygame.draw.rect(screen, (0, 0, 0), (-28 - scrollscreenx, -163 - scrollscreeny, 22, 67), 3)
            pygame.draw.rect(screen, (251, 241, 6), (-28 - scrollscreenx, -54 - scrollscreeny, 22, 52))
            pygame.draw.rect(screen, (0, 0, 0), (-28 - scrollscreenx, -54 - scrollscreeny, 22, 52), 3)
            pygame.draw.rect(screen, (35, 40, 6), (50 - scrollscreenx, -368 - scrollscreeny, 25, 64))
            pygame.draw.rect(screen, (0, 0, 0), (50 - scrollscreenx, -368 - scrollscreeny, 25, 64), 3)
            pygame.draw.rect(screen, (35, 40, 6), (24 - scrollscreenx, -349 - scrollscreeny, 79, 20))
            pygame.draw.rect(screen, (0, 0, 0), (24 - scrollscreenx, -349 - scrollscreeny, 79, 20), 3)
            pygame.draw.rect(screen, (35, 40, 6), (42 - scrollscreenx, -316 - scrollscreeny, 40, 18))
            pygame.draw.rect(screen, (0, 0, 0), (42 - scrollscreenx, -316 - scrollscreeny, 40, 18), 3)
            pygame.draw.rect(screen, (86, 91, 99), (506 - scrollscreenx, -710 - scrollscreeny, 185, 425))
            pygame.draw.rect(screen, (0, 0, 0), (506 - scrollscreenx, -710 - scrollscreeny, 185, 425), 3)
            pygame.draw.rect(screen, (86, 91, 99), (538 - scrollscreenx, -284 - scrollscreeny, 129, 34))
            pygame.draw.rect(screen, (0, 0, 0), (538 - scrollscreenx, -284 - scrollscreeny, 129, 34), 3)
            pygame.draw.rect(screen, (86, 91, 99), (559 - scrollscreenx, -251 - scrollscreeny, 85, 30))
            pygame.draw.rect(screen, (0, 0, 0), (559 - scrollscreenx, -251 - scrollscreeny, 85, 30), 3)
            pygame.draw.rect(screen, (86, 91, 99), (534 - scrollscreenx, -743 - scrollscreeny, 120, 35))
            pygame.draw.rect(screen, (0, 0, 0), (534 - scrollscreenx, -743 - scrollscreeny, 120, 35), 3)
            pygame.draw.rect(screen, (86, 91, 99), (561 - scrollscreenx, -771 - scrollscreeny, 64, 30))
            pygame.draw.rect(screen, (0, 0, 0), (561 - scrollscreenx, -771 - scrollscreeny, 64, 30), 3)
            pygame.draw.rect(screen, (45, 45, 44), (551 - scrollscreenx, -571 - scrollscreeny, 98, 147))
            pygame.draw.rect(screen, (0, 0, 0), (551 - scrollscreenx, -571 - scrollscreeny, 98, 147), 3)
            pygame.draw.rect(screen, (45, 45, 44), (575 - scrollscreenx, -334 - scrollscreeny, 43, 34))
            pygame.draw.rect(screen, (0, 0, 0), (575 - scrollscreenx, -334 - scrollscreeny, 43, 34), 3)
            pygame.draw.rect(screen, (45, 45, 44), (609 - scrollscreenx, -323 - scrollscreeny, 50, 14))
            pygame.draw.rect(screen, (0, 0, 0), (609 - scrollscreenx, -323 - scrollscreeny, 50, 14), 3)
            pygame.draw.rect(screen, (214, 213, 211), (573 - scrollscreenx, -660 - scrollscreeny, 44, 45))
            pygame.draw.rect(screen, (0, 0, 0), (573 - scrollscreenx, -660 - scrollscreeny, 44, 45), 3)
            pygame.draw.rect(screen, (214, 20, 10), (583 - scrollscreenx, -651 - scrollscreeny, 23, 24))
            pygame.draw.rect(screen, (0, 0, 0), (583 - scrollscreenx, -651 - scrollscreeny, 23, 24), 3)
            pygame.draw.rect(screen, (177, 176, 174), (205 - scrollscreenx, -1391 - scrollscreeny, 226, 464))
            pygame.draw.rect(screen, (0, 0, 0), (205 - scrollscreenx, -1391 - scrollscreeny, 226, 464), 3)
            pygame.draw.rect(screen, (177, 176, 174), (226 - scrollscreenx, -1431 - scrollscreeny, 173, 42))
            pygame.draw.rect(screen, (0, 0, 0), (226 - scrollscreenx, -1431 - scrollscreeny, 173, 42), 3)
            pygame.draw.rect(screen, (177, 176, 174), (269 - scrollscreenx, -1463 - scrollscreeny, 86, 32))
            pygame.draw.rect(screen, (0, 0, 0), (269 - scrollscreenx, -1463 - scrollscreeny, 86, 32), 3)
            pygame.draw.rect(screen, (177, 176, 174), (240 - scrollscreenx, -930 - scrollscreeny, 149, 38))
            pygame.draw.rect(screen, (0, 0, 0), (240 - scrollscreenx, -930 - scrollscreeny, 149, 38), 3)
            pygame.draw.rect(screen, (177, 176, 174), (266 - scrollscreenx, -893 - scrollscreeny, 97, 27))
            pygame.draw.rect(screen, (0, 0, 0), (266 - scrollscreenx, -893 - scrollscreeny, 97, 27), 3)
            pygame.draw.rect(screen, (78, 70, 74), (222 - scrollscreenx, -1366 - scrollscreeny, 188, 154))
            pygame.draw.rect(screen, (0, 0, 0), (222 - scrollscreenx, -1366 - scrollscreeny, 188, 154), 3)
            pygame.draw.rect(screen, (78, 70, 74), (229 - scrollscreenx, -1093 - scrollscreeny, 181, 146))
            pygame.draw.rect(screen, (0, 0, 0), (229 - scrollscreenx, -1093 - scrollscreeny, 181, 146), 3)
            pygame.draw.rect(screen, (124, 107, 114), (686 - scrollscreenx, -1292 - scrollscreeny, 108, 206))
            pygame.draw.rect(screen, (0, 0, 0), (686 - scrollscreenx, -1292 - scrollscreeny, 108, 206), 3)
            pygame.draw.rect(screen, (124, 107, 114), (867 - scrollscreenx, -1294 - scrollscreeny, 97, 209))
            pygame.draw.rect(screen, (0, 0, 0), (867 - scrollscreenx, -1294 - scrollscreeny, 97, 209), 3)
            pygame.draw.rect(screen, (160, 144, 149), (1001 - scrollscreenx, -785 - scrollscreeny, 488, 327))
            pygame.draw.rect(screen, (0, 0, 0), (1001 - scrollscreenx, -785 - scrollscreeny, 488, 327), 3)
            pygame.draw.rect(screen, (160, 144, 149), (253 - scrollscreenx, -233 - scrollscreeny, 3, 335))
            pygame.draw.rect(screen, (0, 0, 0), (253 - scrollscreenx, -233 - scrollscreeny, 3, 335), 3)
            pygame.draw.rect(screen, (160, 144, 149), (-266 - scrollscreenx, 98 - scrollscreeny, 520, 1))
            pygame.draw.rect(screen, (0, 0, 0), (-266 - scrollscreenx, 98 - scrollscreeny, 520, 1), 3)
            pygame.draw.rect(screen, (13, 2, 9), (1185 - scrollscreenx, -653 - scrollscreeny, 115, 80))
            pygame.draw.rect(screen, (0, 0, 0), (1185 - scrollscreenx, -653 - scrollscreeny, 115, 80), 3)
            pygame.draw.rect(screen, (13, 2, 9), (1198 - scrollscreenx, -583 - scrollscreeny, 18, 63))
            pygame.draw.rect(screen, (0, 0, 0), (1198 - scrollscreenx, -583 - scrollscreeny, 18, 63), 3)
            pygame.draw.rect(screen, (13, 2, 9), (1262 - scrollscreenx, -595 - scrollscreeny, 18, 74))
            pygame.draw.rect(screen, (0, 0, 0), (1262 - scrollscreenx, -595 - scrollscreeny, 18, 74), 3)
            pygame.draw.rect(screen, (239, 222, 228), (1340 - scrollscreenx, -727 - scrollscreeny, 69, 66))
            pygame.draw.rect(screen, (0, 0, 0), (1340 - scrollscreenx, -727 - scrollscreeny, 69, 66), 3)
            pygame.draw.rect(screen, (239, 20, 24), (1360 - scrollscreenx, -712 - scrollscreeny, 31, 32))
            pygame.draw.rect(screen, (0, 0, 0), (1360 - scrollscreenx, -712 - scrollscreeny, 31, 32), 3)
            pygame.draw.rect(screen, (19, 20, 24), (1208 - scrollscreenx, -1285 - scrollscreeny, 641, 381))
            pygame.draw.rect(screen, (0, 0, 0), (1208 - scrollscreenx, -1285 - scrollscreeny, 641, 381), 3)
            pygame.draw.rect(screen, (19, 20, 24), (1139 - scrollscreenx, -1237 - scrollscreeny, 70, 277))
            pygame.draw.rect(screen, (0, 0, 0), (1139 - scrollscreenx, -1237 - scrollscreeny, 70, 277), 3)
            pygame.draw.rect(screen, (19, 20, 24), (1076 - scrollscreenx, -1195 - scrollscreeny, 65, 197))
            pygame.draw.rect(screen, (0, 0, 0), (1076 - scrollscreenx, -1195 - scrollscreeny, 65, 197), 3)
            pygame.draw.rect(screen, (19, 20, 24), (1849 - scrollscreenx, -1253 - scrollscreeny, 71, 309))
            pygame.draw.rect(screen, (0, 0, 0), (1849 - scrollscreenx, -1253 - scrollscreeny, 71, 309), 3)
            pygame.draw.rect(screen, (19, 20, 24), (1920 - scrollscreenx, -1211 - scrollscreeny, 52, 229))
            pygame.draw.rect(screen, (0, 0, 0), (1920 - scrollscreenx, -1211 - scrollscreeny, 52, 229), 3)
            pygame.draw.rect(screen, (1, 10, 11), (1264 - scrollscreenx, -1175 - scrollscreeny, 493, 155))
            pygame.draw.rect(screen, (0, 0, 0), (1264 - scrollscreenx, -1175 - scrollscreeny, 493, 155), 3)
            pygame.draw.rect(screen, (164, 174, 11), (1277 - scrollscreenx, -1104 - scrollscreeny, 50, 14))
            pygame.draw.rect(screen, (0, 0, 0), (1277 - scrollscreenx, -1104 - scrollscreeny, 50, 14), 3)
            pygame.draw.rect(screen, (164, 174, 11), (1385 - scrollscreenx, -1103 - scrollscreeny, 52, 15))
            pygame.draw.rect(screen, (0, 0, 0), (1385 - scrollscreenx, -1103 - scrollscreeny, 52, 15), 3)
            pygame.draw.rect(screen, (164, 174, 11), (1505 - scrollscreenx, -1102 - scrollscreeny, 60, 16))
            pygame.draw.rect(screen, (0, 0, 0), (1505 - scrollscreenx, -1102 - scrollscreeny, 60, 16), 3)
            pygame.draw.rect(screen, (164, 174, 11), (1646 - scrollscreenx, -1102 - scrollscreeny, 60, 16))
            pygame.draw.rect(screen, (0, 0, 0), (1646 - scrollscreenx, -1102 - scrollscreeny, 60, 16), 3)
            pygame.draw.rect(screen, (157, 18, 11), (1306 - scrollscreenx, -1256 - scrollscreeny, 43, 63))
            pygame.draw.rect(screen, (0, 0, 0), (1306 - scrollscreenx, -1256 - scrollscreeny, 43, 63), 3)
            pygame.draw.rect(screen, (157, 18, 11), (1387 - scrollscreenx, -1250 - scrollscreeny, 66, 26))
            pygame.draw.rect(screen, (0, 0, 0), (1387 - scrollscreenx, -1250 - scrollscreeny, 66, 26), 3)
            pygame.draw.rect(screen, (157, 18, 11), (1383 - scrollscreenx, -1192 - scrollscreeny, 45, 57))
            pygame.draw.rect(screen, (0, 0, 0), (1383 - scrollscreenx, -1192 - scrollscreeny, 45, 57), 3)
            pygame.draw.rect(screen, (185, 97, 11), (1326 - scrollscreenx, -1232 - scrollscreeny, 35, 44))
            pygame.draw.rect(screen, (0, 0, 0), (1326 - scrollscreenx, -1232 - scrollscreeny, 35, 44), 3)
            pygame.draw.rect(screen, (185, 97, 11), (1402 - scrollscreenx, -1230 - scrollscreeny, 38, 50))
            pygame.draw.rect(screen, (0, 0, 0), (1402 - scrollscreenx, -1230 - scrollscreeny, 38, 50), 3)
            pygame.draw.rect(screen, (185, 97, 11), (1348 - scrollscreenx, -1181 - scrollscreeny, 48, 39))
            pygame.draw.rect(screen, (0, 0, 0), (1348 - scrollscreenx, -1181 - scrollscreeny, 48, 39), 3)
            pygame.draw.rect(screen, (231, 197, 11), (1357 - scrollscreenx, -1247 - scrollscreeny, 50, 33))
            pygame.draw.rect(screen, (0, 0, 0), (1357 - scrollscreenx, -1247 - scrollscreeny, 50, 33), 3)
            pygame.draw.rect(screen, (231, 197, 11), (1356 - scrollscreenx, -1230 - scrollscreeny, 25, 64))
            pygame.draw.rect(screen, (0, 0, 0), (1356 - scrollscreenx, -1230 - scrollscreeny, 25, 64), 3)
            pygame.draw.rect(screen, (156, 21, 11), (1379 - scrollscreenx, -1217 - scrollscreeny, 40, 44))
            pygame.draw.rect(screen, (0, 0, 0), (1379 - scrollscreenx, -1217 - scrollscreeny, 40, 44), 3)
            pygame.draw.rect(screen, (48, 58, 53), (1512 - scrollscreenx, -2018 - scrollscreeny, 333, 549))
            pygame.draw.rect(screen, (0, 0, 0), (1512 - scrollscreenx, -2018 - scrollscreeny, 333, 549), 3)
            pygame.draw.rect(screen, (48, 58, 53), (1564 - scrollscreenx, -1472 - scrollscreeny, 230, 72))
            pygame.draw.rect(screen, (0, 0, 0), (1564 - scrollscreenx, -1472 - scrollscreeny, 230, 72), 3)
            pygame.draw.rect(screen, (48, 58, 53), (1562 - scrollscreenx, -2082 - scrollscreeny, 219, 65))
            pygame.draw.rect(screen, (0, 0, 0), (1562 - scrollscreenx, -2082 - scrollscreeny, 219, 65), 3)
            pygame.draw.rect(screen, (177, 188, 181), (1552 - scrollscreenx, -1990 - scrollscreeny, 257, 476))
            pygame.draw.rect(screen, (0, 0, 0), (1552 - scrollscreenx, -1990 - scrollscreeny, 257, 476), 3)
            pygame.draw.rect(screen, (100, 28, 5), (1962 - scrollscreenx, -2129 - scrollscreeny, 41, 50))
            pygame.draw.rect(screen, (0, 0, 0), (1962 - scrollscreenx, -2129 - scrollscreeny, 41, 50), 3)
            pygame.draw.rect(screen, (100, 28, 5), (2124 - scrollscreenx, -2051 - scrollscreeny, 32, 38))
            pygame.draw.rect(screen, (0, 0, 0), (2124 - scrollscreenx, -2051 - scrollscreeny, 32, 38), 3)
            pygame.draw.rect(screen, (100, 28, 5), (2194 - scrollscreenx, -2343 - scrollscreeny, 29, 39))
            pygame.draw.rect(screen, (0, 0, 0), (2194 - scrollscreenx, -2343 - scrollscreeny, 29, 39), 3)
            pygame.draw.rect(screen, (100, 28, 5), (2435 - scrollscreenx, -2133 - scrollscreeny, 34, 35))
            pygame.draw.rect(screen, (0, 0, 0), (2435 - scrollscreenx, -2133 - scrollscreeny, 34, 35), 3)
            pygame.draw.rect(screen, (100, 28, 5), (2512 - scrollscreenx, -2344 - scrollscreeny, 33, 35))
            pygame.draw.rect(screen, (0, 0, 0), (2512 - scrollscreenx, -2344 - scrollscreeny, 33, 35), 3)
            pygame.draw.rect(screen, (100, 28, 5), (2696 - scrollscreenx, -2192 - scrollscreeny, 36, 33))
            pygame.draw.rect(screen, (0, 0, 0), (2696 - scrollscreenx, -2192 - scrollscreeny, 36, 33), 3)
            pygame.draw.rect(screen, (100, 28, 5), (2844 - scrollscreenx, -2318 - scrollscreeny, 32, 28))
            pygame.draw.rect(screen, (0, 0, 0), (2844 - scrollscreenx, -2318 - scrollscreeny, 32, 28), 3)
            pygame.draw.rect(screen, (100, 28, 5), (3036 - scrollscreenx, -2213 - scrollscreeny, 34, 33))
            pygame.draw.rect(screen, (0, 0, 0), (3036 - scrollscreenx, -2213 - scrollscreeny, 34, 33), 3)
            pygame.draw.rect(screen, (157, 155, 150), (3257 - scrollscreenx, -2286 - scrollscreeny, 481, 220))
            pygame.draw.rect(screen, (0, 0, 0), (3257 - scrollscreenx, -2286 - scrollscreeny, 481, 220), 3)
            pygame.draw.rect(screen, (157, 155, 150), (3150 - scrollscreenx, -2239 - scrollscreeny, 107, 112))
            pygame.draw.rect(screen, (0, 0, 0), (3150 - scrollscreenx, -2239 - scrollscreeny, 107, 112), 3)
            pygame.draw.rect(screen, (157, 155, 150), (3738 - scrollscreenx, -2244 - scrollscreeny, 86, 132))
            pygame.draw.rect(screen, (0, 0, 0), (3738 - scrollscreenx, -2244 - scrollscreeny, 86, 132), 3)
            pygame.draw.rect(screen, (50, 49, 46), (3380 - scrollscreenx, -2233 - scrollscreeny, 241, 107))
            pygame.draw.rect(screen, (0, 0, 0), (3380 - scrollscreenx, -2233 - scrollscreeny, 241, 107), 3)
            pygame.draw.rect(screen, (50, 49, 46), (4013 - scrollscreenx, -2312 - scrollscreeny, 371, 501))
            pygame.draw.rect(screen, (0, 0, 0), (4013 - scrollscreenx, -2312 - scrollscreeny, 371, 501), 3)
            pygame.draw.rect(screen, (50, 49, 46), (4068 - scrollscreenx, -2392 - scrollscreeny, 248, 80))
            pygame.draw.rect(screen, (0, 0, 0), (4068 - scrollscreenx, -2392 - scrollscreeny, 248, 80), 3)
            pygame.draw.rect(screen, (50, 49, 46), (4100 - scrollscreenx, -2436 - scrollscreeny, 178, 43))
            pygame.draw.rect(screen, (0, 0, 0), (4100 - scrollscreenx, -2436 - scrollscreeny, 178, 43), 3)
            pygame.draw.rect(screen, (50, 49, 46), (4061 - scrollscreenx, -1809 - scrollscreeny, 276, 77))
            pygame.draw.rect(screen, (0, 0, 0), (4061 - scrollscreenx, -1809 - scrollscreeny, 276, 77), 3)
            pygame.draw.rect(screen, (50, 49, 46), (4113 - scrollscreenx, -1730 - scrollscreeny, 174, 54))
            pygame.draw.rect(screen, (0, 0, 0), (4113 - scrollscreenx, -1730 - scrollscreeny, 174, 54), 3)
            pygame.draw.rect(screen, (128, 128, 123), (4067 - scrollscreenx, -2268 - scrollscreeny, 265, 413))
            pygame.draw.rect(screen, (0, 0, 0), (4067 - scrollscreenx, -2268 - scrollscreeny, 265, 413), 3)
            pygame.draw.rect(screen, (128, 128, 123), (4842 - scrollscreenx, -2133 - scrollscreeny, 604, 322))
            pygame.draw.rect(screen, (0, 0, 0), (4842 - scrollscreenx, -2133 - scrollscreeny, 604, 322), 3)
            pygame.draw.rect(screen, (18, 16, 19), (4925 - scrollscreenx, -1916 - scrollscreeny, 80, 68))
            pygame.draw.rect(screen, (0, 0, 0), (4925 - scrollscreenx, -1916 - scrollscreeny, 80, 68), 3)
            pygame.draw.rect(screen, (18, 16, 19), (4924 - scrollscreenx, -2096 - scrollscreeny, 84, 75))
            pygame.draw.rect(screen, (0, 0, 0), (4924 - scrollscreenx, -2096 - scrollscreeny, 84, 75), 3)
            pygame.draw.rect(screen, (18, 16, 19), (5256 - scrollscreenx, -2094 - scrollscreeny, 92, 79))
            pygame.draw.rect(screen, (0, 0, 0), (5256 - scrollscreenx, -2094 - scrollscreeny, 92, 79), 3)
            pygame.draw.rect(screen, (18, 16, 19), (5260 - scrollscreenx, -1935 - scrollscreeny, 91, 82))
            pygame.draw.rect(screen, (0, 0, 0), (5260 - scrollscreenx, -1935 - scrollscreeny, 91, 82), 3)
            pygame.draw.rect(screen, (15, 94, 212), (-999 - scrollscreenx, -1607 - scrollscreeny, 442, 2429))
            pygame.draw.rect(screen, (0, 0, 0), (-999 - scrollscreenx, -1607 - scrollscreeny, 442, 2429), 3)
            pygame.draw.rect(screen, (15, 94, 212), (-558 - scrollscreenx, 316 - scrollscreeny, 1553, 467))
            pygame.draw.rect(screen, (0, 0, 0), (-558 - scrollscreenx, 316 - scrollscreeny, 1553, 467), 3)
            pygame.draw.rect(screen, (15, 94, 212), (994 - scrollscreenx, -76 - scrollscreeny, 1118, 1044))
            pygame.draw.rect(screen, (0, 0, 0), (994 - scrollscreenx, -76 - scrollscreeny, 1118, 1044), 3)
            pygame.draw.rect(screen, (15, 94, 212), (2109 - scrollscreenx, -1536 - scrollscreeny, 4290, 1650))
            pygame.draw.rect(screen, (0, 0, 0), (2109 - scrollscreenx, -1536 - scrollscreeny, 4290, 1650), 3)
            pygame.draw.rect(screen, (173, 252, 163), (5633 - scrollscreenx, -2556 - scrollscreeny, 868, 742))
            pygame.draw.rect(screen, (0, 0, 0), (5633 - scrollscreenx, -2556 - scrollscreeny, 868, 742), 3)
            pygame.draw.rect(screen, (24, 252, 15), (5725 - scrollscreenx, -2459 - scrollscreeny, 643, 533))
            pygame.draw.rect(screen, (0, 0, 0), (5725 - scrollscreenx, -2459 - scrollscreeny, 643, 533), 3)
            pygame.draw.rect(screen, (24, 16, 15), (6000 - scrollscreenx, -2246 - scrollscreeny, 137, 139))
            pygame.draw.rect(screen, (0, 0, 0), (6000 - scrollscreenx, -2246 - scrollscreeny, 137, 139), 3)
            pygame.draw.rect(screen, (24, 16, 15), (5977 - scrollscreenx, -2014 - scrollscreeny, 1, 1))
            pygame.draw.rect(screen, (0, 0, 0), (5977 - scrollscreenx, -2014 - scrollscreeny, 1, 1), 3)
            pygame.draw.rect(screen, (1, 93, 247), (6391 - scrollscreenx, -1537 - scrollscreeny, 870, 421))
            pygame.draw.rect(screen, (0, 0, 0), (6391 - scrollscreenx, -1537 - scrollscreeny, 870, 421), 3)
            pygame.draw.rect(screen, (1, 93, 247), (6767 - scrollscreenx, -2124 - scrollscreeny, 461, 582))
            pygame.draw.rect(screen, (0, 0, 0), (6767 - scrollscreenx, -2124 - scrollscreeny, 461, 582), 3)
            pygame.draw.rect(screen, (1, 93, 247), (6767 - scrollscreenx, -2777 - scrollscreeny, 529, 342))
            pygame.draw.rect(screen, (0, 0, 0), (6767 - scrollscreenx, -2777 - scrollscreeny, 529, 342), 3)
            pygame.draw.rect(screen, (1, 93, 247), (1342 - scrollscreenx, -3176 - scrollscreeny, 5687, 400))
            pygame.draw.rect(screen, (0, 0, 0), (1342 - scrollscreenx, -3176 - scrollscreeny, 5687, 400), 3)
            pygame.draw.rect(screen, (1, 93, 247), (1094 - scrollscreenx, -3120 - scrollscreeny, 265, 1641))
            pygame.draw.rect(screen, (0, 0, 0), (1094 - scrollscreenx, -3120 - scrollscreeny, 265, 1641), 3)
            pygame.draw.rect(screen, (1, 93, 247), (-557 - scrollscreenx, -1781 - scrollscreeny, 1720, 302))
            pygame.draw.rect(screen, (0, 0, 0), (-557 - scrollscreenx, -1781 - scrollscreeny, 1720, 302), 3)
            pygame.draw.rect(screen, (202, 207, 200), (-329 - scrollscreenx, -1201 - scrollscreeny, 447, 262))
            pygame.draw.rect(screen, (0, 0, 0), (-329 - scrollscreenx, -1201 - scrollscreeny, 447, 262), 3)
            pygame.draw.rect(screen, (25, 26, 18), (-144 - scrollscreenx, -1109 - scrollscreeny, 81, 69))
            pygame.draw.rect(screen, (0, 0, 0), (-144 - scrollscreenx, -1109 - scrollscreeny, 81, 69), 3)
            pygame.draw.rect(screen, (87, 26, 18), (570 - scrollscreenx, -24 - scrollscreeny, 113, 92))
            pygame.draw.rect(screen, (0, 0, 0), (570 - scrollscreenx, -24 - scrollscreeny, 113, 92), 3)
            pygame.draw.rect(screen, (87, 26, 18), (1042 - scrollscreenx, -286 - scrollscreeny, 86, 68))
            pygame.draw.rect(screen, (0, 0, 0), (1042 - scrollscreenx, -286 - scrollscreeny, 86, 68), 3)
            pygame.draw.rect(screen, (87, 26, 18), (1805 - scrollscreenx, -494 - scrollscreeny, 40, 36))
            pygame.draw.rect(screen, (0, 0, 0), (1805 - scrollscreenx, -494 - scrollscreeny, 40, 36), 3)
            pygame.draw.rect(screen, (87, 26, 18), (1835 - scrollscreenx, -762 - scrollscreeny, 66, 33))
            pygame.draw.rect(screen, (0, 0, 0), (1835 - scrollscreenx, -762 - scrollscreeny, 66, 33), 3)
            pygame.draw.rect(screen, (202, 192, 190), (2219 - scrollscreenx, -1898 - scrollscreeny, 758, 190))
            pygame.draw.rect(screen, (0, 0, 0), (2219 - scrollscreenx, -1898 - scrollscreeny, 758, 190), 3)
            pygame.draw.rect(screen, (52, 25, 5), (3541 - scrollscreenx, -1824 - scrollscreeny, 141, 61))
            pygame.draw.rect(screen, (0, 0, 0), (3541 - scrollscreenx, -1824 - scrollscreeny, 141, 61), 3)
            pygame.draw.rect(screen, (170, 211, 206), (2788 - scrollscreenx, -2663 - scrollscreeny, 708, 184))
            pygame.draw.rect(screen, (0, 0, 0), (2788 - scrollscreenx, -2663 - scrollscreeny, 708, 184), 3)
            pygame.draw.rect(screen, (20, 24, 20), (3127 - scrollscreenx, -2590 - scrollscreeny, 50, 58))
            pygame.draw.rect(screen, (0, 0, 0), (3127 - scrollscreenx, -2590 - scrollscreeny, 50, 58), 3)
            pygame.draw.rect(screen, (104, 24, 20), (2186 - scrollscreenx, -2619 - scrollscreeny, 49, 38))
            pygame.draw.rect(screen, (0, 0, 0), (2186 - scrollscreenx, -2619 - scrollscreeny, 49, 38), 3)
            pygame.draw.rect(screen, (104, 24, 20), (1824 - scrollscreenx, -2661 - scrollscreeny, 46, 78))
            pygame.draw.rect(screen, (0, 0, 0), (1824 - scrollscreenx, -2661 - scrollscreeny, 46, 78), 3)
            pygame.draw.rect(screen, (104, 24, 20), (-612 - scrollscreenx, -666 - scrollscreeny, 1, 1))
            pygame.draw.rect(screen, (0, 0, 0), (-612 - scrollscreenx, -666 - scrollscreeny, 1, 1), 3)
            pygame.draw.rect(screen, (104, 24, 20), (3 - scrollscreenx, -1280 - scrollscreeny, 1, 1))
            pygame.draw.rect(screen, (0, 0, 0), (3 - scrollscreenx, -1280 - scrollscreeny, 1, 1), 3)
            pygame.draw.rect(screen, (104, 24, 20), (4618 - scrollscreenx, -2558 - scrollscreeny, 1, 1))
            pygame.draw.rect(screen, (0, 0, 0), (4618 - scrollscreenx, -2558 - scrollscreeny, 1, 1), 3)
            pygame.draw.rect(screen, (104, 24, 20), (5848 - scrollscreenx, -1683 - scrollscreeny, 1, 1))
            pygame.draw.rect(screen, (0, 0, 0), (5848 - scrollscreenx, -1683 - scrollscreeny, 1, 1), 3)
            pygame.draw.rect(screen, (104, 24, 20), (5860 - scrollscreenx, -1683 - scrollscreeny, 1, 1))
            pygame.draw.rect(screen, (0, 0, 0), (5860 - scrollscreenx, -1683 - scrollscreeny, 1, 1), 3)"""
                
                
                
            
            
            
            
            
            
            
            
            if build_gun:
                buildscreen = pygame.Surface((size))
                buildscreen.blit(tempbackground, (0, 0))
            """blitting the rects"""
            for images in range(number_of_images):
                if build_gun:
                    pygame.draw.rect(buildscreen, (red[images], green[images], blue[images]), (x[images] - scrollscreenx, y[images] - scrollscreeny, width[images], height[images]))
                else:
                    pygame.draw.rect(screen, (red[images], green[images], blue[images]), (x[images] - scrollscreenx, y[images] - scrollscreeny, width[images], height[images]))
                    pygame.draw.rect(screen, (0, 0, 0), (x[images] - scrollscreenx, y[images] - scrollscreeny, width[images], height[images]), 3)  
    
            if build_gun:
                pygame.draw.rect(buildscreen, (red[number_of_images], green[number_of_images], blue[number_of_images]), (x[number_of_images] - scrollscreenx, y[number_of_images] - scrollscreeny, width[number_of_images], height[number_of_images]))
            else:
                pygame.draw.rect(screen, (red[number_of_images], green[number_of_images], blue[number_of_images]), (x[number_of_images] - scrollscreenx, y[number_of_images] - scrollscreeny, width[number_of_images], height[number_of_images]))
    
                pygame.draw.rect(screen, (0, 0, 0), (x[number_of_images] - scrollscreenx, y[number_of_images] - scrollscreeny, width[number_of_images], height[number_of_images]), 3)
            
            
            """color ui"""
            text = font.render("RED",1,(0,0,0))
            screen.blit(text, (640 - 150, 5))
            text = font.render(str(red[number_of_images]),1,(red[number_of_images],0,0))
            screen.blit(text, (640 - 50, 5))
            
            text = font.render("GREEN",1,(0,0,0))
            screen.blit(text, (640 - 150, 50))
            text = font.render(str(green[number_of_images]),1,(0,green[number_of_images],0))
            screen.blit(text, (640 - 50, 50))
            
            text = font.render("BLUE",1,(0,0,0))
            screen.blit(text, (640 - 150, 100))
            text = font.render(str(blue[number_of_images]),1,(0,0,blue[number_of_images]))
            screen.blit(text, (640 - 50, 100))
            
            
            """change between changing screenpos, pos, and size"""
            
            if not build_gun:
                text = font.render("SCREEN POSITION",1,(0,0,0))
                screen.blit(text, (50, 5))
            
            text = font.render("BLOCK POSITION",1,(0,0,0))
            screen.blit(text, (50, 50))
            
            text = font.render("BLOCK SIZE",1,(0,0,0))
            screen.blit(text, (50, 100))
            
            if change == "screenpos" and not build_gun:
                text = font.render("SCREEN POSITION",1,(255,255,255))
                screen.blit(text, (50, 5))
            elif change == "pos":
                text = font.render("BLOCK POSITION",1,(255,255,255))
                screen.blit(text, (50, 50))
            elif change == "size":
                text = font.render("BLOCK SIZE",1,(255,255,255))
                screen.blit(text, (50, 100))
            
            if not build_gun:    
                text = font.render("COLLISION="+str(collision[number_of_images]),1,(0,0,0))
                screen.blit(text, (50, 400))
            
            if mouse_collision.colliderect(pygame.Rect((50, 5), (150, 20))) and not build_gun:
                text = font.render("SCREEN POSITION",1,(255,255,255))
                screen.blit(text, (50, 5))
                if pygame.mouse.get_pressed()[0]:
                    change = "screenpos"
            elif mouse_collision.colliderect(pygame.Rect((50, 50), (150, 20))):
                text = font.render("BLOCK POSITION",1,(255,255,255))
                screen.blit(text, (50, 50))
                if pygame.mouse.get_pressed()[0]:
                    change = "pos"
            elif mouse_collision.colliderect(pygame.Rect((50, 100), (150, 20))):
                text = font.render("BLOCK SIZE",1,(255,255,255))
                screen.blit(text, (50, 100))
                if pygame.mouse.get_pressed()[0]:
                    change = "size"
            elif mouse_collision.colliderect(pygame.Rect((50, 400), (150, 20))):
                text = font.render("COLLISION="+str(collision[number_of_images]),1,(255,255,255))
                screen.blit(text, (50, 400))
                if pygame.mouse.get_pressed()[0]:
                    if collision[number_of_images]:
                        collision[number_of_images] = False
                        pygame.time.delay(300)
                    else:
                        collision[number_of_images] = True
                        pygame.time.delay(300)
            
            if pygame.key.get_pressed()[pygame.K_UP]:
                if change == "screenpos":
                    scrollscreeny -= 1
                elif change == "pos":
                    y[number_of_images] -= 1
                elif change == "size":
                    if height[number_of_images] > 0:
                        height[number_of_images] -= 1
                        
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                if change == "screenpos":
                    scrollscreeny += 1
                elif change == "pos":
                    y[number_of_images] += 1
                elif change == "size":
                    height[number_of_images] += 1
                    
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if change == "screenpos":
                    scrollscreenx -= 1
                elif change == "pos":
                    x[number_of_images] -= 1
                elif change == "size":
                    if width[number_of_images] > 0:
                        width[number_of_images] -= 1
            
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if change == "screenpos":
                    scrollscreenx += 1
                elif change == "pos":
                    x[number_of_images] += 1
                elif change == "size":
                    width[number_of_images] += 1
             
            """optional controls that I personally use so I dont have to keep switching back and forth"""        
            if pygame.key.get_pressed()[pygame.K_i]:
                height[number_of_images] -= 1
            if pygame.key.get_pressed()[pygame.K_k]:
                height[number_of_images] += 1
            if pygame.key.get_pressed()[pygame.K_j]:
                width[number_of_images] -= 1
            if pygame.key.get_pressed()[pygame.K_l]:
                width[number_of_images] += 1
    
            if not build_gun:
                if pygame.key.get_pressed()[pygame.K_w]:
                    scrollscreeny -= 1
                if pygame.key.get_pressed()[pygame.K_s]:
                    scrollscreeny += 1
                if pygame.key.get_pressed()[pygame.K_a]:
                    scrollscreenx -= 1
                if pygame.key.get_pressed()[pygame.K_d]:
                    scrollscreenx += 1
    
            if pygame.key.get_pressed()[pygame.K_r]:
                red[number_of_images] += 1
                if red[number_of_images] > 255:
                    red[number_of_images] = 0
            if pygame.key.get_pressed()[pygame.K_g]:
                green[number_of_images] += 1
                if green[number_of_images] > 255:
                    green[number_of_images] = 0
            if pygame.key.get_pressed()[pygame.K_b]:
                blue[number_of_images] += 1
                if blue[number_of_images] > 255:
                    blue[number_of_images] = 0
            
            
            if campaign:
                for i in range(0, len(ai_blit)):
                    screen.blit(self.character, (ai_blit[i][0] - scrollscreenx, ai_blit[i][1] - scrollscreeny))
                for i in range(0, len(texts_blity)):
                    pygame.draw.rect(screen, (0, 0, 0), (texts_blity[i] - scrollscreenx, 0, 10, 1000))
                for i in range(0, len(texts_blitx)):
                    pygame.draw.rect(screen, (0, 0, 0), (0, texts_blitx[i] - scrollscreeny, 1000, 10))
                if pygame.mouse.get_pressed()[1]:
                    if not pressedone:
                        backup = (mousepos[0] + scrollscreenx, mousepos[1] + scrollscreeny)
                        try:
                            types = raw_input("f or e: ")
                            new = raw_input("angle: ")
                        except:
                            types = input("f or e: ")
                            new = input("angle: ")
                        if types == "f":
                            ai.append("screen.blit(pygame.transform.rotate(self.character,"+str(new)+"), ("+str(backup[0])+" - imagesx, "+str(backup[1])+" - imagesy))")
                        else:
                            ai_enemy.append(str(backup))
                        ai_blit.append(backup)
                    pressedone = True
                if pygame.mouse.get_pressed()[2]:
                    if not pressedtwo:
                        backup = (mousepos[0] + scrollscreenx, mousepos[1] + scrollscreeny)
                        try:
                            new = raw_input("v or h or vd/hd: ")
                        except:
                            new = input("v or h or vd/hd: ")
                        if new == "v":
                            vert = (True, True)
                        elif new == "vd":
                            vert = (True, None)
                        elif new == "hd":
                            vert = (False, None)
                        else:
                            vert = (False, False)
                        try:
                            new = raw_input("text: ")
                        except:
                            new = input("text: ")
                        if vert[1]:
                            texts.append("if "+str(backup[0])+" - 6 <= self.mainx + imagesx <= "+str(backup[0])+" + 6 and not "+str((0, backup[0]))+"in self.campaign_text_check:")
                            texts.append("    "+"self.campaign.text("+"'"+str(new)+"')")
                            texts.append("    return "+str((0, backup[0])))
                            texts_blity.append(backup[0])
                        elif not vert[1]:
                            texts.append("if "+str(backup[1])+" - 6 <= self.mainy + imagesy <= "+str(backup[1])+" + 6 and not "+str((0, backup[1]))+"in self.campaign_text_check:")
                            texts.append("    "+"self.campaign.text("+"'"+str(new)+"')")
                            texts.append("    return "+str((0, backup[1])))
                            texts_blitx.append(backup[1])
                        elif vert[0]:
                            texts.append("if "+str(backup[0])+" - 6 <= self.mainx + imagesx <= "+str(backup[0])+" + 6 and not "+str((0, backup[0]))+"in self.campaign_text_check:")
                            texts.append("    return 'DONE'")
                            texts_blity.append(backup[0])
                        elif not vert[1]:
                            texts.append("if "+str(backup[1])+" - 6 <= self.mainy + imagesy <= "+str(backup[1])+" + 6 and not "+str((0, backup[1]))+"in self.campaign_text_check:")
                            texts.append("    return 'DONE'")
                            texts_blitx.append(backup[1])
                            
                    pressedtwo = True
                if not pygame.mouse.get_pressed()[1]:
                    pressedone = False
                if not pygame.mouse.get_pressed()[2]:
                    pressedtwo = False
            
            text = font.render(str((mousepos[0] + scrollscreenx, mousepos[1] + scrollscreeny)),1,(0,0,0))
            screen.blit(text, (mousepos[0] + 10, mousepos[1]))
            
            if build_gun:
                screen.blit(buildscreen, (300, 220))
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN:
                        number_of_images += 1
                        if x[number_of_images] == 1 and not build_gun:    
                            x[number_of_images] = mousepos[0] + scrollscreenx 
                            y[number_of_images] = mousepos[1] + scrollscreeny
                        red[number_of_images] = red[number_of_images - 1]
                        green[number_of_images] = green[number_of_images - 1]
                        blue[number_of_images] = blue[number_of_images - 1]

                    elif event.key == pygame.K_BACKSPACE:
                        """delete last square"""
                        del(x[number_of_images])
                        del(y[number_of_images])
                        del(width[number_of_images])
                        del(height[number_of_images])
                        del(red[number_of_images])
                        del(blue[number_of_images])
                        del(green[number_of_images]) 
                        number_of_images -= 1
                    elif event.key == pygame.K_LSHIFT:
                        """edit pervious square"""
                        number_of_images -= 1
                    
                    elif event.key == pygame.K_RSHIFT:
                        if self.menu.yes_no("    ARE YOU SURE?") == "no":
                            continue
                        """might need a +- 300 here!!!!!"""
                        spawn_area_x = (min(x) - 300, max(x) - 300)
                        spawn_area_y = (min(y) - 300, max(y) - 300)
                        try:
                            randint(spawn_area_x[0], spawn_area_x[1])
                            randint(spawn_area_y[0], spawn_area_y[1])
                        except:
                            if not build_gun:
                                print("This map is too small and will crash!")
                                sys.exit()
                        
                        for images in range(number_of_images):
                            collision_list.append(pygame.Rect((x[images], y[images]), (width[images], height[images])))
                        
                        if build_gun:
                            self.rects = []
                            for images in range(number_of_images + 1):
                                self.rects.append((None, (red[images], green[images], blue[images]), (x[images] + 50, y[images], width[images], height[images])))
                            return
                                
                        with open(path+str(map_name)+".py", 'w+') as maps:
                            maps.write("import pygame"+"\n")
                            maps.write("from Resources.scripts.Menus import screen #so if display (full/windowed) stays the same\n")
                            maps.write("spawnarea_x = "+str(spawn_area_x)+"\n")
                            maps.write("spawnarea_y = "+str(spawn_area_y)+"\n")
                            maps.write("background_color = "+str((bred, bgreen, bblue))+"\n")
                            maps.write("def blit_map(imagesx, imagesy):"+"\n")
                            for images in range(number_of_images + 1):
                                maps.write("    pygame.draw.rect(screen, ("+str(red[images])+", "+str(green[images])+", "+str(blue[images])+"), ("+str(x[images])+" - imagesx, "+str(y[images])+" - imagesy, "+str(width[images])+", "+str(height[images])+"))"+"\n")
                                maps.write("    pygame.draw.rect(screen, (0, 0, 0), ("+str(x[images])+" - imagesx, "+str(y[images])+" - imagesy, "+str(width[images])+", "+str(height[images])+"), 3)"+"\n")
                            
                            
                            #for campaign
                            #not meant to make a pretty working script, this is for development only
                            for i in range(0, len(ai)):
                                maps.write("    "+ai[i]+"\n")
                            for i in range(0, len(texts)):
                                maps.write("    "+texts[i]+"\n")
                            maps.write("    enemy_pos = [")
                            for i in range(0, len(ai_enemy)):
                                maps.write(ai_enemy[i]+",")
                            
                            
                            maps.write("def collision(imagesx, imagesy):"+"\n")
                            maps.write("    return [")
                            for images in range(number_of_images + 1):
                                if collision[images]:
                                    maps.write("pygame.Rect(("+str(x[images])+" - imagesx, "+str(y[images])+" - imagesy), ("+str(width[images])+", "+str(height[images])+")), ")
                            
                        with open(path+str(map_name)+".py", 'rb+') as maps:
                            maps.seek(-2, os.SEEK_END)
                            maps.truncate()
                        with open(path+str(map_name)+".py", 'a') as maps:
                            maps.write("]")
                            
                        pygame.time.delay(300)    
                        while True:
                            screen.blit(background, (0, 0))
                            text = font.render("GAME RESTART REQUIRED",1,(255,255,255))
                            screen.blit(text, (200, 200))
                            for event in pygame.event.get():  
                                if event.type == pygame.QUIT: 
                                    sys.exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        sys.exit()
            
                            if pygame.mouse.get_pressed()[0]:
                                break        
                            if pygame.key.get_pressed()[pygame.K_RETURN]:
                                break
                            pygame.display.flip()
                                
                        pygame.display.set_mode((640,480))   
                        try:
                            os.execv(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'game.py'), sys.argv)
                        except OSError: #using embedded python 3 windows version
                            sys.exit()
                        
                        
            pygame.display.set_caption("x: " + str(x[number_of_images]) + " y: " + str(y[number_of_images]) + " width: " + str(width[number_of_images]) + " height: " + str(height[number_of_images]))       
            pygame.display.flip()

class Custom_Gun(object):
    def __init__(self, gun_choice):
        import importlib
        self.guns = importlib.import_module("Data.Creations.Guns."+gun_choice)
        try:
            self.shotgun = self.guns.shotgun
        except:
            self.shotgun = False
    def return_gun(self):
        return self.guns.gun()
    def blit_gun(self, angle):
        return self.guns.blit_gun(angle)
        
           
class Play_Maps(object):
    def __init__(self, map_choice):
        import importlib
        self.maps = importlib.import_module("Data.Creations.Maps."+map_choice)
    def spawn_area(self, map_choice):
        self.spawnX = self.maps.spawnarea_x
        self.spawnY = self.maps.spawnarea_y
    def background_color(self, map_choice):
        return self.maps.background_color
    def blit_map(self, imagesx, imagesy):
        self.maps.blit_map(imagesx, imagesy)
    def map_collisions_update(self, imagesx, imagesy):
        return self.maps.collision(imagesx, imagesy)
            

