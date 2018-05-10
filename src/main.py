# -*- coding: cp1252 -*-
# Neurotic
# By Artur Fast SchirmCharmeMelone@gmail.com
# Februar 2018

#use pygame because some other imports assume that pygame is already initialized!
import pygame,sys
pygame.init()

from game import Game
from connectFour import ConnectFour

#our main is very simple and uses the game class to run a game
game = ConnectFour()
game.start()