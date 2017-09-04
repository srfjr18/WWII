import os, pygame, sys, socket, pickle
from random import randint
from Resources.scripts.Guns import *
from Resources.scripts.Creator import *
from uuid import getnode

if __name__ == "__main__":
    sys.exit()

pygame.init()
screen =  pygame.display.set_mode((640,480))
path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', '')
soundpath = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1]), 'sounds', '')

class Menu(object):
    def __init__(self, words):
        pygame.display.set_caption("WWII")
        self.key = pygame.mixer.Sound(soundpath+"key.wav")
        self.click = pygame.mixer.Sound(soundpath+"click.wav")
        self.background = pygame.Surface(screen.get_size())
        self.background.fill((0,0,0))
        self.background = self.background.convert()
        self.words = words
        self.font = {"big": pygame.font.SysFont("monospace", 50), "medium": pygame.font.SysFont("monospace", 35), "small": pygame.font.SysFont("monospace", 25), "smallish": pygame.font.SysFont("monospace", 20), "extrasmall": pygame.font.SysFont("monospace", 15)}
        
        """checking if mac matches up with the mac in userdata.
        I call this frequently so I figured why not check here"""
        try:
            mac = ':'.join(("%012X" % getnode())[i:i+2] for i in range(0, 12, 2))
            with open(path+"userdata", "r") as file:
                data = pickle.load(file)
            if mac != data["MAC"]:
                raise ValueError("Userdata file is from another system! (MAC does not match)")
        except IOError: #file hasn't been made yet
            pass
    
    def end_screen(self, kills, deaths):
        pygame.time.delay(300)
        pressed = True
        while True:
            screen.blit(self.background, (0, 0))
            if kills > deaths:
                text = self.font["big"].render("YOU WIN",1,(255,255,255))
                screen.blit(text, (220, 200))
            elif deaths > kills:
                text = self.font["big"].render("YOU LOSE",1,(255,255,255))
                screen.blit(text, (190, 200))
            else:
                text = self.font["big"].render("DRAW",1,(255,255,255))
                screen.blit(text, (245, 200))
            
            text = self.font["medium"].render(str(kills)+" - "+str(deaths),1,(255,255,255))
            screen.blit(text, (250, 250))
            
            text = self.font["small"].render("left click to continue",1,(255,255,255))
            screen.blit(text, (150, 300))
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            if pygame.mouse.get_pressed()[0] and not pressed:
                break
            elif not pygame.mouse.get_pressed()[0]:
                pressed = False #used so you cant hold the button without even seeing the killed screen
            pygame.display.flip()
    
    def killed(self):
        pygame.time.delay(300)
        pressed = True
        enemies = ["dankman", "xXrektXx", "FAZE quickscope", "OPTIC NERVE", "mubba bubba", "xxNOsCoPeXX"]
        enemy = enemies[randint(0,5)]
        while True:
            screen.blit(self.background, (0, 0))
            text = self.font["medium"].render("KILLED BY "+enemy,1,(255,255,255))
            screen.blit(text, (100, 225))
            text = self.font["small"].render("left click to respawn",1,(255,255,255))
            screen.blit(text, (150, 275))
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            if pygame.mouse.get_pressed()[0] and not pressed:
                break
            elif not pygame.mouse.get_pressed()[0]:
                pressed = False #used so you cant hold the button without even seeing the killed screen
            pygame.display.flip()
        

    def name(self, different=False, diftext=None, int_only=False):
        name = ""
        shift = False
        screen.blit(self.background, (0, 0))
        text = self.font["small"].render("NAME:",1,(255,255,255))
        screen.blit(text, (250, 150))
        pygame.display.flip()
        while True:
            screen.blit(self.background, (0, 0))
            pygame.draw.rect(screen, (255, 255, 255), (210, 225, screen.get_size()[0] / 3, 50), 2)
            if not different:
                text = self.font["big"].render("NAME:",1,(255,255,255))
                screen.blit(text, (250, 150))
            else:
                text = self.font["big"].render(str(diftext),1,(255,255,255))
                screen.blit(text, (200, 150))
            if len(name) < 10:
                text = self.font["smallish"].render(name+"_",1,(255,255,255))
            else:
                text = self.font["smallish"].render(name,1,(255,255,255))
            screen.blit(text, (250, 250))
            
            if pygame.key.get_pressed()[pygame.K_RSHIFT] or pygame.key.get_pressed()[pygame.K_LSHIFT]:
                shift = True
            elif not pygame.key.get_pressed()[pygame.K_RSHIFT] and not pygame.key.get_pressed()[pygame.K_LSHIFT]:
                shift = False
            
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_BACKSPACE:
                        pygame.mixer.Sound.play(self.key) 
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN and name != "":
                        pygame.mixer.Sound.play(self.key)
                        if not different: 
                            with open(path+"userdata", "r") as file:
                                data = pickle.load(file)
                            data["name"] = name
                            with open(path+"userdata", "w+") as file:
                                pickle.dump(data, file, protocol=2) 
                            """with open (path+'data', 'w+') as file:
                                file.write(name+'\n'+'25')"""
                            return
                        else:
                            return name
                    elif len(name) < 10:  
                        pygame.mixer.Sound.play(self.key)
                        try: 
                            if int_only:
                                int(chr(event.key))
                                
                            if str(chr(event.key)) == '.':
                                raise ValueError
                                 
                            if shift:
                                name = name + str(chr(event.key)).upper()
                            else:
                                name = name + str(chr(event.key))
                        except ValueError:
                            pass
                if pygame.mouse.get_pressed()[0] and name != "":
                    pygame.mixer.Sound.play(self.key)
                    if not different:
                        with open(path+"userdata", "r") as file:
                            data = pickle.load(file)
                        data["name"] = name
                        data["rank"] = 25
                        with open(path+"userdata", "w+") as file:
                            pickle.dump(data, file, protocol=2) 
                        """with open (path+'data', 'w+') as file:
                            file.write(name+'\n'+'25')"""
                        return
                    else:
                        return name
            pygame.display.flip()
                
                
    
    def TitleScreen(self):
        while True:
            screen.blit(self.background, (0, 0))
            text = self.font["big"].render("WWII",1,(255,255,255))
            screen.blit(text, (250, 225))
            text = self.font["small"].render("left click to continue",1,(255,255,255))
            screen.blit(text, (150, 275))
            pygame.display.flip()
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            if pygame.mouse.get_pressed()[0]:
                pygame.mixer.Sound.play(self.click)
                break
        if not os.path.isfile(path+'userdata'):
            mac = ':'.join(("%012X" % getnode())[i:i+2] for i in range(0, 12, 2))
            new = {"name": "NONE", "rank": 25, "LOADOUT 1": ["M1 GARAND", "RATIONS", "HOLLOW POINTS", "MEDIC"], "LOADOUT 2": ["M1 GARAND", "RATIONS", "HOLLOW POINTS", "MEDIC"], "LOADOUT 3": ["M1 GARAND", "RATIONS", "HOLLOW POINTS", "MEDIC"], "LOADOUT 4": ["M1 GARAND", "RATIONS", "HOLLOW POINTS", "MEDIC"], "LOADOUT 5": ["M1 GARAND", "RATIONS", "HOLLOW POINTS", "MEDIC"], "IP": [], "MAC": mac}
            with open(path+"userdata", "w+") as file:
                pickle.dump(new, file, protocol=2)
            self.name()
        return False
                
    def GameSetup(self, *description):
        pygame.time.delay(300)
        long_boxes = False
        while True:
            try:
                if description[0] == "long":
                    long_boxes = True
            except:
                pass
        
            screen.blit(self.background, (0, 0))
            
            if not long_boxes:
                text = self.font["big"].render("WWII",1,(255,255,255))
                screen.blit(text, (250, 225))
            
            
            
            for num in range(0, len(self.words)):
                text = self.font["small"].render(self.words[num],1,(255,255,255))
                screen.blit(text, (25, 15 + 50 * num))
                if long_boxes:
                    pygame.draw.rect(screen, (255, 255, 255), (0, 50 * num, screen.get_size()[0] / 2.2, 50), 2)
                else:            
                    pygame.draw.rect(screen, (255, 255, 255), (0, 50 * num, screen.get_size()[0] / 3, 50), 2)
            
            mousepos = pygame.mouse.get_pos()
            mouse_collision = pygame.Rect((mousepos[0], mousepos[1]), (1,1))
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            try:
                if description[0] == "name":
                    """"with open(path+"data", "r") as file:
                        name, self.rank = file.readlines()
                        name = name.rstrip()
                        self.rank = self.rank.rstrip()"""
                    with open(path+"userdata", "r") as file:
                        data = pickle.load(file)
                    name = data["name"]
                    self.rank = data["rank"]
                    
                    self.rank = int(int(self.rank) / 25)
                    pygame.draw.rect(screen, (255, 255, 255), (480 - 55, 0, screen.get_size()[0] / 3, 50), 2)
                    text = self.font["small"].render(name,1,(255,255,255))
                    screen.blit(text, (480 - 25, 15))
                    text = self.font["small"].render(str(self.rank),1,(255,255,255))
                    screen.blit(text, (480 + 125, 15))
            except:
                pass
            
                    
            
            try:
                description[0]
            except:
                description = (None,) #fixes errors with index being out of range
            
            if description[0] == "rank":
                """with open(path+"userdata", "r") as file:
                    name, self.rank = file.readlines()
                    name = name.rstrip()
                    self.rank = self.rank.rstrip()"""
                with open(path+"userdata", "r") as file:
                    data = pickle.load(file)
                
                self.rank = data["rank"]
                self.rank = int(int(self.rank) / 25)
                self.required_ranks = description[1]
                       

            for num in range(0, len(self.words)):
                if mouse_collision.colliderect(pygame.Rect((0, num * 50), (screen.get_size()[0] / 3, 50))):
                
                    #pygame.mixer.Sound.play(self.hover)
                    
                    
                    text = self.font["small"].render(self.words[num],1,(255,165,0))
                    screen.blit(text, (25, 15 + 50 * num))
                    
                    try:
                        if self.rank < self.required_ranks[num]:
                            text = self.font["small"].render("UNLOCKED AT RANK " + str(self.required_ranks[num]),1,(255,255,255))
                            screen.blit(text, (250, 15 + 50 * num))  
                    except:
                        pass
                    
                    try: #this requires our perks to also have the rank args
                        if description[num + 2] != "name" and description[num + 2] != "rank":
                            text = self.font["extrasmall"].render(description[num + 2],1,(255,255,255))
                            screen.blit(text, (25, 320))
                    except:
                        pass
                
            if pygame.mouse.get_pressed()[0]:
                for num in range(0, len(self.words)):
                    if mouse_collision.colliderect(pygame.Rect((0, 50 * num), (screen.get_size()[0] / 3, 50))):
                        pygame.mixer.Sound.play(self.click)
                        if self.words[num] != "BACK":
                            if description[0] == "rank" and self.rank >= self.required_ranks[num]:
                                return self.words[num]
                            elif description[0] != "rank":
                                return self.words[num]
                        else:
                            return self.words[num]
                        
            pygame.display.flip()
            
            
    def yes_no(self, question, questiontwo="", yes="YES", no="NO"):
        pygame.time.delay(300)
        while True:
            screen.blit(self.background, (0, 0))

            text = self.font["medium"].render(question,1,(255,255,255))
            screen.blit(text, (100, 150))
            text = self.font["medium"].render(questiontwo,1,(255,255,255))
            screen.blit(text, (100, 200))

            text = self.font["small"].render(yes,1,(255,255,255))
            screen.blit(text, (125, 15 + 50 * 5))            
            pygame.draw.rect(screen, (255, 255, 255), (100, 50 * 5, screen.get_size()[0] / 3, 50), 2)
            
            text = self.font["small"].render(no,1,(255,255,255))
            screen.blit(text, (125 + screen.get_size()[0] / 3, 15 + 50 * 5))            
            pygame.draw.rect(screen, (255, 255, 255), (100 + screen.get_size()[0] / 3, 50 * 5, screen.get_size()[0] / 3, 50), 2)
            
            mousepos = pygame.mouse.get_pos()
            mouse_collision = pygame.Rect((mousepos[0], mousepos[1]), (1,1))
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                        
            if mouse_collision.colliderect(pygame.Rect((100, 5 * 50), (screen.get_size()[0] / 3, 50))):
                text = self.font["small"].render(yes,1,(255,165,0))
                screen.blit(text, (125, 15 + 50 * 5))
                
            elif mouse_collision.colliderect(pygame.Rect((100 + screen.get_size()[0] / 3, 5 * 50), (screen.get_size()[0] / 3, 50))):
                text = self.font["small"].render(no,1,(255,165,0))
                screen.blit(text, (125 + screen.get_size()[0] / 3, 15 + 50 * 5))

                
            if pygame.mouse.get_pressed()[0]:
                if mouse_collision.colliderect(pygame.Rect((100, 5 * 50), (screen.get_size()[0] / 3, 50))):
                    pygame.mixer.Sound.play(self.click)
                    return "yes"
                elif mouse_collision.colliderect(pygame.Rect((100 + screen.get_size()[0] / 3, 5 * 50), (screen.get_size()[0] / 3, 50))):
                    pygame.mixer.Sound.play(self.click)
                    return "no"
                        
            pygame.display.flip()


class Loadouts(object):
    def __init__(self, ifback):
        with open(path+"userdata", "r") as file:
            data = pickle.load(file)
        """self.loadout_one = []
        self.loadout_two = []
        self.loadout_three = []
        self.loadout_four = []
        self.loadout_five = []"""
        
        self.loadout_one = data["LOADOUT 1"]
        self.loadout_two = data["LOADOUT 2"]
        self.loadout_three = data["LOADOUT 3"]
        self.loadout_four = data["LOADOUT 4"]
        self.loadout_five = data["LOADOUT 5"]
        
        self.click = pygame.mixer.Sound(soundpath+"click.wav")
        if ifback:
            self.words = ["LOADOUT 1", "LOADOUT 2", "LOADOUT 3", "LOADOUT 4", "LOADOUT 5", "BACK"]
        else:
            self.words = ["LOADOUT 1", "LOADOUT 2", "LOADOUT 3", "LOADOUT 4", "LOADOUT 5"]
         
        """for lines in open(path+'LOADOUT 1', 'r').readlines():
            self.loadout_one.append(lines.rstrip())
        for lines in open(path+'LOADOUT 2', 'r').readlines():
            self.loadout_two.append(lines.rstrip())
        for lines in open(path+'LOADOUT 3', 'r').readlines():
            self.loadout_three.append(lines.rstrip())
        for lines in open(path+'LOADOUT 4', 'r').readlines():
            self.loadout_four.append(lines.rstrip())
        for lines in open(path+'LOADOUT 5', 'r').readlines():
            self.loadout_five.append(lines.rstrip())"""
            
            
        self.background = pygame.Surface(screen.get_size())
        self.background.fill((0,0,0))
        self.background = self.background.convert()
        
        self.font = {"big": pygame.font.SysFont("monospace", 50), "small": pygame.font.SysFont("monospace", 25)}
            
    def display_loadout(self):
        pygame.time.delay(300)
        while True:
            screen.blit(self.background, (0, 0))

            text = self.font["big"].render("WWII",1,(255,255,255))
            screen.blit(text, (250, 225))
            
            mousepos = pygame.mouse.get_pos()
            mouse_collision = pygame.Rect((mousepos[0], mousepos[1]), (1,1))
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            for num in range(0, len(self.words)):
                text = self.font["small"].render(self.words[num],1,(255,255,255))
                screen.blit(text, (25, 15 + 50 * num))            
                pygame.draw.rect(screen, (255, 255, 255), (0, 50 * num, screen.get_size()[0] / 3, 50), 2)

            for num in range(0, len(self.words)):
                if mouse_collision.colliderect(pygame.Rect((0, num * 50), (screen.get_size()[0] / 3, 50))):
                    text = self.font["small"].render(self.words[num],1,(255,165,0))
                    screen.blit(text, (25, 15 + 50 * num))
                    if self.words[num] == "LOADOUT 1":
                        for num in range(0, len(self.loadout_one)):
                            text = self.font["small"].render(self.loadout_one[num],1,(255,255,255))
                            screen.blit(text, (480 - 25, 15 + 50 * num))            
                            pygame.draw.rect(screen, (255, 255, 255), (480 - 55, 50 * num, screen.get_size()[0] / 3, 50), 2)
                    elif self.words[num] == "LOADOUT 2":
                        for num in range(0, len(self.loadout_two)):
                            text = self.font["small"].render(self.loadout_two[num],1,(255,255,255))
                            screen.blit(text, (480 - 25, 15 + 50 * num))            
                            pygame.draw.rect(screen, (255, 255, 255), (480 - 55, 50 * num, screen.get_size()[0] / 3, 50), 2)
                    elif self.words[num] == "LOADOUT 3":
                        for num in range(0, len(self.loadout_three)):
                            text = self.font["small"].render(self.loadout_three[num],1,(255,255,255))
                            screen.blit(text, (480 - 25, 15 + 50 * num))            
                            pygame.draw.rect(screen, (255, 255, 255), (480 - 55, 50 * num, screen.get_size()[0] / 3, 50), 2)
                    elif self.words[num] == "LOADOUT 4":
                        for num in range(0, len(self.loadout_four)):
                            text = self.font["small"].render(self.loadout_four[num],1,(255,255,255))
                            screen.blit(text, (480 - 25, 15 + 50 * num))            
                            pygame.draw.rect(screen, (255, 255, 255), (480 - 55, 50 * num, screen.get_size()[0] / 3, 50), 2)
                    elif self.words[num] == "LOADOUT 5":
                        for num in range(0, len(self.loadout_five)):
                            text = self.font["small"].render(self.loadout_five[num],1,(255,255,255))
                            screen.blit(text, (480 - 25, 15 + 50 * num))            
                            pygame.draw.rect(screen, (255, 255, 255), (480 - 55, 50 * num, screen.get_size()[0] / 3, 50), 2)
                            
                
            if pygame.mouse.get_pressed()[0]:
                for num in range(0, len(self.words)):
                    if mouse_collision.colliderect(pygame.Rect((0, 50 * num), (screen.get_size()[0] / 3, 50))):
                        pygame.mixer.Sound.play(self.click)
                        return self.words[num]
            pygame.display.flip()

class Setup(object):
    def __init__(self, map_choice="SHIP", custom=False):
        self.map_choice = map_choice
        self.custom = custom
        self.max_kills = 1000000
        self.online = False
        self.background = pygame.Surface(screen.get_size())
        self.background.fill((0,0,0))
        self.background = self.background.convert()
        self.font = {"big": pygame.font.SysFont("monospace", 50), "medium": pygame.font.SysFont("monospace", 35), "small": pygame.font.SysFont("monospace", 25), "smallish": pygame.font.SysFont("monospace", 20), "extrasmall": pygame.font.SysFont("monospace", 15)}
    
    def update_data(self, number, loadout_number, new):
        with open(path+"userdata", "r") as file:
            data = pickle.load(file)
        data[loadout_number][number] = new
        with open(path+"userdata", "w+") as file:
            pickle.dump(data, file, protocol=2) 
        
    def MainMenu(self):
        pygame.mixer.music.load(soundpath+'music.wav')
        pygame.mixer.music.play(-1)
    
        go_back_once = False
        #self.custom = False
        while True:
            choice = Menu(words = ["LOADOUTS", "MAPS", "CREATE", "OPTIONS", "ONLINE GAME", "OFFLINE GAME"]).GameSetup("name", "", "", "CURRENT MAP: "+str(self.map_choice))
            if choice == "MAPS":
                go_back_once = True
                while True:
                    try:
                        map_choice_backup = self.map_choice
                    except:
                        pass
                    if go_back_once:
                        self.map_choice = Menu(["CUSTOM", "SHIP", "PACIFIC", "BARREN", "TOWN", "BASE", "BACK"]).GameSetup()
                    else:
                        break
                
                    if self.map_choice == "CUSTOM":
                        go_back_once = True
                        self.custom = True
                        custom_maps = os.listdir(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', 'Creations', 'Maps'))
                        custom_maps = [s for s in custom_maps if s.endswith('.py')]
                        custom_maps = [maps[:-3] for maps in custom_maps]
                        custom_maps.remove("__init__")
                        custom_maps.append("BACK")
                        self.map_choice = Menu(custom_maps).GameSetup()
                        if self.map_choice == "BACK":
                            self.custom = False
                    else:
                        go_back_once = False
                    
                    if self.map_choice == "BACK":
                        try:
                            self.map_choice = map_choice_backup
                        except:
                            del(self.map_choice)
            if choice == "CREATE":
                go_back_once = True
                while True:
                    if go_back_once:
                        create_choice = Menu(["GUN", "MAP", "DELETE GUN", "DELETE MAP", "BACK"]).GameSetup("rank", [20, 25, 20, 25])
                    else:
                        break
                    go_back_once = False
                    creator = Creator()
                    if create_choice == "GUN":
                        creator.gun_builder()
                    elif create_choice == "MAP":
                        creator.map_builder()
                    elif create_choice == "DELETE GUN":
                        custom_guns = os.listdir(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', 'Creations', 'Guns'))
                        custom_guns = [s for s in custom_guns if s.endswith('.py')]
                        custom_guns = [guns[:-3] for guns in custom_guns]
                        custom_guns.remove("__init__")
                        custom_guns.append("BACK")
                        delete = Menu(custom_guns).GameSetup()
                        go_back_once = True
                        if delete != "BACK":
                            os.remove(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', 'Creations', 'Guns', '')+delete+".py")
                            try:
                                os.remove(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', 'Creations', 'Guns', '')+delete+".pyc")
                            except OSError:
                                pass
                            
                            
                            #LOAD IN PICKLE FILE AND REWRITE IT
                            
                            """remove now non existent guns from loadouts"""
                            loadoutpath = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', '')    
                            with open(loadoutpath+"userdata", "r") as file:
                                data = pickle.load(file)
                            for loadout in ["LOADOUT 1", "LOADOUT 2", "LOADOUT 3", "LOADOUT 4", "LOADOUT 5"]:
                                if delete == data[loadout][0]:
                                    data[loadout][0] = "M1 GARAND"
                                    
                            with open(loadoutpath+"userdata", "w+") as file:
                                pickle.dump(data, file, protocol=2)
                                
                                """rewrite_file = False
                                with open(loadoutpath, 'r') as file:
                                    if delete in file.read():
                                        rewrite_file = True
                                        num = 0
                                        new = []
                                        file.seek(0)
                                        for lines in file.readlines():
                                            num += 1
                                            if num == 1:
                                                new.append("M1 GARAND")
                                                new.append("\n")
                                            else:
                                                new.append(lines)
                                if rewrite_file:
                                    os.remove(loadoutpath)
                                    with open(loadoutpath, 'w+') as file:
                                        file.write(''.join(new))"""
                    
                    
                    elif create_choice == "DELETE MAP":
                        custom_maps = os.listdir(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', 'Creations', 'Maps'))
                        custom_maps = [s for s in custom_maps if s.endswith('.py')]
                        custom_maps = [maps[:-3] for maps in custom_maps]
                        custom_maps.remove("__init__")
                        custom_maps.append("BACK")
                        delete = Menu(custom_maps).GameSetup()
                        go_back_once = True
                        if delete != "BACK":
                            os.remove(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', 'Creations', 'Maps', '')+delete+".py")
                            try:
                                os.remove(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', 'Creations', 'Maps', '')+delete+".pyc")
                            except OSError:
                                pass
            
            if choice == "OPTIONS":
                while True:
                    option_choice = Menu(["FULLSCREEN", "WINDOWED", "GAME OPTIONS", "BACK"]).GameSetup("", "", "", "", "PLAY TO CUSTOM KILLS/DEATHS FOR YOUR GAME")
                    if option_choice == "GAME OPTIONS":
                        while True:
                            self.max_kills = Menu([]).name(True, "MAX K/Ds:", True)
                            try:
                                self.max_kills = int(self.max_kills)
                                break
                            except:
                                pass
                    elif option_choice == "FULLSCREEN": 
                        pygame.display.set_mode((640,480), pygame.FULLSCREEN)
                    elif option_choice == "WINDOWED":
                        pygame.display.set_mode((640,480))
                    else:
                        break
            
            if choice == "LOADOUTS":
                while True:
                    if not go_back_once:
                        loadout_number = Loadouts(True).display_loadout()
                    if loadout_number == "BACK":
                        break
                    else:    
                        loadoutchoice = Menu(["WEAPON", "PERK 1", "PERK 2", "PERK 3", "BACK"]).GameSetup()
                    if loadoutchoice == "WEAPON":
                        while True:
                            weapon_type = Menu(["RIFLES", "SMGs", "LMGs", "SNIPERS", "CUSTOM", "BACK"]).GameSetup()                    
                            if weapon_type == "RIFLES":                    
                                weapon = Menu(["M1 GARAND", "GEWEHR 43", "M1A1", "FG42", "STG44", "BACK"]).GameSetup("rank", [1, 5, 10, 16, 18], "SEMI-AUTO, HIGHEST DAMAGE ASSAULT RIFLE", "SEMI-AUTO, MODERATE POWER", "SEMI-AUTO, SHORT DELAY BETWEEN SHOTS", "FULL-AUTO, HIGH FIRERATE", "FULL-AUTO, HIGH POWER")
                            elif weapon_type == "SMGs":
                                weapon = Menu(["THOMPSON", "MP40", "M3", "OWEN GUN", "PPSH41", "BACK"]).GameSetup("rank", [1, 5, 11, 15, 20], "FULL-AUTO, VERY HIGH FIRERATE", "FULL-AUTO, BALANCE BETWEEN POWER AND FIRERATE", "FULL-AUTO, HIGH POWER", "FULL-AUTO, MODERATE FIRERATE", "FULL-AUTO, FASTEST FIRING WEAPON IN WAR")
                            elif weapon_type == "LMGs":
                                weapon = Menu(["M1919", "BAR", "TYPE 99", "BACK"]).GameSetup("rank", [1, 5, 13], "FULL-AUTO, 250 ROUND MAG", "FULL-AUTO, MODERATE FIRERATE", "FULL-AUTO, BALANCE BETWEEN POWER AND FIRERATE")
                            elif weapon_type == "SNIPERS":
                                weapon = Menu(["SVT40", "MOSIN NAGANT", "ARIASKA", "SPRINGFIELD", "BACK"]).GameSetup("rank", [1, 6, 7, 12], "BOLT ACTION", "BOLT ACTION", "BOLT ACTION", "BOLT ACTION")
                            elif weapon_type == "CUSTOM":
                                custom_guns = os.listdir(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Data', 'Creations', 'Guns'))
                                custom_guns = [s for s in custom_guns if s.endswith('.py')]
                                custom_guns = [guns[:-3] for guns in custom_guns]
                                custom_guns.remove("__init__")
                                custom_guns.append("BACK")
                                weapon = Menu(custom_guns).GameSetup()
                            
                            
                            
                            elif weapon_type == "BACK":
                                break
                                
                            """writing our weapon choice to file"""
                            if weapon != "BACK":
                                self.update_data(0, loadout_number, weapon)
                            go_back_once = True
                            del(weapon)
                    elif loadoutchoice == "PERK 1":
                        perk1 = Menu(["RATIONS", "QUICK HANDS", "RAPID FIRE", "BACK"]).GameSetup("rank", [1, 3, 6], "MOVE FASTER", "RELOAD FASTER", "FIRE RATE INCREASED BY 50%")
                
                        if perk1 != "BACK":
                            self.update_data(1, loadout_number, perk1)
                        go_back_once = True                       
                
                        del(perk1)
                     
                    elif loadoutchoice == "PERK 2":
                        perk2 = Menu(["HOLLOW POINTS", "SELECT FIRE", "EXT MAGS", "BACK"]).GameSetup("rank", [1, 5, 9], "HIGHER DAMAGE", "SEMI-AUTO GUNS ARE FULL-AUTO", "50% MORE AMMO")
                
                        if perk2 != "BACK":
                            self.update_data(2, loadout_number, perk2)
                        go_back_once = True                       
                
                        del(perk2)
                                          
                    elif loadoutchoice == "PERK 3":
                        perk3 = Menu(["MEDIC", "ALPHA MALE", "DISTRACTION", "BACK"]).GameSetup("rank", [1, 5, 11], "MORE HEALTH", "ENEMIES MOVE SLOWER TOWARDS YOU", "ENEMIES ARE LESS ACCURATE")
                
                        if perk3 != "BACK":
                            self.update_data(3, loadout_number, perk3)
                        go_back_once = True
                
                        del(perk3)
                    elif loadoutchoice == "BACK":
                        go_back_once = False
                                     
            elif choice == "ONLINE GAME":
                if not self.online_check():
                    self.online = False
                    screen.blit(self.background, (0, 0))
                    text = self.font["medium"].render("NO CONNECTION",1,(255,0,0))
                    screen.blit(text, (180, 150))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    continue
                else:
                    self.online = True
                    return
            elif choice == "OFFLINE GAME":
                try:
                    self.map_choice
                    return
                except:
                    font = pygame.font.SysFont("monospace", 25)
                    text = font.render("NO MAP SELECTED",1,(255,0,0))
                    screen.blit(text, (25, 300))
                    pygame.display.flip()
                    pygame.time.delay(2000) 
    
    def online_check(self):
        try:
            import urllib.request
            return True #python 3 embedded zip won't let me actually check
        except ImportError: #python 2
            import urllib
            
        screen.blit(self.background, (0, 0))
        text = self.font["smallish"].render("CHECKING INTERNET CONNECTION...",1,(255,255,255))
        screen.blit(text, (140, 150))
        pygame.display.flip()
        try:
            urllib.urlopen("https://www.google.com")
            return True
        except:
            return False
                
    def guns(self, loadout_number, angle=None):  
        """self.weapon = open(path+loadout_number, 'r').readlines()[0].rstrip()
        #open(path+loadout_number, 'r').close()"""
        with open(path+"userdata", "r") as file:
            data = pickle.load(file)
            
        try:
            loadout = data[str(loadout_number)]
            self.weapon = loadout[0]
        except: #enemy option
            self.weapon = loadout_number
        if self.weapon == "M1 GARAND":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().m_one_garand(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().m_one_garand(angle)
                return
        elif self.weapon == "MP40":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().mp40(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().mp40(angle)
                return
        elif self.weapon == "THOMPSON":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().thompson(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().thompson(angle)
                return
        elif self.weapon == "STG44":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().stg(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().stg(angle)
                return
        elif self.weapon == "M1A1":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().m_one_a_one(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().m_one_a_one(angle)
                return
        elif self.weapon == "FG42":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().fg_forty_two(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().fg_forty_two(angle)
                return
        elif self.weapon == "PPSH41":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().ppsh(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().ppsh(angle)
                return
        elif self.weapon == "GEWEHR 43":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().gewehr_forty_three(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().gewehr_forty_three(angle)
                return  
        elif self.weapon == "M3":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().m_three(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().m_three(angle)
                return
        elif self.weapon == "OWEN GUN":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().owen(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().owen(angle)
                return
        elif self.weapon == "M1919":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().m_nineteen_nineteen(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().m_nineteen_nineteen(angle)
                return
        elif self.weapon == "BAR":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().bar(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().bar(angle)
                return
        elif self.weapon == "TYPE 99":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().type_ninety_nine(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().type_ninety_nine(angle)
                return
        elif self.weapon == "SVT40":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().svt_forty(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().svt_forty(angle)
                return
        elif self.weapon == "MOSIN NAGANT":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().mosin_nagant(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().mosin_nagant(angle)
                return
        elif self.weapon == "ARIASKA":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().ariaska(angle)
            except (TypeError, ValueError):
                self.gun = Gun_Types().ariaska(angle)
                return
        elif self.weapon == "SPRINGFIELD":
            try:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Gun_Types().springfield(angle)
            except ((TypeError, ValueError), ValueError):
                self.gun = Gun_Types().springfield(angle)
                return
        else: #custom gun
            if angle == None:
                self.firerate, self.action, self.stk, self.mag, self.reloadtime, self.recoil = Custom_Gun(self.weapon).return_gun()
            else:
                self.gun = Custom_Gun(self.weapon).blit_gun(angle)
                return
                
        """perk1 = open(path+loadout_number, 'r').readlines()[1].rstrip() """
        perk1 = loadout[1]   
        if perk1 == "QUICK HANDS":
            self.reloadtime *= 0.75
        elif perk1 == "RAPID FIRE":
            if self.firerate > 1:
                self.firerate = int(self.firerate * 0.5)
    
        """perk2 = open(path+loadout_number, 'r').readlines()[2].rstrip() """
        perk2 = loadout[2]   
        if perk2 == "HOLLOW POINTS":
            self.stk *= 0.75
        elif perk2 == "SELECT FIRE":
            if self.stk > 5:
                if self.action == "semi-auto":
                    self.action = "full-auto"
                    self.firerate = 15
                else:
                    self.action = "semi-auto"
                    self.firerate = 1
        elif perk2 == "EXT MAGS":
            self.mag = int(self.mag * 1.5)    
    
    def perks(self, loadout_number):
        with open(path+"userdata", "r") as file:
            data = pickle.load(file)
        loadout = data[str(loadout_number)]
        """perk1 = open(path+loadout_number, 'r').readlines()[1].rstrip()"""
        perk1 = loadout[1]
        if perk1 == "RATIONS":
            self.rations = True
        else: 
            self.rations = False
   
        """perk3 = open(path+loadout_number, 'r').readlines()[3].rstrip()"""
        perk3 = loadout[3]    
        if perk3 == "MEDIC":
            self.medic = True
        else:
            self.medic = False
        if perk3 == "ALPHA MALE":
            self.alpha = True
        else:
            self.alpha = False
        if perk3 == "DISTRACTION":
            self.distraction = True
        else:
            self.distraction = False
            
    def pause(self, setup):
        while True:
            pause = Menu(["RESUME", "LOADOUTS     UPDATES AT NEXT SPAWN", "OPTIONS", "END GAME"]).GameSetup()
            if pause == "RESUME":
                try:
                    return new_setup
                except:
                    return None
            elif pause == "LOADOUTS     UPDATES AT NEXT SPAWN":
                loadout_number = Loadouts(True).display_loadout()                    
                if loadout_number != "BACK":
                    new_setup = Setup()
                    new_setup.guns(loadout_number)
                    new_setup.guns(loadout_number, 0)
                    new_setup.perks(loadout_number)
                    new_setup.map_choice = setup.map_choice
                    new_setup.loadout_number = loadout_number
            elif pause == "OPTIONS":
                while True:
                    option_choice = Menu(["FULLSCREEN", "WINDOWED", "BACK"]).GameSetup()
                    if option_choice == "FULLSCREEN": 
                        pygame.display.set_mode((640,480), pygame.FULLSCREEN)
                    elif option_choice == "WINDOWED":
                        pygame.display.set_mode((640,480))
                    else:
                        break
            elif pause == "END GAME":
                return "end"          
