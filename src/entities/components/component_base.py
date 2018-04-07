#every component should have only pure data fields

#logic should be at a minimum and you should think three times before adding any actual logic
#no update methods here!

class Component_Base():
    def __init__(self, name = 'base'):
        self.name = name #should be three letters unique description
        #self.id = 0

