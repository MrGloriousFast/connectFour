import pygame
import datetime
import src.data.globals as glo

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


    #draw text at a position
    def drawText(self, x, y, text, color=glo.WHITE):
        textSurfaceObj = glo.font.render(text, False, color)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topleft = (x, y)
        self.surface.blit(textSurfaceObj, textRectObj)

    def flip(self):
        pygame.display.update()


