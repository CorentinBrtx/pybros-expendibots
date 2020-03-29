"""
This module contains some useful functions for different actions.
"""
import copy

def getCoords(token):
    return [token[1], token[2]]

def distance(t1, t2):
    x1,y1 = getCoords(t1)
    x2,y2 = getCoords(t2)
    return max(abs(x1-x2), abs(y1-y2))

def goalAchieved(gameState):
    myToken = gameState["white"][0]
    target = gameState["black"][0]
    return (distance(myToken, target) <= 1)

def move(gameState, n, x1, y1, x2, y2):
    gameStateCopy = copy.deepcopy(gameState)
    tokenMoved = list(filter(lambda token: getCoords(token) == [x1,y1], gameStateCopy["white"]))[0]
    if tokenMoved[0] == n:
        tokenMoved[1] = x2
        tokenMoved[2] = y2
    else:
        tokenMoved[0] -= n
        gameStateCopy["white"].append([n,x2,y2])
    return gameStateCopy

def occupied(gs, x, y):
    return (len(list(filter(lambda token: getCoords(token) == [x,y], gs["black"]))) > 0)

def possibleChildren(gs):
    result = []
    for token in gs["white"]:
        for i in range(1,token[0]+1):
            if (token[1]+i)<=7 and not(occupied(gs, token[1]+i, token[2])):
                for k in range(i, token[0]+1):
                    result.append(move(gs, k, token[1], token[2], token[1]+i, token[2]))
            if (token[1]-i)>=0 and not(occupied(gs, token[1]-i, token[2])):
                for k in range(i, token[0]+1):
                    result.append(move(gs, k, token[1], token[2], token[1]-i, token[2]))
            if (token[2]+i)<=7 and not(occupied(gs, token[1], token[2]+i)):
                for k in range(i, token[0]+1):
                    result.append(move(gs, k, token[1], token[2], token[1], token[2]+i))
            if (token[2]-i)>=0 and not(occupied(gs, token[1], token[2]-i)):
                for k in range(i, token[0]+1):
                    result.append(move(gs, k, token[1], token[2], token[1], token[2]-i))
    return result


         