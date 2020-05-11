
# pylint: disable=import-error
# pylint: disable=no-name-in-module

from pybros.util import Minimax
from pybros.opening_moves import read_opening_moves, sort_gs, flat_tuple
import time


class Player:

    def __init__(self, colour):

        self.gameState = {
            "white": [[1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1], [1, 3, 0], [1, 3, 1], [1, 4, 0], [1, 4, 1], [1, 6, 0], [1, 6, 1], [1, 7, 0], [1, 7, 1]],
            "black": [[1, 0, 7], [1, 0, 6], [1, 1, 7], [1, 1, 6], [1, 3, 7], [1, 3, 6], [1, 4, 7], [1, 4, 6], [1, 6, 7], [1, 6, 6], [1, 7, 7], [1, 7, 6]]
        }
        self.colour = colour
        self.turn = 0
        self.book_opening_moves = read_opening_moves()
        self.time_left = 60

        self.weights = [6.5, -6.5, -0.37, 4.3, -0.1]

    def action(self):

        start_time = time.process_time()

        self.turn += 1

        if self.turn == 1:
            sort_gs(self.gameState)
            stop_time = time.process_time()
            self.time_left -= (stop_time - start_time)
            return self.book_opening_moves[(flat_tuple(self.gameState), self.colour)]

        else:
            minimax = Minimax(self.colour, self.weights, self.turn, self.time_left)
            best_action = minimax.best_action(self.gameState)
            stop_time = time.process_time()
            self.time_left -= (stop_time - start_time)
            return best_action

    def update(self, colour, action):

        if colour == self.colour:
            self.turn += 1

        if action[0] == "BOOM":
            for token in self.gameState[colour]:
                if (token[1], token[2]) == action[1]:
                    boomed_tokens = [token]
                    break

            explosion = True
            while explosion:
                explosion = False
                for c in self.gameState.keys():
                    for token in self.gameState[c]:
                        for boomed_token in boomed_tokens:
                            if self.within_reach(token, boomed_token):
                                boomed_tokens.append(token)
                                self.gameState[c].remove(token)
                                explosion = True
                                break

        elif action[0] == "MOVE":
            for token in self.gameState[colour]:
                if (token[1], token[2]) == action[2]:
                    moved_token = token
                    break

            tokens_on_target = self.occupied_mine(self.gameState, colour, action[3][0], action[3][1])

            if moved_token[0] == action[1]:
                self.gameState[colour].remove(moved_token)
            else:
                moved_token[0] -= action[1]

            if tokens_on_target is None:
                self.gameState[colour].append([action[1], action[3][0], action[3][1]])
            else:
                tokens_on_target[0] += action[1]

    def within_reach(self, t1, t2):
        """
        Returns True if t1 and t2 and in an explosion radius (1 square apart)
        """
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
        """ 
        Returns the number of your tokens on the specified position (None if there isn't any)
        """
        for token in gs[colour]:
            if (token[1], token[2]) == (x, y):
                return token
        return None
