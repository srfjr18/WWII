import os, pygame, sys

path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', 'Creations', 'Maps', '')
gun_path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', 'Creations', 'Guns', '')

class Creator(object):
    def __init__(self):
        from Resources.scripts.Menus import Menu 
        self.menu = Menu([])
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
        screen = pygame.display.set_mode((640,480))
        background = pygame.Surface(screen.get_size())
        background.fill((0,0,0))
        background = background.convert()
        
        pygame.time.delay(300)
        gun_name = self.menu.name(True, "GUN NAME:")
        
        semiauto = False
        fullauto = True
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
            screen.blit(text, (20, 80))
            
            text = self.menu.font["smallish"].render("full-auto",1,(255,255,255))
            screen.blit(text, (20, 100))
            
            #Done button
            pygame.draw.rect(screen, (255, 255, 255), (screen.get_size()[0] / 3, 400, screen.get_size()[0] / 3, 50), 2)
            text = self.menu.font["small"].render("DONE",1,(255,255,255))
            screen.blit(text, (screen.get_size()[0] / 3 + 25, 415))
            
            if semiauto:
                text = self.menu.font["smallish"].render("semi-auto",1,(255,165,0))
                screen.blit(text, (20, 80))
            else:
                text = self.menu.font["smallish"].render("full-auto",1,(255,165,0))
                screen.blit(text, (20, 100))
            
            if mouse_collision.colliderect(pygame.Rect((20, 80), (120, 30))):
                text = self.menu.font["smallish"].render("semi-auto",1,(255,165,0))
                screen.blit(text, (20, 80))
            elif mouse_collision.colliderect(pygame.Rect((20, 100), (120, 30))):
                text = self.menu.font["smallish"].render("full-auto",1,(255,165,0))
                screen.blit(text, (20, 100))
            elif mouse_collision.colliderect(pygame.Rect((screen.get_size()[0] / 3, 400), (screen.get_size()[0] / 3, 50))):
                text = self.menu.font["small"].render("DONE",1,(255,165,0))
                screen.blit(text, (screen.get_size()[0] / 3 + 25, 415))
            
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
              
                
            if pygame.mouse.get_pressed()[0]:
                if mouse_collision.colliderect(pygame.Rect((20, 80), (120, 30))):
                    semiauto = True
                    fullauto = False
                elif mouse_collision.colliderect(pygame.Rect((20, 100), (120, 30))):
                    semiauto = False
                    fullauto = True
                elif mouse_collision.colliderect(pygame.Rect((screen.get_size()[0] / 3, 400), (screen.get_size()[0] / 3, 50))):
                    with open(gun_path+str(gun_name)+".py", 'w+') as gun:
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
                            damage = damage = str(50 - int(self.slider_dict["damage"] * 4.9))
                        
                        
                        firerate = str(firerate)
                               
                        mag = self.slider_dict["mag size"] * 5
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

                    os.execv(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'game.py'), sys.argv)
                    
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
            pygame.display.flip()
                    
            
    
    def map_builder(self):
        pygame.init()

        screen =  pygame.display.set_mode((640,480))
        clock = pygame.time.Clock()
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
                break
           
        pygame.time.delay(300)
        map_name = self.menu.name(True, "MAP NAME:")
        
        bred = bgreen = bblue = 0
        
        pygame.time.delay(300)
        while True:
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
        
        background = tempbackground
        change = "pos"        
        while True:
            milliseconds = clock.tick(FPS)
            screen.blit(background, (0, 0))
    
            mousepos = pygame.mouse.get_pos()
            mouse_collision = pygame.Rect((mousepos[0], mousepos[1]), (1, 1))
    
            text = font.render(str((mousepos[0] + scrollscreenx, mousepos[1] + scrollscreeny)),1,(0,0,0))
            screen.blit(text, (mousepos[0] + 10, mousepos[1]))
            
            """blitting the rects"""
            for images in range(number_of_images):
                pygame.draw.rect(screen, (red[images], green[images], blue[images]), (x[images] - scrollscreenx, y[images] - scrollscreeny, width[images], height[images]))
                pygame.draw.rect(screen, (0, 0, 0), (x[images] - scrollscreenx, y[images] - scrollscreeny, width[images], height[images]), 3)  
    
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
            
            text = font.render("SCREEN POSITION",1,(0,0,0))
            screen.blit(text, (50, 5))
            
            text = font.render("BLOCK POSITION",1,(0,0,0))
            screen.blit(text, (50, 50))
            
            text = font.render("BLOCK SIZE",1,(0,0,0))
            screen.blit(text, (50, 100))
            
            if change == "screenpos":
                text = font.render("SCREEN POSITION",1,(255,255,255))
                screen.blit(text, (50, 5))
            elif change == "pos":
                text = font.render("BLOCK POSITION",1,(255,255,255))
                screen.blit(text, (50, 50))
            elif change == "size":
                text = font.render("BLOCK SIZE",1,(255,255,255))
                screen.blit(text, (50, 100))
                
            text = font.render("COLLISION="+str(collision[number_of_images]),1,(0,0,0))
            screen.blit(text, (50, 400))
            
            if mouse_collision.colliderect(pygame.Rect((50, 5), (150, 20))):
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
                        if x[number_of_images] == 1:    
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
                        
                        
                        """might need a +- 300 here!!!!!"""
                        spawn_area_x = (min(x) - 300, max(x) - 300)
                        spawn_area_y = (min(y) - 300, max(y) - 300)
                        try:
                            randint(spawn_area_x[0], spawn_area_x[1])
                            randint(spawn_area_y[0], spawn_area_y[1])
                        except:
                            print("This map is too small and will crash!")
                            sys.exit()
                        
                        for images in range(number_of_images):
                            collision_list.append(pygame.Rect((x[images], y[images]), (width[images], height[images])))
                            
                        with open(path+str(map_name)+".py", 'w+') as maps:
                            maps.write("import pygame"+"\n")
                            maps.write("screen =  pygame.display.set_mode((640,480))"+"\n")
                            maps.write("spawnarea_x = "+str(spawn_area_x)+"\n")
                            maps.write("spawnarea_y = "+str(spawn_area_y)+"\n")
                            maps.write("background_color = "+str((bred, bgreen, bblue))+"\n")
                            maps.write("def blit_map(imagesx, imagesy):"+"\n")
                            for images in range(number_of_images + 1):
                                maps.write("    pygame.draw.rect(screen, ("+str(red[images])+", "+str(green[images])+", "+str(blue[images])+"), ("+str(x[images])+" - imagesx, "+str(y[images])+" - imagesy, "+str(width[images])+", "+str(height[images])+"))"+"\n")
                                maps.write("    pygame.draw.rect(screen, (0, 0, 0), ("+str(x[images])+" - imagesx, "+str(y[images])+" - imagesy, "+str(width[images])+", "+str(height[images])+"), 3)"+"\n")
                            
                            maps.write("def collision(imagesx, imagesy):"+"\n")
                            maps.write("    return [")
                            for images in range(number_of_images):
                                if collision[images]:
                                    maps.write("pygame.Rect(("+str(x[images])+" - imagesx, "+str(y[images])+" - imagesy), ("+str(width[images])+", "+str(height[images])+")), ")
                            maps.seek(-2, os.SEEK_END)
                            maps.truncate()
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
                                
                            
                        os.execv(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'game.py'), sys.argv)
                        
                        
            pygame.display.set_caption("x: " + str(x[number_of_images]) + " y: " + str(y[number_of_images]) + " width: " + str(width[number_of_images]) + " height: " + str(height[number_of_images]))       
            pygame.display.flip()

class Custom_Gun(object):
    def __init__(self, gun_choice):
        import importlib
        self.guns = importlib.import_module("Data.Creations.Guns."+gun_choice)
    def return_gun(self):
        return self.guns.gun()
        
           
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
            

