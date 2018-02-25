import urllib, os, shutil 
from zipfile import *

def update(build):
    files = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'file.zip')
    path = os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), '')
    urllib.urlretrieve('https://github.com/srfjr18/WWII-base/archive/master.zip', files)
    zip = ZipFile(files)
    zip.extractall(path)
    
    
    with open os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master', 'Resources', 'Menus.py') as check:
            if build in check.read()
                return "up to date"
    

    shutil.rmtree(path+'Resources')
    shutil.copytree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master', 'Resources') path)
    shutil.copy2(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master', 'game.py') path)
    
    shutil.rmtree(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'WWII-base-master'))
    os.remove(os.path.join(os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-2]), 'file.zip'))
