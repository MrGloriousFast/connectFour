from ai.bot_base import BotBase
import numpy as np
from pprint import pprint
from random import randint, uniform
import math


class Brain(BotBase):

    def __init__(self, nodearray):
        super().__init__()

        self.structure = nodearray
        self.Layers = []
        for h in range(0, len(nodearray) - 1):
            # define the layer with the bias
            layer = np.zeros(nodearray[h] + 1, dtype=float)  # +1 for the bias node!
            layer[-1] = 1.0  # set the bias to 1.0
            self.Layers.append(layer)

        # output does not need a bias
        self.Layers.append(np.zeros(nodearray[-1], dtype=float))
        self._createWeights()

    def choose_action(self, field, action_list, player_num):

        input = []

        #a random input node
        input.append(uniform(-1.0, 1.0))

        #apply the gamefield
        for x in range(0, 7):
            for y in range(0, 6):
                if field[x, y] == -1:
                    input.append(0.0)
                elif field[x, y] == player_num:
                    input.append(1.0)
                else:#if field[x, y] == 1:
                    input.append(0.5)


        #print(input)
        output = self.propagate(np.array(input))
        output *= 7.0

        decision = 0
        if output < 1.0:
            decision = 0
        elif output < 2.0:
            decision = 1
        elif output < 3.0:
            decision = 2
        elif output < 4.0:
            decision = 3
        elif output < 5.0:
            decision = 4
        elif output < 6.0:
            decision = 5
        else:
            decision = 6

        if len(action_list)==0:
            return 0

        #if we want to make an illegal move
        #if not decision in action_list:
        #    return super().choose_action(field, action_list)


        return decision


    def _createWeights(self):

        # basically just create the weights between the layers
        # set every weight to random values
        self.weights = []
        for L in range(0, len(self.Layers) - 2):

            # don't connect the bias to the layer before it

            self.weights.append(self._weights_matrix(self.Layers[L].size, self.Layers[L + 1].size - 1))

        # last layer is our output layer and there is no bias node so we can connect everyone to each other
        self.weights.append(self._weights_matrix(self.Layers[-2].size, self.Layers[-1].size))


    def _weights_matrix(self, a, b):
        f = 4.0

        m = np.random.rand(a, b)

        for x in range(0, a):
            for y in range(0, b):
                if randint(0,100)<90:
                    m[x,y] = uniform(-f, f)
                else:
                    m[x, y] = 0.0
        return m


    # returns True if applying the input worked!
    def _setArray(self, resArray, inArray):
        if resArray.size - 1 < inArray.size:
            print('ERROR input size too big!\n'
                  + 'inLayer ' + str(inArray) + '\n'
                  + 'input ' + str(resArray) + '\n'
                  )
            return False
        else:
            # set all layer to zeros
            for i in range(resArray.size):
                resArray[i] = 0.0
            # fill the layer with the new input
            for i in range(inArray.size):
                resArray[i] = inArray[i]
            return True

    def propagate(self, inArray):
        # if applying the input failed return
        if not self._setArray(self.Layers[0], inArray):
            return

        # propagate the input through all layers to the output
        for L in range(0, len(self.Layers) - 1):
            rangeout = self.Layers[L + 1].size - 1  # -1 due to bias, we dont write into that one
            # if we are at the output layer ew have no bias that we need to ignore
            if L == len(self.Layers) - 2:
                rangeout += 1
            for nodeOut in range(0, rangeout):
                summ = 0.0
                for nodeIn in range(self.Layers[L].size):
                    summ += self.Layers[L][nodeIn] * self.weights[L][nodeIn][nodeOut]
                self.Layers[L + 1][nodeOut] = self._activation(summ)
        return self.Layers[-1]

    def _activation(self, x):
        return self.sigmoid(x)

    def parabel(self, x):
        return math.copysign(x * x, x)

    def expo(self, x):
        return math.sqrt(abs(x))

    def polynom(self, x):
        a = 1.0
        b = 1.0
        c = 1.0
        return a * (x * x) + b * x + c

    def log(self, x):
        return math.log(2.0, x + 1.0)

    def rectangle(self, x):
        if x > 0:
            return 1.0
        else:
            return -1.0

    def sinus(self, x):
        return math.sin(math.pi * x)

    def sigmoid(self, x, derivative=False):
        if (derivative == True):
            return x * (1.0 - x)
        return 1.0 / (1.0 + np.exp(-x))

    def linear(self, x):
        #return x
        if x < 0:
            return x*0.01
        else:
            return x

    def printIt(self):
        print('structure ', self.structure)
        # print('input  ', *self.input)
        # for L in range(len(self.Layers)):
        # print('w'+str(L), self.weights[L].size)
        # print('h'+str(L), self.Layers[L].size)
        # print('w', self.weights[-1].size)
        # print('output ', *self.output)
        pprint(vars(self))
        '''
        result = ''
        result += 'sizeIn '+ str(self.sizeIn) + '\n'
        result += 'sizeOut '+ str(self.sizeOut) + '\n'
        result += 'input:\n'+str(self.input)+'\n'
        result += 'output:\n'+str(self.output)+'\n'
        return result
        '''


