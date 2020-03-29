"""
This module contains some useful functions for different actions.
"""
import copy
from util import *

def getCoords(token):
    return [token[1], token[2]]

def distance(t1, t2):
    x1,y1 = getCoords(t1)
    x2,y2 = getCoords(t2)
    return max(abs(x1-x2), abs(y1-y2))

def goalAchieved(gameState):

    nbBlack = len(gameState["black"])
    killed = [False for _ in range(nbBlack)]

    for _ in range(nbBlack):
        for i in range(nbBlack):
            if not killed[i]:
                if min([distance(gameState["black"][i], wToken) for wToken in gameState["white"]] + [distance(gameState["black"][i], gameState["black"][j]) for j in range(nbBlack) if killed[j]]) <= 1:
                    killed[i] = True

    return all(killed)

def move(gameState, n, x1, y1, x2, y2):
    gameStateCopy = copy.deepcopy(gameState)
    tokenMoved = list(filter(lambda token: getCoords(token) == [x1,y1], gameStateCopy["white"]))[0]
    if tokenMoved[0] == n:
        tokenMoved[1] = x2
        tokenMoved[2] = y2
    else:
        tokenMoved[0] -= n
        gameStateCopy["white"].append([n,x2,y2])
    return (gameStateCopy, ["move", n, x1, y1, x2, y2])

def occupied(gs, x, y):
    return (len(list(filter(lambda token: getCoords(token) == [x,y], gs["black"]))) > 0)

def possibleChildren(gs, cost):
    result = []
    for token in gs["white"]:
        for i in range(1,token[0]+1):
            if (token[1]+i)<=7 and not(occupied(gs, token[1]+i, token[2])):
                for k in range(i, token[0]+1):
                    result.append((move(gs, k, token[1], token[2], token[1]+i, token[2]), cost+1, gs))
            if (token[1]-i)>=0 and not(occupied(gs, token[1]-i, token[2])):
                for k in range(i, token[0]+1):
                    result.append((move(gs, k, token[1], token[2], token[1]-i, token[2]), cost+1, gs))
            if (token[2]+i)<=7 and not(occupied(gs, token[1], token[2]+i)):
                for k in range(i, token[0]+1):
                    result.append((move(gs, k, token[1], token[2], token[1], token[2]+i), cost+1, gs))
            if (token[2]-i)>=0 and not(occupied(gs, token[1], token[2]-i)):
                for k in range(i, token[0]+1):
                    result.append((move(gs, k, token[1], token[2], token[1], token[2]-i), cost+1, gs))
    return result

def findPath(node, visited):
    if node[1] == 0:
        return []
    else:
        result = findPath(list(filter(lambda n: n[0][0] == node[2], visited))[0], visited) + [node[0]]
        if node[0][1][0] == "move":
            print_move(node[0][1][1:])
        return result
        

def bfs(gsStart):
    visited = [((gsStart, []), 0, None)]
    queue = [((gsStart, []), 0, None)]
    i = 0
    display = {}
    while queue:
        node = queue.pop(0)
        gs = node[0][0]
        if goalAchieved(gs):
            result =  findPath(node, visited)
            print_boom(gs["white"][0][1], gs["white"][0][2])
            print_gamestate(gs)
            return result
        else:
            for nextNode in possibleChildren(gs, node[1]):
                if nextNode[0][0] not in [node[0][0] for node in visited]:
                    queue.append(nextNode)
                    visited.append(nextNode)
            display[(gs["white"][0][1],gs["white"][0][2])] = str(node[1]) + str(i)
            i += 1
    print_board(display)
         