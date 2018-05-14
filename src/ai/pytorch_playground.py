import random

import copy
import torch as pt
import torch.nn as nn
import torch.nn.functional as F

import numpy as np

from ai.bot_base import BotBase


class TorchBot(BotBase, nn.Module):
    def __init__(self):

        super(BotBase, self).__init__()
        super(TorchBot, self).__init__()
        self.name = "torchBot"

        # convolution layer so we can detect patterns
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=3, kernel_size=2, stride=1, groups=1)
        self.conv2 = nn.Conv2d(in_channels=3, out_channels=1, kernel_size=2, stride=1, groups=1)

        # gamefield input -> hiddenlayer
        self.fc1 = nn.Linear(5*4, 10)

        # hidden layer -> output
        self.fc2 = nn.Linear(10, 7)

    def choose_action(self, gamefield, action_list, player_color):

        sensors = self.one_hot(gamefield, player_color)
        # sensors = self.prepare_input(gamefield, player_color)

        actors = self.forward(sensors)
        actors = list(actors)
        choice = actors.index(max(actors))

        return choice

    def forward(self, x):

        # due to batch size we have do this
        x = pt.unsqueeze(x, 0)
        #x = pt.unsqueeze(x, 0)


        x = F.relu(self.conv1(x))


        x = F.relu(self.conv2(x))


        # flatten the tensor so we can put our fc onto it
        x = x.view(-1)

        x = self.fc1(x)


        x = self.fc2(x)


        x = F.softmax(x, dim=0)


        return x

    def one_hot(self, input_numpy_2d_array, player_color):
        # the values we will encounter in the input
        # for each one of them we will have to create a one hot encoding
        classes = [-1.0, 0.0, 1.0]

        if player_color == 1:
            classes = [-1.0, 1.0, 0.0]

        # get the input dimensions
        dim_x = input_numpy_2d_array.shape[0]
        dim_y = input_numpy_2d_array.shape[1]

        # create a tensor big enough to fit all data
        hot_tensor = pt.zeros([len(classes), dim_x, dim_y], dtype=pt.float32)

        # fill the tensor with our values
        for x in range(0, dim_x):
            for y in range(0, dim_y):
                value = input_numpy_2d_array[x][y]
                for c in range(0, len(classes)):
                    if value == classes[c]:
                        hot_tensor[c][x][y] = 1.0

        return hot_tensor

    def mutate(self):

        mutation_step = 10.0

        for f in self.parameters():
            # x percent chance to change a weight
            if random.randint(0, 100) < 1:
                f.data.sub_(random.uniform(-mutation_step, mutation_step))

    def get_clone(self):
        return copy.deepcopy(self)

