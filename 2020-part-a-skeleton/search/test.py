from useful import bfs, boom, groupBlacks, goalAchieved
import copy
import cProfile
import pstats


gameState = {
    "white": [[3,0,0]],
    "black": [[1,7,7],[1,7,0],[1,0,7],[1,5,0],[1,5,1],[1,5,2],[1,6,2],[1,7,2]]
}
"""

gameState = {
    "white": [[1,0,1],[1,1,0],[1,4,4],[1,4,7]],
    "black": [[1,0,3],[1,1,3],[1,2,3],[1,3,2],[1,3,1],[1,3,0],[1,1,1],[1,0,4],[1,1,4],[1,2,4],[1,4,2],[1,4,1],[1,4,0],[1,7,4],[1,0,7],[1,7,0]]
}

"""

cProfile.run('bfs(gameState)', 'restats')


#p = pstats.Stats('restats')

#p.strip_dirs().sort_stats('cumulative').print_stats()
