
from ai.NeuroNet import Brain
from random import randint,uniform
import copy



class Mutant(Brain):
    def __init__(self, nodearray):
        super().__init__(nodearray)
        self.mutationStep = uniform(0.01, 10.0)


    def mutate(self):
        # pick random weight and change it
        s = self.mutationStep

        l = randint(0, len(self.weights) - 1)
        x = randint(0, 100000000) % self.weights[l].shape[0]
        y = randint(0, 100000000) % self.weights[l].shape[1]

        # in 49% increase the weight
        # in 49% decrese the weight
        # in 2% set the weight to 0
        r = randint(0, 100)
        if r < 49:

            self.weights[l][x][y] += s

        elif r < 98:
            self.weights[l][x][y] -= s
        else:
            self.weights[l][x][y] = 0.0

        max_weight = 100.0
        min_weight = -max_weight

        self.weights[l][x][y] = max(min_weight, self.weights[l][x][y])
        self.weights[l][x][y] = min(max_weight, self.weights[l][x][y])


    def makeChild(self, s=None):
        if s == None:
            s = uniform(0.0, 2.0 * self.mutationStep) + uniform(0.0, 0.001)
            # s=uniform(0.0,3.0)
        child = copy.deepcopy(self)
        child.mutationStep = s

        child.mutate()
        return child
