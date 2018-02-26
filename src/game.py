import pygame, sys
import src.data.globals as glo
from src.render.render import Renderer
from src.gameState import GameState

from src.entities.agents.bot import Bot

class Game():
    def __init__(self):
        # init the base classes as attributes
        self.painter = Renderer()
        self.state = GameState()

        self.enemies = []
        self.enemies.append(Bot())


    def start(self):
        self.__init__()
        self.loop()
        print('finished')


    def begin_frame(self):
        pass


    def logic(self):
        pass

    def draw(self):
        #first empty the screen
        self.painter.clear()

        #now draw new stuff
        for e in self.enemies:
            self.painter.drawImage(e.components['img'].image, e.components['pos'].x, e.components['pos'].y)

        #draw some debug info on the screen
        if self.state.debug:
            self.painter.drawText(0,  0, "Frames: "  + str(glo.frame_counter))
            self.painter.drawText(0, 20, "Delta_t: " + str(glo.deltaT))

        # Actually redraw the screen
        self.painter.flip()


    def end_frame(self):

        #increment the frame counter
        glo.frame_counter += 1

        #for now we jsut wait a little bit
        #later on we should wait depending on FPS settings
        pygame.time.wait(1)


    #basically user input via mouse or keyboard
    def event_loop(self):
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def loop(self):
        # main gameloop
        #to make the game engine easy we will use one frame for logic AND for rendering
        while True:
            #begin the frame
            self.begin_frame()

            #get user input
            self.event_loop()

            #calculate everything you need
            self.logic()

            #draw everything
            self.draw()

            #end the frame
            self.end_frame()

