import os, shutil
from zipfile import *
import time, pygame, sys, stat
      
try:
    import urllib.request as urllib #python 3
except:
    import urllib

def rm_dir(path_to_file):
    if os.name == "nt":
        for root, dirs, files in os.walk(path_to_file):
            for d in dirs:
                os.chmod(os.path.join(root,d),stat.S_IWUSR)
            for f in files:
                os.chmod(os.path.join(root,f),stat.S_IWUSR)
    shutil.rmtree(path_to_file)

def update(build):
    files = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'file.zip')
    path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), '')
    
    if __name__ != "__main__":
        screen =  pygame.display.set_mode((640,480))
        text = pygame.font.SysFont("monospace", 35).render("PLEASE WAIT, CHECKING",1,(255,255,255))
        screen.blit(text, (110, 150))
        text = pygame.font.SysFont("monospace", 35).render("FOR UPDATE...",1,(255,255,255))
        screen.blit(text, (200, 200))
        
        pygame.display.flip()
        
        try:
            urllib.urlretrieve('https://github.com/srfjr18/WWII-base/archive/master.zip', files)
            embed = False
            if os.name == "nt":
                embed = True
        except AttributeError:
            embed = True
            os.system("powershell.exe [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; curl https://github.com/srfjr18/WWII-base/archive/master.zip -O "+str(files)) #to fix annoying encoding problem with embedded zip
        except:
            return "no connection"
        zip = ZipFile(files)
        zip.extractall(path)
        zip.close()
    
    
        with open(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master', 'Resources', 'scripts', 'Menus.py')) as check:
                if build in check.read():
                     do_stuff = True
                else:
                    do_stuff = False
            
        if do_stuff:
            rm_dir(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master'))
            os.remove(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'file.zip'))
            return "up to date"
        else:
            from Resources.scripts.Menus import Menu
            yn = Menu([]).yes_no("   AN UPDATE IS", " AVAILIBLE. CONTINUE?")  
            if yn == "no":
                rm_dir(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master'))
                os.remove(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'file.zip'))
                return yn    
                
        if embed:
            os.system(path+"python.exe "+os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Resources', 'scripts', 'Updater.py'))   
            pygame.quit()
            sys.exit()         
    try:
        shutil.copytree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Resources', 'sounds'), path+'sounds')
        shutil.copytree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Resources', 'images'), path+'images')
    except:
        pass
    
    rm_dir(path+'Resources')
    shutil.copytree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master', 'Resources'), path+'Resources')
    shutil.copy2(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master', 'game.py'), path+'game.py')
    
    shutil.copytree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'images'), os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Resources', 'images'))
    shutil.copytree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'sounds'), os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Resources', 'sounds'))
    
    rm_dir(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master'))
    rm_dir(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'images'))
    rm_dir(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'sounds'))
    os.remove(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'file.zip'))
    
if __name__ == "__main__":
    time.sleep(2)
    update("fake")
    pygame.init()
    screen =  pygame.display.set_mode((640,480))
    font = {"big": pygame.font.SysFont("monospace", 50), "medium": pygame.font.SysFont("monospace", 35), "small": pygame.font.SysFont("monospace", 25), "smallish": pygame.font.SysFont("monospace", 20), "extrasmall": pygame.font.SysFont("monospace", 15)}
    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))
    background = background.convert()    
    pygame.time.delay(300)    
    while True:
        screen.blit(background, (0, 0))
        text = font["medium"].render("GAME RESTART REQUIRED",1,(255,255,255))
        screen.blit(text, (130, 150))
        
        
        text = font["small"].render("YOU MAY NEED TO APPLY PERMISSIONS (CHMOD)",1,(255,255,255))
        screen.blit(text, (17, 250))
        
        text = font["small"].render("DEPENDING ON YOUR OS",1,(255,255,255))
        screen.blit(text, (200, 280))
        
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
    sys.exit() 
