import os, shutil
from zipfile import *
import urllib

def update(build):
    files = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'file.zip')
    path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), '')
    try:
        urllib.urlretrieve('https://github.com/srfjr18/WWII-base/archive/master.zip', files)
    except LookupError:
        os.system("C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe" ["curl https://github.com/srfjr18/WWII-base/archive/master.zip -0 "+ files]) #to fix annoying encoding problem with embedded zip
    zip = ZipFile(files)
    zip.extractall(path)
    
    
    with open(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master', 'Resources', 'scripts', 'Menus.py')) as check:
            if build in check.read():
                shutil.rmtree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master'))
                os.remove(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'file.zip'))
                return "up to date"
    
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
