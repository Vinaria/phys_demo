from tkinter import *
from tkinter import messagebox
import pyscreenshot


def screenshot(name='photo'):
    shot = pyscreenshot.grab()
    dist = 'screenshots'
    shot.save(dist + '/' + name + '.png')
    Tk().wm_withdraw()  # to hide the main window
    messagebox.showinfo('Screenshot info', 'Снимок экрана был сохранен в папке ' + dist)
