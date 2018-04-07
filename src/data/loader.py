import os
import sys
import pygame
from pygame.locals import *


if not pygame.font: print("Warning, fonts disabled")
if not pygame.mixer: print("Warning, sound disabled")

def load_image(file):
    #colorkey
    #this color will be invisible
    transColor = pygame.Color(200, 0, 200)

    #load the image
    #video mode has to be set before calling this line
    #video is set in the render.py file, the main or the game class have to set it
    image = pygame.image.load(file).convert()

    #after loading we make the transcolor invisible
    image.set_colorkey(transColor)

    return image