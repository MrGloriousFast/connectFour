#import components
from src.entities.components.position import *
from src.entities.components.visuals import Image

#import the Agent base class
from src.entities.agents.entity_base import Agent_Base
import pygame

class Bot(Agent_Base):
    def __init__(self):
        # create the base
        super().__init__()

        #give a position
        self.add_component(Position(500.0, 400.0))

        #an image
        img = Image('../art/dinos/dino_2r.png')
        self.add_component(img)
