
# pylint: disable=import-error
# pylint: disable=no-name-in-module

from opening_moves.opening_moves import read_opening_moves, sort_gs, flat_tuple
from tdleaf_pybros.train import train
from tdleaf_pybros.util import Minimax
import os
import csv
import time


class Player:

    def __init__(self, colour):

        self.gamestate = {
            "white": [[1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1], [1, 3, 0], [1, 3, 1], [1, 4, 0], [1, 4, 1], [1, 6, 0], [1, 6, 1], [1, 7, 0], [1, 7, 1]],
            "black": [[1, 0, 7], [1, 0, 6], [1, 1, 7], [1, 1, 6], [1, 3, 7], [1, 3, 6], [1, 4, 7], [1, 4, 6], [1, 6, 7], [1, 6, 6], [1, 7, 7], [1, 7, 6]]
        }
        self.colour = colour
        self.book_opening_moves = read_opening_moves()
        self.states_list = []
        self.turn = 1
        self.time_left = 60

        with open(os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), "weights.csv"), newline='') as csvfile:
            r = csv.reader(csvfile, delimiter=";")
            row = next(r)
            self.weights = list(map(float, row))


    def action(self):

        start_time = time.time()

        if self.turn == 1:
            sort_gs(self.gamestate)
            self.time_left -= (time.time() - start_time)
            return self.book_opening_moves[(flat_tuple(self.gamestate), self.colour)]

        else:
            minimax = Minimax(self.colour, self.weights, self.turn, self.time_left)
            best_move, reward, leaf = minimax.best_action(self.gamestate)
            self.states_list.append((reward, leaf))
            self.time_left -= (time.time() - start_time)
            return best_move

    def update(self, colour, action):

        if colour==self.colour:
            self.turn += 1
            
        if action[0] == "BOOM":
            for token in self.gamestate[colour]:
                if (token[1], token[2]) == action[1]:
                    boomed_tokens = [token]
                    break

            explosion = True
            while explosion:
                explosion = False
                for c in self.gamestate.keys():
                    for token in self.gamestate[c]:
                        for boomed_token in boomed_tokens:
                            if self.within_reach(token, boomed_token):
                                boomed_tokens.append(token)
                                self.gamestate[c].remove(token)
                                explosion = True
                                break

        elif action[0] == "MOVE":
            for token in self.gamestate[colour]:
                if (token[1], token[2]) == action[2]:
                    moved_token = token
                    break

            tokens_on_target = self.occupied_mine(self.gamestate, colour, action[3][0], action[3][1])

            if moved_token[0] == action[1]:
                self.gamestate[colour].remove(moved_token)
            else:
                moved_token[0] -= action[1]

            if tokens_on_target is None:
                self.gamestate[colour].append([action[1], action[3][0], action[3][1]])
            else:
                tokens_on_target[0] += action[1]

        if len(self.gamestate["white"]) == 0 or len(self.gamestate["black"]) == 0:
            train(self.states_list, self.colour)

        # print_gamestate(self.gamestate)

    def within_reach(self, t1, t2):
        x1, y1 = t1[1], t1[2]
        x2, y2 = t2[1], t2[2]
        if x1 > x2:
            difx = x1-x2
        else:
            difx = x2-x1
        if y1 > y2:
            dify = y1-y2
        else:
            dify = y2-y1
        if difx > dify:
            return difx <= 1
        else:
            return dify <= 1

    def occupied_mine(self, gs, colour, x, y):
        """ Returns the number of white tokens on the specified position (None if there isn't any)

        Arguments:
            gs {gamestate} -- current gamestate
            x {int} -- x coordinate
            y {int} -- y coordinate

        Returns:
            int -- Number of white tokens
        """
        for token in gs[colour]:
            if (token[1], token[2]) == (x, y):
                return token
        return None
