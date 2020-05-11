
import pstats
import cProfile
from math import tanh
from pybros.player import Player
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir)))

# pylint: disable=import-error

p = Player("white")
p.update("black", ("MOVE", 1, (4, 6), (1, 3)))
p.update("black", ("MOVE", 1, (3, 6), (1, 3)))
p.update("black", ("MOVE", 1, (1, 6), (1, 3)))
p.update("white", ("MOVE", 1, (3, 1), (6, 1)))
p.update("white", ("MOVE", 1, (4, 1), (6, 1)))
p.update("white", ("MOVE", 1, (1, 0), (1, 1)))
# p.update("black", ("MOVE", 1, (0,7),(1,6)))
# p.update("black", ("MOVE", 1, (1,7),(1,6)))
# p.update("black", ("MOVE", 1, (0,6),(1,6)))
# p.update("black", ("MOVE", 1, (3,6),(4,6)))
# p.update("black", ("MOVE", 1, (7,7),(6,6)))
# p.update("black", ("MOVE", 1, (6,7),(6,6)))
# p.update("black", ("MOVE", 1, (7,6),(6,6)))
# p.update("white",("MOVE",1,(6,1),(6,5)))
# p.update("white",("MOVE",1,(6,0),(2,5)))
# p.update("white",("MOVE",1,(3,1),(2,5)))
# p.update("white",("MOVE",1,(4,1),(2,5)))
# p.update("white",("MOVE",1,(0,1),(0,3)))
# p.update("white",("MOVE",1,(0,0),(0,3)))
# print(p.action())


def manhattan_distance(t1, t2):
    """ Returns the manhattan distance between two tokens

    Arguments:
        t1 {[int, int, int]}
        t2 {[int, int, int]}

    Returns:
        int -- manhattan distance
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
    return difx+dify


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


def within_reach(t1, t2):
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


# def test():
#     for i in range(10000000):
#         k = manhattan_distance([1,2,5],[3,7,3])

# cProfile.run('test()', 'restats')

cProfile.run('print(p.action())', 'restats')


p = pstats.Stats('restats')

p.strip_dirs().sort_stats('cumtime').print_stats()
