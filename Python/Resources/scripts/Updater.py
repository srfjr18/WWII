import os, shutil
from zipfile import *
import urllib, time, pygame

def update(build):
    files = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'file.zip')
    path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), '')
    
    if __name__ != "__main__":
        try:
            urllib.urlretrieve('https://github.com/srfjr18/WWII-base/archive/master.zip', files)
            embed = False
        except AttributeError:
            embed = True
            os.system("powershell.exe [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; curl https://github.com/srfjr18/WWII-base/archive/master.zip -O "+str(files)) #to fix annoying encoding problem with embedded zip
        except:
            return "no connection"
        zip = ZipFile(files)
        zip.extractall(path)
    
    
        with open(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master', 'Resources', 'scripts', 'Menus.py')) as check:
                if build in check.read():
                    shutil.rmtree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master'))
                    os.remove(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'file.zip'))
                    return "up to date"
                
                
        if embed:
            os.system(path+"python.exe "+os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Resources', 'scripts', 'Updater.py'))   
            sys.exit()         
    
    shutil.copytree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Resources', 'sounds'), path+'sounds')
    shutil.copytree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Resources', 'images'), path+'images')
    
    shutil.rmtree(path+'Resources')
    shutil.copytree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master', 'Resources'), path+'Resources')
    shutil.copy2(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master', 'game.py'), path+'game.py')
    
    shutil.copytree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'images'), os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Resources', 'images'))
    shutil.copytree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'sounds'), os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'Resources', 'sounds'))
    
    shutil.rmtree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master'))
    shutil.rmtree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'images'))
    shutil.rmtree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'sounds'))
    os.remove(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'file.zip'))
    
if __name__ == "__main__":
    time.sleep(2)
    updater("fake")
    pygame.init()
    screen =  pygame.display.set_mode((640,480))
    pygame.time.delay(300)    
    while True:
        screen.blit(self.background, (0, 0))
        text = self.font["medium"].render("GAME RESTART REQUIRED",1,(255,255,255))
        screen.blit(text, (130, 150))
        text = self.font["extrasmall"].render("Depending on your OS, you may need to give proper permissions to the updated game.py file",1,(255,255,255))
        screen.blit(text, (10, 200))
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
