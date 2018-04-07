import os
import sys
import pygame
from pygame.locals import *


if not pygame.font: print("Warning, fonts disabled")
if not pygame.mixer: print("Warning, sound disabled")

def load_image(file):
    image = pygame.image.load(file)
    image.set_colorkey(image.get_at((0, 0)))

    transColor = pygame.Color(255, 0, 255)
    image = pygame.image.load(file)
    image.set_colorkey(transColor)

    '''
    
    try:
        image = pygame.image.load(file)
        image.set_colorkey(image.get_at((0, 0)))

    except:
        print("Unable to load: ", file)
        image = None
    '''
    return image