import pygame

FPS = 100
window_y = 720
window_x = 1280
caption = 'Neurotic'

font = pygame.font.Font('freesansbold.ttf', 16)

deltaT = 0
frame_counter = 0

#set up the colors
#            R    G    B
GRAY     = (100, 100, 100)
DARKGRAY = ( 10,  10,  10)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
DARKRED  = (155,   0,   0)
GREEN    = (  0, 255,   0)
DARKGREEN= (  0, 155,   0)
BLUE     = (  0,   0, 255)
DARKBLUE = (  0,   0, 155)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
BGCOLOR = BLACK