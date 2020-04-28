
# pylint: disable=import-error
# pylint: disable=no-name-in-module

from pybros.utilPrint import print_gamestate
from pybros.util import distance, occupied_mine, minimax
from pybros.opening_moves import read_opening_moves, sort_gs, flat_tuple


class Player:

    def __init__(self, colour):
        pass

    def action(self):
        return eval(input())

    def update(self, colour, action):
        pass
