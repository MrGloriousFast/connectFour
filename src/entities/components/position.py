from src.entities.components.component_base import Component_Base
import pygame, random

#where in the map is the entity
class Position(Component_Base):
    def __init__(self,x=100.0,y=100.0):
        super().__init__('pos')

        self.x = x
        self.y = y
    def get_pos(self):
        return (self.x,self.y)

    def set_pos(self,x,y):
        self.x=x
        self.y=y

#some things have no body but can move! AKA sound, animations
class Move(Component_Base):
    def __init__(self,speedx=0,speedy=0):
        super().__init__('mov')

        self.accl_x = 0.0
        self.accl_y = 0.0

        self.speed_x = speedx
        self.speed_y = speedy



#every collide box has also a position it is actually a position with extra length and height dimensions
class CollideBox(Position):
    def __init__(self, x, y, length, height):
        super.__init__(x,y)
        self.name = 'box'

        self.rect = pygame.Rect(x,y,length,height)