#!/usr/bin/env python
from Resources.scripts.Enemy import *
from Resources.scripts.Menus import *   
import pygame, socket, pickle, sys, math, traceback, os, time
from threading import Thread

if __name__ == "__main__":
    sys.exit()
    
screen = pygame.display.set_mode((640,480))
path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', '')

class online_mode(Enemy, Enemy_Gun):
    def __init__(self, map_choice, max_kills, join=False):
        self.enemy_gun = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
        self.online_max_kills = max_kills
        self.online_map_choice = map_choice
        self.eo = 3
        self.break_waitscreen = False
        self.titlescreen = False
        
        
        
        self.stop_all = False
        
        
        self.online_paused = False
        self.raise_error = False
        
        self.no_lan = False
        self.stop_all = False
        self.joins = False
        
        self.mainx_d = 295
        self.mainy_d = 215
        
        
        self.mainx = 295
        self.mainy = 215
        
        self.angle = 0 
        self.background = pygame.Surface(screen.get_size())
        self.background.fill((0,0,0))
        self.fire = pygame.image.load(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Resources', 'images', '')+'flame.png')
        
        self.flame_thrower = False
        
        self.background = self.background.convert()
        self.shotgun = True
        self.font = {"big": pygame.font.SysFont("monospace", 50), "medium": pygame.font.SysFont("monospace", 35), "small": pygame.font.SysFont("monospace", 25), "smallish": pygame.font.SysFont("monospace", 20), "extrasmall": pygame.font.SysFont("monospace", 15)}
        
        
        self.back = False
        while True:
            if self.stop_all:
                return
            if join:
                self.option = "JOIN SERVER"
            else:
                self.option = Menu(["START SERVER", "JOIN SERVER", "BACK"]).GameSetup()
            if self.option == "BACK":
                self.back = True
                break
            elif self.option == "START SERVER":
                if self.online_map_choice == None:
                    font = pygame.font.SysFont("monospace", 25)
                    text = font.render("NO MAP SELECTED",1,(255,0,0))
                    screen.blit(text, (25, 300))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    self.option = Menu(["START SERVER", "JOIN SERVER", "BACK"]).GameSetup()
                else:  
                    Thread(target=self.server_connector, args=(0,)).start()
                    try:
                        self.server_main()
                    except:
                        continue
                    break
            elif self.option == "JOIN SERVER":
                while True:
                    choice = Menu([]).yes_no("   CHOOSE IP FROM:", "", "PREVIOUS IPS", "  NEW IP", True)
                    if choice == "no":
                        ip = self.ip_enter()
                    elif choice == "back":
                        break
                    else:
                        path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', '')
                        with open(path+"userdata", "rb") as file:
                            data = pickle.load(file)
                        ip_options = data["IP"]
                        ip_options.append("BACK")        
                        ip = Menu(ip_options).GameSetup("long")
                        if ip == "BACK":
                            del(ip)
                            continue
                        break
                            
                        
                            
                try:
                    Thread(target=self.client_connector, args=(ip,0,)).start()
                    self.client_main()
                except:
                    continue
                break
        Enemy_Gun.__init__(self)
        Enemy.__init__(self, 1, 1, 1, 1)
    
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()  
        return ip
            
    def ip_enter(self):
        soundpath = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1]), 'sounds', '')
        self.key = pygame.mixer.Sound(soundpath+"key.wav")
        name = ""
        screen.blit(self.background, (0, 0))
        if self.option == "START SERVER":
            text = self.font["smallish"].render("YOUR COMPUTER'S IP:",1,(255,255,255))
        else:
            text = self.font["smallish"].render("SERVER IP:",1,(255,255,255))
        screen.blit(text, (250, 150))
        pygame.display.flip()
        while True:
            screen.blit(self.background, (0, 0))
            pygame.draw.rect(screen, (255, 255, 255), (210, 225, screen.get_size()[0] / 3, 50), 2)
            if self.option == "START SERVER":
                text = self.font["smallish"].render("YOUR COMPUTER'S IP:",1,(255,255,255))
            else:
                text = self.font["smallish"].render("SERVER IP:",1,(255,255,255))
            screen.blit(text, (220, 150))
            text = self.font["smallish"].render(name+"_",1,(255,255,255))
            screen.blit(text, (220, 250))
            
            
            
            
            
            
            if self.back_button(True):
                return
            
            
            
            
            
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_BACKSPACE:
                        pygame.mixer.Sound.play(self.key) 
                        name = name[:-1]
                    elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        pass
                    elif event.key == pygame.K_RETURN and name != "":
                        pygame.mixer.Sound.play(self.key) 
                        text = self.font["smallish"].render(name+"_",1,(0,0,0))
                        screen.blit(text, (220, 250)) #hide it
                        text = self.font["smallish"].render("SEARCHING...",1,(255,255,255))
                        screen.blit(text, (220, 250))
                        pygame.display.flip()
                        
                        path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', '')
                        
                        with open(path+"userdata", "rb") as file:    
                            data = pickle.load(file)
                        ip = data["IP"]
                        if len(ip) == 5:
                            for num in range(5):
                                if num < 5:
                                    ip[num - 1] = ip[num]
                            ip[5] = name
                        else:
                            ip.append(name)
                        data["IP"] = ip
                        with open(path+"userdata", "wb+") as file:
                            pickle.dump(data, file, protocol=2)
                                    
                        return name
                    else: 
                        pygame.mixer.Sound.play(self.key) 
                        try:
                            if str(chr(event.key)) != ".":
                                int(chr(event.key))                              
                            name = name + str(chr(event.key))
                        except ValueError:
                            pass
                if pygame.mouse.get_pressed()[0] and name != "":
                    pygame.mixer.Sound.play(self.key) 
                    return name
            pygame.display.flip()
        
    
    def recvall(self, sock):
        #this seems to work?
        data = sock.recv(1024)
        while True:
            try:
                data.decode()
                return data
            except:
                pass
            try:
                data = pickle.loads(data)
                return data
            except:
                data += sock.recv(1024)    
    
    def online_pause_thread(self, l, setup):
        self.stop_all = False
        self.online_paused = True
        self.new_setup = setup.pause(setup, True)
        self.flame_thrower = setup.flame_thrower #resume w/ changing loadout                
        if self.new_setup == None: #resume w/o changing loadout
            del(self.new_setup)          
        elif self.new_setup == "end": #end game
            del(self.new_setup)
            if setup.online:
                try:
                    self.c.close()
                except:
                    self.s.close() 
                    
                     
            self.stop_all = True  
            self.titlescreen = True
            self.online_paused = False
            self.stop_all = False
            sys.exit()
        self.online_paused = False
        
    def client_connector(self, ip, l):
        self.break_waitscreen = False
        self.server = False
        while True:
            try:
                self.s = socket.socket()        
                host = str(ip) #'50.33.202.123' #ip
                port = 5006               

                self.s.connect((host, port))
                
                
                self.online_map_choice = self.recvall(self.s).decode()
        
                if self.recvall(self.s).decode() == "True":
                    self.lan = True
                else:
                    self.lan = False

                pygame.time.delay(300)
            
                self.online_max_kills = int(self.recvall(self.s).decode())
                
                pygame.time.delay(300)
                
                self.name = self.recvall(self.s).decode()
                
                with open(path+"userdata", "rb") as file:
                    data = pickle.load(file)
                    name = data["name"]
                    
                self.s.send(str(name).encode())
        
                self.s.settimeout(3)
            except:
                self.joins = True
                print("Error when joining server:")
                traceback.print_exc()
                self.raise_error = True
                try:
                    self.c.close()
                except:
                    self.s.close()
                sys.exit()
                
            self.break_waitscreen = True
            break
    
    def attempt_disconnect(self):
        self.b = socket.socket()        
        host = str(self.get_ip()) 
        port = 5006     
        self.b.settimeout(0.1)        
        self.b.connect((host, port))
        self.b.close()
        self.no_lan = True
        self.stop_all = True
        
    def back_button(self, normal=False):
        pygame.draw.rect(screen, (255, 255, 255), (0, 480 - 50, screen.get_size()[0] / 3, 50), 2)
        text = self.font["small"].render("BACK",1,(255,255,255))
        screen.blit(text, (25, 15 + 480 - 50))
        mousepos = pygame.mouse.get_pos()
        mouse_collision = pygame.Rect((mousepos[0], mousepos[1]), (1,1))
        if mouse_collision.colliderect(pygame.Rect((0, 480 - 50), (screen.get_size()[0] / 3, 50))):
            text = self.font["small"].render("BACK",1,(255,165,0))
            screen.blit(text, (25, 15 + 480 - 50))
            if pygame.mouse.get_pressed()[0]:
                if normal:
                    return True
                if not self.server:
                    self.joins = True
                try:
                    self.s.close()
                except:
                    self.c.close()
                self.raise_error = True
                
                    
    def client_main(self):
        while True:
            screen.blit(self.background, (0, 0))
            text = self.font["smallish"].render("SEARCHING FOR SERVER...",1,(255,255,255))
            screen.blit(text, (170, 150))
            text = self.font["smallish"].render("WAITING FOR CONNECTION...",1,(255,255,255))
            screen.blit(text, (170, 200))
            
            
            self.back_button()
            
            pygame.display.flip()
            
            if self.raise_error:
                self.raise_error = False
                self.stop_all = True
                self.joins = True
                raise Exception
            
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    pygame.display.set_mode((640,480))
                    try:
                        self.c.close()
                    except:
                        self.s.close()
                    os._exit(1)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((640,480))
                        try:
                            self.c.close()
                        except:
                            self.s.close()
                        os._exit(1)
            if self.break_waitscreen:
                break
        

    def server_connector(self, l):
        self.break_waitscreen = False
        self.server = True
        
        
        while True:
            try:
                self.s = socket.socket()
                host = "" #ip #str(ip) #'192.168.254.29' #computer ip
                port = 5006  
                
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                              
                self.s.bind((host, port))       
        
                self.s.listen(5)  
                self.c, self.addr = self.s.accept()
                del(self.s)
            except:
                print("Error when joining server:")
                traceback.print_exc()
                self.raise_error = True
                try:
                    self.c.close()
                except:
                    self.s.close()

                sys.exit()
            
            self.break_waitscreen = True
            break
        
    def server_main(self):
        ip = self.get_ip()
        while True:
            screen.blit(self.background, (0, 0))
            text = self.font["smallish"].render("STARTING SERVER...",1,(255,255,255))
            screen.blit(text, (170, 150))
            text = self.font["smallish"].render("WAITING FOR CONNECTION...",1,(255,255,255))
            screen.blit(text, (170, 200))
            text = self.font["smallish"].render("YOUR IP: "+str(ip),1,(255,255,255))
            screen.blit(text, (170, 300))
            
            
            self.back_button()
            
            
            pygame.display.flip()
            
            if self.raise_error:
                self.raise_error = False
                self.attempt_disconnect()

            
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    pygame.display.set_mode((640,480))
                    try:
                        self.c.close()
                    except:
                        self.s.close()
                    os._exit(1)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((640,480))
                        try:
                            self.c.close()
                        except:
                            self.s.close()
                        os._exit(1)
            if self.break_waitscreen:
                break
        
         
        self.c.send(str(self.online_map_choice).encode())  
        
        if self.no_lan:
            self.lan = ""
        else:  
            self.lan = Menu([]).yes_no("ARE YOU ON LAN OR HAVE", "A STRONG CONNECTION?")
        if self.lan == "yes":
            self.lan = True
        else:
            self.lan = False
            
        self.c.send(str(self.lan).encode())
        
        pygame.time.delay(300)
        
        self.c.send(str(self.online_max_kills).encode())
        
        pygame.time.delay(300)
        
        
        with open(path+"userdata", "rb") as file:
            data = pickle.load(file)
            name = data["name"]
        self.c.send(str(name).encode())
        
        self.name = self.recvall(self.c)
         
        self.c.settimeout(3)
              
    
    def blit_shot(self, nothing=False):
        for rise, run in zip(self.enemy_shotrise_list, self.enemy_shotrun_list):
            if self.flame_thrower or nothing:
                screen.blit(self.fire, (run, rise))
                
            else:
                screen.blit(self.bullet, (run, rise))
            
    def collide_you(self, mainx, mainy, collision_list):
        self.mainx, self.mainy = mainx, mainy
        main_collision = pygame.Rect((self.mainx, self.mainy), self.backup.get_size())
        for rise, run in zip(self.enemy_shotrise_list, self.enemy_shotrun_list):
            for collisions in collision_list[:]:
                if pygame.Rect((run,rise), self.bullet.get_size()).colliderect(main_collision):
                    return True
        
    def send_receive(self, mainx, mainy, stk, angle, imagesx, imagesy, shotrise_list, shotrun_list, gun=None, enemy_gun=None):

        try:
            imagesx[1]
            imagesx_backup = imagesx
            imagesx = imagesx_backup[0]
            realimagesx = imagesx_backup[1]
            
            
            imagesy[1]
            imagesy_backup = imagesy
            imagesy = imagesy_backup[0]
            realimagesy = imagesy_backup[1]
            
        except:
            realimagesx = imagesx
            realimagesy = imagesy
            
    
        self.mainx, self.mainy = mainx, mainy
        
        
        
        if self.mainx != 295:
            shotrise_list = [i - self.mainy + self.mainy_d for i in shotrise_list]
            shotrun_list = [i - self.mainx + self.mainx_d for i in shotrun_list]
        
        
        
        
        """experimental to speed up user side of game on slow server"""
        self.eo += 1
        if self.eo % 4 != 0 and not self.lan:
            try:
                self.diffX
            except:
                try:
                    self.diffX = (self.enemyposX - self.backup_pos[0]) / 4
                    self.diffY = (self.enemyposY - self.backup_pos[1]) / 4
                    """self.diff_shotrise_list = self.diff_shotrun_list = []
                    
                    if len(self.enemy_shotrise_list) == len(self.backup_pos[2]):
                        for rise, run, brise, brun in zip(self.enemy_shotrise_list, self.enemy_shotrun_list, self.backup_pos[2], self.backup_pos[3]):
                            self.diff_shotrise_list.append((rise - brise) / 4)
                            self.diff_shotrun_list.append((run - brun) / 4)"""
                except:
                    self.diffX, self.diffY = 0, 0
                    #self.diff_shotrise_list = self.diff_shotrun_list = []
                          
            """for num in range(0, len(self.enemy_shotrise_list)):
                try:
                    self.enemy_shotrise_list[num] += self.diff_shotrise_list[num]
                    self.enemy_shotrun_list[num] += self.diff_shotrun_list[num]
                except:
                    pass"""
                
            
            
            if self.diffX < 30 and self.diffY < 30:
                self.enemyposX += self.diffX
                self.enemyposY += self.diffY                        
            return
        else:
            try:
                del(self.diffX)
                del(self.diffY)
                self.backup_pos = (self.enemyposX, self.enemyposY) #, self.enemy_shotrise_list, self.enemy_shotrun_list)
            except:
                pass 
            
            
        if enemy_gun != None:
            self.enemy_gun = enemy_gun    
        if self.option == "JOIN SERVER":
            data = pickle.dumps([stk, angle, imagesx, imagesy, shotrise_list, shotrun_list], protocol=2)
            try:
                if gun != None:
                    self.s.send(pickle.dumps([gun], protocol=2))
                else:
                    self.s.send(data)
            except:
                return True
            
                
            """for gunshots"""
            try:
                backup_shot_len = len(self.enemy_shotrise_list)
            except:
                beckup_shot_len = []
                
            
            
                
            try:
                new = self.recvall(self.s)
            except:
                return True
            
            
            if new != "pause":
                
                try:
                    self.enemy_stk, self.angle, self.enemyposX, self.enemyposY, self.enemy_shotrise_list, self.enemy_shotrun_list = new
                    if str(self.enemy_stk) == "30.1" or 27.1 > self.enemy_stk > 27.08:
                        self.flame_thrower = True
                    else:
                        self.flame_thrower = False
                except (TypeError, ValueError): #gun model was sent instead
                    bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
                    try:
                        for i in new[0]:
                            pygame.draw.rect(bg, i[1], i[2])
                        self.enemy_gun = bg
                    except (TypeError, IndexError):
                        pass
                    except:
                        traceback.print_exc()
                        return True
                    
                
                
            newX = self.enemyposX + self.mainx
            newY = self.enemyposY + self.mainy    
            
            self.enemyposX += self.mainx_d
            self.enemyposY += self.mainy_d
            
            self.enemy_shotrise_list = [(newY - realimagesy) + i - self.mainy for i in self.enemy_shotrise_list]
            self.enemy_shotrun_list = [(newX - realimagesx) + i - self.mainx for i in self.enemy_shotrun_list]
            
            
            """also for gunshots"""
            if len(self.enemy_shotrise_list) > backup_shot_len:
                pygame.mixer.Sound.play(self.gunshot)
            
        elif self.option == "START SERVER":
            
            """for gunshots"""
            try:
                backup_shot_len = len(self.enemy_shotrise_list)
            except:
                beckup_shot_len = []
        
        
            try:
                new = self.recvall(self.c)
            except:
                return True
            
            if new != "pause":
                
                try:
                    self.enemy_stk, self.angle, self.enemyposX, self.enemyposY, self.enemy_shotrise_list, self.enemy_shotrun_list = new
                    if str(self.enemy_stk) == "30.1" or 27.1 > self.enemy_stk > 27.08:
                        self.flame_thrower = True
                    else:
                        self.flame_thrower = False
                except (TypeError, ValueError): #gun model was sent instead
                    bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
                    try:
                        for i in new[0]:
                            pygame.draw.rect(bg, i[1], i[2])
                        self.enemy_gun = bg
                    except (TypeError, IndexError):
                        pass
                    except:
                        traceback.print_exc()
                        return True
            
            
            newX = self.enemyposX + self.mainx
            newY = self.enemyposY + self.mainy
            
            self.enemyposX += self.mainx_d
            self.enemyposY += self.mainy_d
            
            
            
            
            
            self.enemy_shotrise_list = [(newY - realimagesy) + i - self.mainy for i in self.enemy_shotrise_list]
            self.enemy_shotrun_list = [(newX - realimagesx) + i - self.mainx for i in self.enemy_shotrun_list]
            
            data = pickle.dumps([stk, angle, imagesx, imagesy, shotrise_list, shotrun_list], protocol=2)
            try:
                if gun != None:
                    self.c.send(pickle.dumps([gun], protocol=2))
                else:
                    self.c.send(data)
            except:
                return True
                
                
            """also for gunshots"""
            if len(self.enemy_shotrise_list) > backup_shot_len:
                pygame.mixer.Sound.play(self.gunshot)
            
        
