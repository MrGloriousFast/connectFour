import os
import sys
import pygame
from pygame.locals import *


if not pygame.font: print("Warning, fonts disabled")
if not pygame.mixer: print("Warning, sound disabled")






def load_image(file, colorkey=False):
    #file = os.path.join('data', file)
    try:
        image = pygame.image.load(file)
        colorkey = image.get_at((0, 0))
        if colorkey is True:
            image.set_colorkey(colorkey, pygame.RLEACCEL)
    except:
        print("Unable to load: ", file)
        image = None
    return image