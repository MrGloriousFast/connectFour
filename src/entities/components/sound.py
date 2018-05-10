from entities.components.component_base import Component_Base
import pygame

class Sound(Component_Base):
    def __init__(self, sound):

        super().__init__('bla')

        self.sound = sound