import random


class BotBase():
    def __init__(self):
        self.name = 'default bot'

    def choose_action(self, gamefield, action_list, player_color):
        return random.choice(action_list)