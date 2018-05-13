import random

from render.render import Renderer
from game import Game
import pygame, sys, random
import data.globals as glo
from render.render import Renderer
from world.map import Map
from entities.components.gamefield import Gamefield
from entities.agents.bot import Bot
from ai.bot_base import BotBase
from ai.NeuroNet import Brain
from ai.mutant import Mutant
from ai.NEAT.neat_main import NEATBrain
from ai.pytorch_playground import TorchBot

class ConnectFour(Game):
    def __init__(self):
        self.name = 'connect four'

        # init the base classes as attributes
        # needs to be called before loading images! Or pygame will not know the video mode and crash
        self.painter = Renderer()

        self.slomo = False
        self.sleep = 100

        self.vertical_win = True

        # only if a bot wins against all champions can he enter the champions, replacing one randomly
        self.champions = []
        self.champion_size = 10
        self.champion_win_counter = 0

        # champion bots
        for i in range(self.champion_size):
            b = TorchBot()
            for _ in range(0):
                b.mutate()
            self.champions.append(b)

        self.gameCount = 0
        self.illegal_move_counter = 0
        self.foul_play = False
        self.wins = [0,0]

        # create map
        self.world = Gamefield()

        # create player list
        self.player_list = []
        self.player_list.append(self.champions[0])
        self.player_list.append(self.champions[1])
        self.player_color = ['RED', 'BLUE']
        self.player_points = [0, 0]

        self.player_pointer = 0
        self.beginning_player = 0

    def start(self):
        print('starting game ', self.name)

        self.__init__()
        self.loop()

        print('finished')

    def begin_frame(self):
        pass

    def logic(self):


        self.turney()

        '''
        winner = self.sys_check_for_win(self.world)
        if winner == -1:  # no one has won
            self.player_turn()
        else:

            self.winner_is(winner)
        '''

    def turney(self):

        # create mutant
        #mutant = random.choice(self.champions).get_clone()
        r = random.randint(self.champion_size/2, self.champion_size-1)
        mutant = self.champions[r].get_clone()
        for _ in range(random.randint(1, 15)):
            mutant.mutate()

        # fight against all champs
        self.champion_win_counter = 0
        rounds = 1

        for champ in self.champions:
            temp = 0
            # two rounds so both begin once
            for _ in range(rounds):

                # change who begins
                self.beginning_player += 1
                self.beginning_player %= 2
                self.player_pointer = self.beginning_player

                # remember if the mutant won
                winner = self.play_against(mutant, champ)

                if winner == 0:
                    temp +=1
                    if temp == rounds:
                        self.champion_win_counter += 1

        #fight the random bot too
        random_bot = BotBase()
        # two rounds so both begin once
        for _ in range(rounds):

            # change who begins
            self.beginning_player += 1
            self.beginning_player %= 2
            self.player_pointer = self.beginning_player

            # remember if the mutant won
            if self.play_against(mutant, random_bot) == 0:

                #print('random bot beaten')
                self.champion_win_counter += 1


        # if the mutant won against all other he joins them
        # replacing one random champ

        #if self.champion_win_counter > self.champion_size-2:
        self.champions[self.champion_win_counter-2] = mutant

        #print('wins ', self.champion_win_counter, '/', self.champion_size)
        #print('new champion ', self.champion_win_counter-1)

    def play_against(self, bot0, bot1):

        # reset gamefield
        self.world = Gamefield()

        # set the bots as players
        self.player_list[0] = bot0
        self.player_list[1] = bot1

        winner = -1
        while winner == -1:
            # make one turn
            self.player_turn()

            if self.slomo and self.sleep > 0:
                # draw it on screen
                self.draw()
                self.end_frame()

            # next players turn
            self.next_player()

            if self.foul_play:
                # if we saw a foul the other player won
                self.foul_play = False
                winner = self.player_pointer
            else:
                # check for winner on the field
                winner = self.sys_check_for_win(self.world)

        # draw it on screen
        self.draw()
        self.end_frame()

        self.gameCount += 1
        if self.gameCount % 100 == 0:
            print(' gameCount ', self.gameCount)
        if self.slomo:
            print(' winner: ' + self.player_color[winner])
        #return who has won
        return winner

    def winner_is(self, player_num):
        if self.slomo == True and not self.sleep == 0:

            print('winner of game ', self.gameCount, " is player " + self.player_color[player_num] + ' ' + self.player_list[player_num].name)

        if (self.slomo == True and self.sleep == 0):
            self.draw()

        self.wins[player_num] += 1

        self.gameCount += 1
        if self.gameCount%100 == 0:
            print('end of round ', self.gameCount, self.player_color[0] + ' '+ str(self.wins[0]), self.player_color[1] + ' ' + str(self.wins[1]), ' illegal moves: ', self.illegal_move_counter)
            self.illegal_move_counter = 0
            self.wins = [0, 0]
        # reset gamefield
        self.world = Gamefield()

        # someone has won!
        self.player_points[player_num] += 1
        if self.player_points[player_num] > 7:# and self.player_points[0] != self.player_points[0]:
            self.player_points = [0, 0]

            best = self.player_list[player_num]
            self.player_list = []

            mutant = best.get_clone()
            for _ in range(random.randint(1, 50)):
                mutant.mutate()

            mutant.name = 'mutant'
            best.name = 'champion'

            self.player_list.append(best)
            self.player_list.append(mutant)




    def player_turn(self):
        #print('player ', self.player_pointer, " turn")

        actions = self.world.get_possible_actions()
        player = self.player_list[self.player_pointer]
        choice = player.choose_action(self.world.field, actions, self.player_pointer)

        #illegal choice!
        if not choice in self.world.get_possible_actions():
            #if self.slomo and not self.sleep == 0:
                #print('\t' + self.player_color[self.player_pointer]+ ' made an illegal move and lost the round')

            self.illegal_move_counter += 1

            self.foul_play = True
            return

        #print('\the has choosen ', choice)
        self.world.put_stone(choice, self.player_pointer)

    def next_player(self):
        self.player_pointer += 1
        self.player_pointer %= (len(self.player_list))

    def sys_check_for_win(self, gamefield):

        counter = 1
        last_stone = -1

        if self.vertical_win:
            # check vertical
            for x in range(0, gamefield.rows):
                for y in range(0, gamefield.colomns):
                    if last_stone == gamefield.field[x, y]:
                        counter += 1
                    else:
                        counter = 1
                        last_stone = gamefield.field[x, y]

                    if counter == gamefield.win_condition and not last_stone == -1:

                        return last_stone


        # check horizontal
        for y in range(0, gamefield.colomns):
            for x in range(0, gamefield.rows):
                if last_stone == gamefield.field[x, y]:
                    counter += 1
                else:
                    counter = 1
                    last_stone = gamefield.field[x, y]

                if counter == gamefield.win_condition and not last_stone == -1:

                    return last_stone


        # diagonal checks can be optimized... but fuck it

        # check diagonal left to right
        for x in range(0, gamefield.rows - gamefield.win_condition):
            for y in range(0, gamefield.colomns - gamefield.win_condition):
                for i in range(0, gamefield.win_condition):
                    if last_stone == gamefield.field[x + i, y + i]:
                        counter += 1
                    else:
                        counter = 1
                        last_stone = gamefield.field[x + i, y + i]

                    if counter == gamefield.win_condition and not last_stone == -1:

                        return last_stone

        # check diagonal right to left
        for x in range(gamefield.win_condition, gamefield.rows):
            for y in range(gamefield.win_condition, gamefield.colomns):
                for i in range(0, gamefield.win_condition):
                    if last_stone == gamefield.field[x - i, y - i]:
                        counter += 1
                    else:
                        counter = 1
                        last_stone = gamefield.field[x - i, y - i]

                    if counter == gamefield.win_condition and not last_stone == -1:

                        return last_stone

        # no one has won
        return -1

    def draw(self):
        # empty the screen for new drawings
        self.painter.clear()

        # draw new stuff
        self.painter.draw_connect_four(self.world)

        # Redraw the screen now
        self.painter.flip()

    def end_frame(self):

        # increment the frame counter
        glo.frame_counter += 1

        # for now we jsut wait a little bit
        # later on we should wait depending on FPS settings
        # for a turn based game we might even just draw once and wait for user input


        if self.slomo:
            pygame.time.wait(self.sleep)
        else:
            pass

    # basically user input via mouse or keyboard
    def event_loop(self):
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYUP and event.key == pygame.K_SPACE):
                self.slomo = not self.slomo
            if (event.type == pygame.KEYUP and event.key == pygame.K_UP):
                self.sleep += 10
                print('sleeptime ', self.sleep)
            if (event.type == pygame.KEYUP and event.key == pygame.K_DOWN):
                self.sleep -= 10
                if self.sleep < 0:
                    self.sleep = 0
                print('sleeptime ', self.sleep)


    def loop(self):
        # main gameloop
        # to make the game engine easy we will use one frame for logic AND for rendering
        while True:
            # begin the frame
            self.begin_frame()

            # get user input
            self.event_loop()

            # calculate everything you need
            self.logic()

            if (self.slomo and self.sleep > 0) or self.gameCount%1000 == 0:
                # draw everything
                self.draw()

            # end the frame
            self.end_frame()

