
# pylint: disable=import-error

#from pybros.utilPrint import print_move, print_boom, print_board, print_gamestate
from math import inf
import random


def distance(t1, t2):
    """ Returns the "boom" distance between two tokens

    Arguments:
        t1 {[int, int, int]}
        t2 {[int, int, int]}

    Returns:
        int -- "boom" distance (maximum between distances in lines or in columns)
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
        return difx
    else:
        return dify


def occupied_mine(gs, colour, x, y):
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


def occupied_other(gs, colour, x, y):
    """ Returns True if there is a black token on the specified position, False otherwise """
    other = other_colour(colour)

    for token in gs[other]:
        if (token[1], token[2]) == (x, y):
            return True
    return False


def random_boom(gs, colour):
    token = random.choice(gs[colour])
    return ("BOOM", (token[1], token[2]))


def possible_children(gs, colour):
    result = []
    for token in gs[colour]:
        for i in range(1, token[0]+1):
            if (token[1]+i) <= 7 and not(occupied_other(gs, colour, token[1]+i, token[2])):
                for k in range(1, token[0]+1):
                    result.append(("MOVE", k, (token[1], token[2]), (token[1]+i, token[2])))
            if (token[1]-i) >= 0 and not(occupied_other(gs, colour, token[1]-i, token[2])):
                for k in range(1, token[0]+1):
                    result.append(("MOVE", k, (token[1], token[2]), (token[1]-i, token[2])))
            if (token[2]+i) <= 7 and not(occupied_other(gs, colour, token[1], token[2]+i)):
                for k in range(1, token[0]+1):
                    result.append(("MOVE", k, (token[1], token[2]), (token[1], token[2]+i)))
            if (token[2]-i) >= 0 and not(occupied_other(gs, colour, token[1], token[2]-i)):
                for k in range(1, token[0]+1):
                    result.append(("MOVE", k, (token[1], token[2]), (token[1], token[2]-i)))
    return result


def other_colour(colour):
    if colour == "white":
        return "black"
    else:
        return "white"
