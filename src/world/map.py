import numpy as np

class Map:
    def __init__(self):
        self.dim_x = 100
        self.dim_y = 100
        self.scale = 8 #one map square equals X pixels

        #where the map data is stored
        self.grid = np.random.randint(2, (self.dim_x, self.dim_y), dtype='int') #np.array((self.dim_x, self.dim_y), dtype='int')

    def get(self,x,y):
        #check if its inside
        if(x>0 and y>0 and x<self.dim_x and y<self.dim_y):
            return self.grid[x, y]
        else:
            return 0

    def set(self, x, y, value):
        #check if its inside
        if(x>0 and y>0 and x<self.dim_x and y<self.dim_y):
            self.grid[x, y] = value
        else:
            print('trying to assign out of bounds', x, y, self.dim_x, self.dim_y, value)

