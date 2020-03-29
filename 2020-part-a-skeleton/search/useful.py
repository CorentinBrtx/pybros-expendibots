"""
This module contains some useful functions for different actions.
"""

# pylint: disable=import-error

import copy
from search.util import print_move, print_boom, print_board, print_gamestate

def getCoords(token):
    return [token[1], token[2]]

def distance(t1, t2):
    x1,y1 = getCoords(t1)
    x2,y2 = getCoords(t2)
    return max(abs(x1-x2), abs(y1-y2))

def manhattanDistance(t1, t2):
    x1,y1 = getCoords(t1)
    x2,y2 = getCoords(t2)
    return abs(x1-x2) + abs(y1-y2)

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
    tokensOnTarget = occupiedWhite(gameStateCopy, x2, y2)
    if tokenMoved[0] == n:
        if tokensOnTarget is None:
            tokenMoved[1] = x2
            tokenMoved[2] = y2
        else:
            gameStateCopy["white"].remove(tokenMoved)
            tokensOnTarget[0] += n
    else:
        tokenMoved[0] -= n
        if tokensOnTarget is None:
            gameStateCopy["white"].append([n,x2,y2])
        else:
            tokensOnTarget[0] += n
    return (gameStateCopy, ["move", n, x1, y1, x2, y2])

def occupiedWhite(gs, x, y):
    tokens = list(filter(lambda token: getCoords(token) == [x,y], gs["white"]))
    if len(tokens) > 0:
        return tokens[0]
    else:
        return None
    
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

def groupBlacks(gs):
    nbBlacks = len(gs["black"])
    groups = []
    grouped = [False for _ in range(nbBlacks)]
    for i in range(nbBlacks):
        if not grouped[i]:
            grouped[i] = True
            newGroup = [gs["black"][i]]
            for j in range(i+1, nbBlacks):
                if (not grouped[j]) and (min([distance(gs["black"][j], token) for token in newGroup])<=1):
                    newGroup.append(gs["black"][j])
                    grouped[j] = True
            groups.append(newGroup)
    
    return groups

def estimatedCost(gs, groupsParam):
    
    groups = groupsParam.copy()

    availableTokens = copy.deepcopy(gs["white"])
    for token in availableTokens:
        for group in groups:
            if min([distance(token, target) for target in group])<=1:
                groups.remove(group)
                token[0] -= 1
                break
    
    if groups == []:
        return 0

    total = 0
    for token in availableTokens:
        total += sum([sum([token[0]*manhattanDistance(token, target) for target in group]) for group in groups])
    return (total // sum([len(group) for group in groups]))


def sortGs(gs):
    gs["white"].sort()
    gs["black"].sort()

def findPath(node, visited):
    if node[1] == 0:
        return []
    else:
        result = findPath(list(filter(lambda n: n[0][0] == node[2], visited))[0], visited) + [node[0]]
        if node[0][1][0] == "move":
            print_move(node[0][1][1:])
        return result
        
def boomAll(gs):
    for token in gs["white"]:
        print_boom(token[1], token[2])

def bfs(gsStart):
    sortGs(gsStart)
    print_gamestate(gsStart)
    groups = groupBlacks(gsStart)
    # Node = ((gameState, last_action), cost_so_far, parent_node)
    visited = [((gsStart, []), 0, None)]
    queue = [((gsStart, []), 0, None)]
    i = 0
    display = {}
    while queue:
        node = queue.pop(0)
        gs = node[0][0]
        if goalAchieved(gs):
            result =  findPath(node, visited)
            boomAll(gs)
            print_gamestate(gs)
            return result
        else:
            for nextNode in possibleChildren(gs, node[1]):
                sortGs(nextNode[0][0])
                if nextNode[0][0] not in [node[0][0] for node in visited]:
                    queue.append(nextNode)
                    visited.append(nextNode)
            queue.sort(key = (lambda newNode: 2*newNode[1] + estimatedCost(newNode[0][0], groups)))
            display[(gs["white"][0][1],gs["white"][0][2])] = str(node[1]) + str(i)
            i += 1
    print_board(display)
         