
# pylint: disable=import-error
# pylint: disable=no-name-in-module

from random_pybros.util import distance, occupied_mine, possible_children, random_boom
import random


class Player:

    def __init__(self, colour):

        self.gameState = {
            "white": [[1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1], [1, 3, 0], [1, 3, 1], [1, 4, 0], [1, 4, 1], [1, 6, 0], [1, 6, 1], [1, 7, 0], [1, 7, 1]],
            "black": [[1, 0, 7], [1, 0, 6], [1, 1, 7], [1, 1, 6], [1, 3, 7], [1, 3, 6], [1, 4, 7], [1, 4, 6], [1, 6, 7], [1, 6, 6], [1, 7, 7], [1, 7, 6]]
        }
        self.colour = colour

    def action(self):

        if random.uniform(0, 1) < 0.1:
            return random_boom(self.gameState, self.colour)
        children = possible_children(self.gameState, self.colour)
        return random.choice(children)

    def update(self, colour, action):

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
                            if distance(token, boomed_token) <= 1:
                                boomed_tokens.append(token)
                                self.gameState[c].remove(token)
                                explosion = True
                                break

        elif action[0] == "MOVE":
            for token in self.gameState[colour]:
                if (token[1], token[2]) == action[2]:
                    moved_token = token
                    break

            tokens_on_target = occupied_mine(self.gameState, colour, action[3][0], action[3][1])

            if moved_token[0] == action[1]:
                self.gameState[colour].remove(moved_token)
            else:
                moved_token[0] -= action[1]

            if tokens_on_target is None:
                self.gameState[colour].append([action[1], action[3][0], action[3][1]])
            else:
                tokens_on_target[0] += action[1]
