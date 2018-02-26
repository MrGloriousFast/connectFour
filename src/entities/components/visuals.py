from src.entities.components.component_base import Component_Base
from src.data.loader import load_image
import pygame

#for now we will not do any animation only one image per entity to keep it simple
class Image(Component_Base):
    def __init__(self, imagePath):

        super().__init__('img')

        self.image = load_image(imagePath)