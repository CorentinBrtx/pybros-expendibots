
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir)))

# pylint: disable=import-error
from tdleaf_pybros.player import Player
import cProfile
import pstats

p = Player("white")
p.update("black", ("MOVE", 1, (4,6),(3,6)))
p.update("white", ("MOVE", 1, (3,1),(4,1)))
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
#print(p.action())

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
#     for i in range(1000000):
#         if (i<500000):
#             if (within_reach([1,1,1],[1,4,5])):
#                 coucou = i

# cProfile.run('test()', 'restats')

cProfile.run('print(p.action())', 'restats')


p = pstats.Stats('restats')

p.strip_dirs().sort_stats('tottime').print_stats()