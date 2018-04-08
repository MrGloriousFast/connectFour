import pygame, sys, math, random
import src.data.globals as glo
from data.resources import Atlas_images
from src.render.render import Renderer
from src.gameState import GameState
from src.data.loader import load_image

from src.entities.agents.bot import Bot


#Game class that structures gameflow
#note for refactoring:
    #inherit from this class and outsource the functionality into child classes
class Game():
    def __init__(self):
        # init the base classes as attributes
        self.painter = Renderer() #needs to be called before loading images! Or pygame will not know the video mode and crash
        self.state = GameState()

        self.enemies = []
        for _ in range(0,500):
            x=random.uniform(0, glo.window_x)
            y=random.uniform(0, glo.window_y)
            self.enemies.append(Bot(x,y))


    def start(self):
        self.__init__()
        self.loop()
        print('finished')


    def begin_frame(self):
        pass


    def logic(self):
        collection = self.enemies
        mx, my = pygame.mouse.get_pos()
        self.sys_follow_mouse(collection, mx, my)
        self.sys_move(collection)


    def sys_follow_mouse(self, collection, aimx, aimy):
        for i, e in enumerate(collection):
            px, py = e.comp('pos').get_pos()
            e.comp('mov').accl_x = -0.00001 * (px - aimx)
            e.comp('mov').accl_y = -0.00001 * (py - aimy)


    def sys_move(self, collection):
        # move everyone
        for i, e in enumerate(collection):
            e.comp('mov').speed_x += e.comp('mov').accl_x
            e.comp('mov').speed_y += e.comp('mov').accl_y

            e.comp('pos').x += e.comp('mov').speed_x
            e.comp('pos').y += e.comp('mov').speed_y

    def sys_draw(self, collection):

        # now draw new stuff
        for i, e in enumerate(collection):

            x, y = e.components['pos'].get_pos()
            self.painter.drawImage(e.components['img'].image, x, y)

    def draw(self):
        # empty the screen for new drawings
        self.painter.clear()

        #draw new stuff
        self.sys_draw(self.enemies)

        #draw some debug info on the screen
        if self.state.debug:
            self.painter.drawText(0,  0, "Frames:  " + str(glo.frame_counter))
            self.painter.drawText(0, 20, "Delta_t: " + str(glo.deltaT))

        # Redraw the screen now
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

