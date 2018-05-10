# import components
from data.resources import Atlas_images
from entities.components.position import *
from entities.components.visuals import Image

# import the Agent base class
from entities.agents.entity_base import Agent_Base


class Bot(Agent_Base):
    def __init__(self, px, py):
        # create the base
        super().__init__()

        #give a position
        p = Position(px,py)
        self.add_component(p)

        #an image
        i = Image(Atlas_images.getInstance().img_dino)
        self.add_component(i)

        #ability to move around
        m = Move()
        self.add_component(m)
