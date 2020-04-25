
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir)))

# pylint: disable=import-error
from pybros.player import Player
import cProfile
import pstats

p = Player("white")
p.update("white",("MOVE",1,(3,0),(2,4)))
#p.update("black", ("MOVE", 1, (3,6),(4,3)))
#p.update("black", ("MOVE", 1, (3,7),(4,4)))
#print(p.action())


cProfile.run('print(p.action())', 'restats')


p = pstats.Stats('restats')

p.strip_dirs().sort_stats('tottime').print_stats()
