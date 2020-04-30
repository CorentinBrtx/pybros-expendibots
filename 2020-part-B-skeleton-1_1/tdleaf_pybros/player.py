
# pylint: disable=import-error
# pylint: disable=no-name-in-module

from tdleaf_pybros.utilPrint import print_gamestate
from tdleaf_pybros.util import distance, occupied_mine, minimax
from opening_moves.opening_moves import read_opening_moves, sort_gs, flat_tuple
from tdleaf_pybros.train import train
import os
import csv


class Player:

    def __init__(self, colour):

        self.gamestate = {
            "white": [[1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1], [1, 3, 0], [1, 3, 1], [1, 4, 0], [1, 4, 1], [1, 6, 0], [1, 6, 1], [1, 7, 0], [1, 7, 1]],
            "black": [[1, 0, 7], [1, 0, 6], [1, 1, 7], [1, 1, 6], [1, 3, 7], [1, 3, 6], [1, 4, 7], [1, 4, 6], [1, 6, 7], [1, 6, 6], [1, 7, 7], [1, 7, 6]]
        }
        self.colour = colour
        self.book_opening_moves = read_opening_moves()
        self.states_list = []
        self.turn = 0

        with open(os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), "weights.csv"), newline='') as csvfile:
            r = csv.reader(csvfile, delimiter=";")
            row = next(r)
            self.weights = list(map(float, row))


    def action(self):

        self.turn += 1

        if self.turn == 1:
            sort_gs(self.gamestate)
            return self.book_opening_moves[(flat_tuple(self.gamestate), self.colour)]

        else:
            best_move, reward, leaf = minimax(self.gamestate, self.colour, self.weights)
            self.states_list.append((reward, leaf))
            return best_move

    def update(self, colour, action):
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
                            if distance(token, boomed_token) <= 1:
                                boomed_tokens.append(token)
                                self.gamestate[c].remove(token)
                                explosion = True
                                break

        elif action[0] == "MOVE":
            for token in self.gamestate[colour]:
                if (token[1], token[2]) == action[2]:
                    moved_token = token
                    break

            tokens_on_target = occupied_mine(self.gamestate, colour, action[3][0], action[3][1])

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

        # print_gamestate(self.gameState)
