"""
helper.py

Source Code from Luke Arntson (cthulhu32) 
    arcade game "Death Tower" from pyweek.org 
    (https://pyweek.org/e/Cthulhu32_v2/)

Adapted from Python2 to Python3

loads images, sounds

*supplements the data file
"""

import os, pygame
from pygame.locals import *

#functions to create our resources
def load_image(name, colorkey=None):
    """ Load image and return image object"""
    fullname = os.path.join('images')
    fullname = os.path.join(fullname, name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except(pygame.error):
        print('Cannot load image:', fullname)
        return None
    return image, image.get_rect()    


def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    try:
        sound = pygame.mixer.Sound(os.path.join('audio', name))
    except(pygame.error):
        print('Cannot load sound:', name)
    return sound


def load_music(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return
    try:
        pygame.mixer.music.load(os.path.join('audio', name))
        
    except(pygame.error):
        print('Cannot load music:', name)
    return
