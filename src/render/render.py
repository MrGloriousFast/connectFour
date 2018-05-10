import pygame
import datetime
import data.globals as glo
import numpy as np

class Renderer:

    def __init__(self):

        self.surface = pygame.display.set_mode((glo.window_x, glo.window_y))#,pygame.FULLSCREEN)

        pygame.display.set_caption(glo.caption)

    def clear(self):
        self.surface.fill(glo.BGCOLOR)

    def screenShot(self):
        now = datetime.datetime.today()
        pygame.image.save(self.surface,
                          "Screenshots/" + str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "-" + str(
                              now.hour) + "-" + str(now.minute) + "-" + str(now.second) + ".png")
        print(" ")
        print("Screenshot taken! ")
        print(str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "-" + str(now.hour) + "-" + str(
            now.minute) + "-" + str(now.second) + ".png")


    def drawImage(self,image, xx, yy):

        #check if in screen
        if(xx<glo.window_x and xx >0.0):
            if yy < glo.window_y and yy>0.0:
                (xsize, ysize) = image.get_size()
                #print('in painter', xx,yy)
                self.surface.blit(image, (int(xx - xsize / 2), int(yy - ysize / 2)))

    def drawWorld(self, map):
        rekt = pygame.Rect(0,0,map.scale,map.scale)
        for index, x in np.ndenumerate(map.grid):

            if map.get(index[0],index[1])==1:

                if map.scale >1:
                    rekt.x = index[0]*map.scale #move(*index)
                    rekt.y = index[1]*map.scale

                    pygame.draw.rect(self.surface, glo.WHITE, rekt)

                else:
                    #pygame.draw.gfxdraw.pixel(self.surface, index[0], index[1], glo.WHITE)
                    self.surface.set_at(index, glo.WHITE)

    def draw_connect_four(self, gamefield):

        #height
        circle_height = glo.window_y / gamefield.colomns

        #width
        circle_width = glo.window_x / gamefield.rows

        glo.BGCOLOR = glo.BLACK

        for x in range(0, gamefield.rows):
            for y in range(0, gamefield.colomns):
                rekt = pygame.Rect(x*circle_width,y*circle_height,circle_width,circle_height)
                color = glo.DARKGRAY #empty places
                if gamefield.field[x,y] == 0:
                    color = glo.DARKRED
                elif gamefield.field[x,y] == 1:
                    color = glo.DARKBLUE

                pygame.draw.ellipse(self.surface, color, rekt)

    #draw text at a position
    def drawText(self, x, y, text, color=glo.WHITE):
        textSurfaceObj = glo.font.render(text, False, color)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topleft = (x, y)
        self.surface.blit(textSurfaceObj, textRectObj)

    def flip(self):
        pygame.display.update()


