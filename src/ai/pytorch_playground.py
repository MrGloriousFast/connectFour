import random

import copy
import torch
import torch.nn as nn
import torch.nn.functional as F

import numpy as np

from ai.bot_base import BotBase


class TorchBot(BotBase, nn.Module):
    def __init__(self):

        super(BotBase, self).__init__()
        super(TorchBot, self).__init__()
        self.name = "torchBot"

        # gamefield input -> hiddenlayer
        self.fc1 = nn.Linear(6*7*2, 20)

        # hidden layer -> output
        self.fc2 = nn.Linear(20, 7)

    def choose_action(self, gamefield, action_list, player_color):
        sensors = self.prepare_input(gamefield, player_color)

        actors = self.forward(sensors)
        actors = list(actors)
        choice = actors.index(max(actors))

        return choice

    def forward(self, i):
        x = torch.Tensor(i)
        x = self.fc1(x)
        x = self.fc2(x)

        x = F.softmax(x, dim=0)

        return x

    def prepare_input(self, field, player_color):

        # gamefield is 2d array and we have to make it into a list
        # brain wants a list as input
        in_list = []

        enemy_color = 0
        if player_color == 0:
            enemy_color = 1

        # apply own stone inputs
        for ii in np.nditer(field):
            if ii == player_color:
                in_list.append(1.0)
            else:
                in_list.append(0.0)

        # apply enemy stone inputs
        for ii in np.nditer(field):
            if ii == enemy_color:
                in_list.append(1.0)
            else:
                in_list.append(0.0)

        return in_list

    def mutate(self):

        mutation_step = 1.0

        for f in self.parameters():
            if random.randint(0,100) < 5:
                f.data.sub_(random.uniform(-mutation_step, mutation_step))

    def get_clone(self):
        return copy.deepcopy(self)

