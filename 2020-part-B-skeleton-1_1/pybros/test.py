
# pylint: disable=import-error
from player import Player


p = Player("white")
p.update("white",("MOVE",1,(3,0),(3,2)))
p.update("black", ("MOVE", 1, (3,6),(4,3)))
p.update("black", ("MOVE", 1, (3,7),(4,4)))
print(p.action())