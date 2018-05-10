from entities.components.component_base import Component_Base
import numpy as np


class Gamefield(Component_Base):

    def __init__(self):
        # 2d array of ints representing the gamefield
        #0 is open/free
        #1 is a stone of player 1
        #2 is a stone of player 2
        self.rows = 7
        self.colomns = 6
        self.win_condition = 4

        temp = []
        for i in range(0, self.rows*self.colomns):
            temp.append(-1)

        self.field = np.array(temp, dtype='int32')
        self.field = self.field.reshape(self.rows, self.colomns)

        self.name = 'field'

    #if one can put a stone in that row or not
    def is_free(self, row):
        if self.field[row, 0] == -1:
            return True
        else:
            return False

    #probably not needed but easier to understand from outside
    def get_stone(self,x,y):
        return self.field[x,y]

    #make sure the stone falls down to the bottom
    def put_stone(self, row, player):
        if self.is_free(row):
            y = self.colomns-1
            while self.field[row, y] != -1:
                y -= 1
            self.field[row, y] = player
        else:
            print('illegal move')

    #get a list of viable actions
    def get_possible_actions(self):
        actions = []
        for i in range(0,self.rows):
            if self.is_free(i):
                actions.append(i)
        return actions

