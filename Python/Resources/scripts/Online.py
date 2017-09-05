#!/usr/bin/env python
from Resources.scripts.Enemy import *
from Resources.scripts.Menus import *   
import pygame, socket, pickle, sys, math, traceback, os
from threading import Thread

if __name__ == "__main__":
    sys.exit()
    
screen = pygame.display.set_mode((640,480))

class online_mode(Enemy, Enemy_Gun):
    def __init__(self, map_choice, max_kills):
        self.enemy_gun = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
        self.online_max_kills = max_kills
        self.online_map_choice = map_choice
        self.eo = 3
        self.mainx = 300
        self.mainy = 240
        self.angle = 0 
        self.background = pygame.Surface(screen.get_size())
        self.background.fill((0,0,0))
        self.background = self.background.convert()
        self.font = {"big": pygame.font.SysFont("monospace", 50), "medium": pygame.font.SysFont("monospace", 35), "small": pygame.font.SysFont("monospace", 25), "smallish": pygame.font.SysFont("monospace", 20), "extrasmall": pygame.font.SysFont("monospace", 15)}
        self.option = Menu(["START SERVER", "JOIN SERVER", "BACK"]).GameSetup()
        
        
        self.back = False
        while True:
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
                    try:
                        self.server()
                        break
                    except: 
                        self.kill_thread = True
                        print("Error when creating server:")
                        traceback.print_exc()
                        continue
            elif self.option == "JOIN SERVER":
                choice = Menu([]).yes_no("   CHOOSE IP FROM:", "", "PREVIOUS IPS", "  NEW IP")
                if choice == "no":
                    ip = self.ip_enter()
                else:
                    path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', '')
                    """with open(path+"ips", "r") as file:
                        ip_options = []
                        for lines in file.readlines():
                            ip_options.append(lines.rstrip())"""
                    with open(path+"userdata", "rb") as file:
                        data = pickle.load(file)
                    ip_options = data["IP"]
                    ip_options.append("BACK")        
                    ip = Menu(ip_options).GameSetup("long")
                    if ip == "BACK":
                        del(ip)
                            
                try:
                    self.client(ip)
                    break
                except UnboundLocalError:
                    pass
                except:
                    self.kill_thread = True
                    print("Error when joining server:")
                    traceback.print_exc()
        Enemy_Gun.__init__(self)
        Enemy.__init__(self, 1, 1, 1, 1)
    
    def exit_script(self, l):
        self.kill_thread = False
        while True:
            if self.kill_thread:
                sys.exit() 
        
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    pygame.display.set_mode((640,480))
                    try:
                        self.c.close
                    except:
                        self.s.close
                    os._exit(1)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RSHIFT:
                        print("wtf")
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((640,480))
                        try:
                            self.c.close
                        except:
                            self.s.close
                        os._exit(1)
        
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
                        """deletefirstline = False
                        
                        if not os.path.isfile(path+'ips'):
                            create = open(path+'ips', 'w+')
                            create.close()
                        
                        with open(path+'ips', 'r') as file:
                            deletefirstline = len(file.readlines()) >= 5
                            
                            
                        new = ""    
                        if deletefirstline:
                            with open(path+'ips', 'r+') as file:
                                num = 0
                                for lines in file.readlines():
                                    num += 1
                                    if num > 1:
                                        new += str(lines)
                                        
                        if deletefirstline:
                            with open(path+"ips", "w") as file:               
                                file.write(new)
                        
                        
                        with open(path+'ips', 'a') as file:
                            file.write(name+"\n")"""
                        
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
        
    def client(self, ip):
        
        Thread(target=self.exit_script, args=(0,)).start()
    
        self.s = socket.socket()        
        host = str(ip) #'50.33.202.123' #ip
        port = 5006               
        
        
        screen.blit(self.background, (0, 0))
        text = self.font["smallish"].render("SEARCHING FOR SERVER...",1,(255,255,255))
        screen.blit(text, (170, 150))
        text = self.font["smallish"].render("WAITING FOR CONNECTION...",1,(255,255,255))
        screen.blit(text, (170, 200))
        pygame.display.flip()
        self.s.connect((host, port))
        
        self.kill_thread = True
        
        
        self.online_map_choice = self.recvall(self.s).decode()
        
        if self.recvall(self.s).decode() == "True":
            self.lan = True
        else:
            self.lan = False
        
        pygame.time.delay(300)
            
        self.online_max_kills = int(self.recvall(self.s).decode())
        
        self.s.settimeout(3)
        
        #self.recvall(self.s) 
        #self.s.send(raw_input("Client please type: "))
        #s.close()

    def server(self):
    
        Thread(target=self.exit_script, args=(0,)).start()
    
        self.s = socket.socket()
        host = "" #ip #str(ip) #'192.168.254.29' #computer ip
        port = 5006                
        self.s.bind((host, port))       
        
        screen.blit(self.background, (0, 0))
        text = self.font["smallish"].render("STARTING SERVER...",1,(255,255,255))
        screen.blit(text, (170, 150))
        text = self.font["smallish"].render("WAITING FOR CONNECTION...",1,(255,255,255))
        screen.blit(text, (170, 200))
        pygame.display.flip()
        
        self.s.listen(5)  
        self.c, self.addr = self.s.accept()
        
        self.kill_thread = True
         
        self.c.send(str(self.online_map_choice).encode())    
        self.lan = Menu([]).yes_no("ARE YOU ON LAN OR HAVE", "A STRONG CONNECTION?")
        if self.lan == "yes":
            self.lan = True
        else:
            self.lan = False
            
        self.c.send(str(self.lan).encode())
        
        pygame.time.delay(300)
        
        self.c.send(str(self.online_max_kills).encode())
         
        self.c.settimeout(3)
              
        #self.c.send(raw_input("Server please type: "))

        #c.close()
    
    def blit_shot(self):
        for rise, run in zip(self.enemy_shotrise_list, self.enemy_shotrun_list):
            screen.blit(self.bullet, (run, rise))
            
    def collide_you(self, collision_list):
        main_collision = pygame.Rect((self.mainx, self.mainy), self.backup.get_size())
        for rise, run in zip(self.enemy_shotrise_list, self.enemy_shotrun_list):
            for collisions in collision_list[:]:
                if pygame.Rect((run,rise), self.bullet.get_size()).colliderect(main_collision):
                    return True
        
    def send_receive(self, stk, angle, imagesx, imagesy, shotrise_list, shotrun_list, gun=None):
    
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
                except (TypeError, ValueError): #gun model was sent instead
                    bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
                    try:
                        for i in new[0]:
                            pygame.draw.rect(bg, i[1], i[2])
                        self.enemy_gun = bg
                    except:
                        return True
                
                
                
            
            self.enemyposX += self.mainx
            self.enemyposY += self.mainy
            
            self.enemy_shotrise_list = [(self.enemyposY - imagesy) + i - self.mainy for i in self.enemy_shotrise_list]
            self.enemy_shotrun_list = [(self.enemyposX - imagesx) + i - self.mainx for i in self.enemy_shotrun_list]
            
            
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
                except (TypeError, ValueError): #gun model was sent instead
                    bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
                    try:
                        for i in new[0]:
                            pygame.draw.rect(bg, i[1], i[2])
                        self.enemy_gun = bg
                    except:
                        return True
            
            self.enemyposX += self.mainx
            self.enemyposY += self.mainy
            
            self.enemy_shotrise_list = [(self.enemyposY - imagesy) + i - self.mainy for i in self.enemy_shotrise_list]
            self.enemy_shotrun_list = [(self.enemyposX - imagesx) + i - self.mainx for i in self.enemy_shotrun_list]
            
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
            
