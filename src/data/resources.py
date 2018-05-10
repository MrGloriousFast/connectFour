

from data.loader import load_image

'''

Singelton that stores all of our images
'''

class Atlas_images:
    #singleton pattern with one instance
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Atlas_images.__instance == None:
            Atlas_images()
        return Atlas_images.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Atlas_images.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            #set the instance variable to this new created 'self'
            Atlas_images.__instance = self

            #load an image
            self.img_dino = load_image('../art/dinos/dino_2r.png')


