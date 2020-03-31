"""
This module contains some useful functions for different actions.
"""

# pylint: disable=import-error

import copy
from search.util import print_move, print_boom, print_board, print_gamestate


def getCoords(token):
    """ Returns the coordinates of a token (or a stack of tokens)
    
    Arguments:
        token {[int, int, int]} -- [nBTokens, coordX, coordY]
    
    Returns:
        [int, int] -- Coordinates of the stack of tokens
    """
    return [token[1], token[2]]


def distance(t1, t2):
    """ Returns the "boom" distance between two tokens
    
    Arguments:
        t1 {[int, int, int]}
        t2 {[int, int, int]}
    
    Returns:
        int -- "boom" distance (maximum between distances in lines or in columns)
    """
    x1,y1 = getCoords(t1)
    x2,y2 = getCoords(t2)
    return max(abs(x1-x2), abs(y1-y2))


def manhattanDistance(t1, t2):
    """ Returns the manhattan distance between two tokens
    
    Arguments:
        t1 {[int, int, int]}
        t2 {[int, int, int]}
    
    Returns:
        int -- manhattan distance
    """
    x1,y1 = getCoords(t1)
    x2,y2 = getCoords(t2)
    return abs(x1-x2) + abs(y1-y2)


def goalAchieved(gameState):
    """ Returns True if the goal is reached with the specified gamestate
    
    Arguments:
        gameState { } -- dictionary with the lists of the white and the black tokens
    
    Returns:
        bool -- True if all the black tokens would be killed by the explosion of all the white tokens, False otherwise
    """
    nbBlack = len(gameState["black"])
    killed = [False for _ in range(nbBlack)]

    for _ in range(nbBlack):
        for i in range(nbBlack):
            if not killed[i]:
                if min([distance(gameState["black"][i], wToken) for wToken in gameState["white"]] + [distance(gameState["black"][i], gameState["black"][j]) for j in range(nbBlack) if killed[j]]) <= 1:
                    killed[i] = True

    return all(killed)


def move(gameState, n, x1, y1, x2, y2):
    """ This function returns the new gamestate after moving the token as specified, along with a list explaining what the move was
    
    Arguments:
        gameState {dict(str, list([int, int, int]))} -- current gamestate
        n int -- nb of tokens to move
        x1, y1 {int, int} -- original coordinates 
        x2, y2 {int, int} -- target
    
    Returns:
        (gamestate, [str, int, int, int, int, int]) -- new gamestate and a list to recap the move made
    """
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
    """ Returns the number of white tokens on the specified position (None if there isn't any)
    
    Arguments:
        gs {gamestate} -- current gamestate
        x {int} -- x coordinate
        y {int} -- y coordinate
    
    Returns:
        int -- Number of white tokens
    """
    tokens = list(filter(lambda token: getCoords(token) == [x,y], gs["white"]))
    if len(tokens) > 0:
        return tokens[0]
    else:
        return None
    

def occupied(gs, x, y):
    """ Returns True if there is a black token on the specified position, False otherwise 
    """
    return (len(list(filter(lambda token: getCoords(token) == [x,y], gs["black"]))) > 0)


def possibleChildren(gs, cost):
    """ This function returns all the gamestates reachable from the current one within one move
    
    Arguments:
        gs {gamestate} -- current gamestate
        cost {int} -- cost of the path to the current gamestate
    
    Returns:
        list((gamestate, moveRecap), int, gamestate) -- ((new gamestate, recap of the move made), cost of the path to the new gamestate, parent gamestate)
    """
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
    """ This function returns groups of black tokens. Black tokens are in a same group if the explosion of one of them results in the explosion of the entire group.
    
    Arguments:
        gs {gamestate} -- current gamestate
    
    Returns:
        list(list(token)) -- list of groups of black tokens
    """
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
    """ This functions returns an estimated cost to get from the current gamestate to a goal state. 
    
    Arguments:
        gs {gamestate} -- current gamestate
        groupsParam {list(list(token))} -- groups of black tokens
    
    Returns:
        int -- estimated cost
    """
    
    groups = groupsParam.copy()

    # Here, if a white token can kill a group of black tokens by exploding, then we don't take this token into account for the estimated cost, and we consider the related group of black tokens as killed 
    availableTokens = copy.deepcopy(gs["white"])
    for token in availableTokens:
        for group in groups:
            if min([distance(token, target) for target in group])<=1:
                groups.remove(group)
                token[0] -= 1
                break
    
    if groups == []:
        return 0

    # For each remaining white token, we compute the average manhattan distance with any black tokens group still alive, and we finally sum all these averages
    total = 0
    for token in availableTokens:
        total += sum([sum([token[0]*manhattanDistance(token, target) for target in group]) for group in groups])
    return (total // sum([len(group) for group in groups]))


def sortGs(gs):
    """ Sorts the lists of tokens in the gamestate """
    gs["white"].sort()
    gs["black"].sort()

def findPath(node, visited):
    """ This function prints all the moves made to go from the initial gamestate to the final one
    
    Arguments:
        node {node} -- the final node (containing the final gamestate)
        visited {list(node)} -- list of the nodes visited during the search
    
    Returns:
        list(node) -- list of the nodes from the initial one to the final one
    """
    if node[1] == 0:
        return []
    else:
        result = findPath(list(filter(lambda n: n[0][0] == node[2], visited))[0], visited) + [node[0]]
        if node[0][1][0] == "move":
            print_move(node[0][1][1:])
        return result
        
def boomAll(gs):
    """ Prints "boom" for every white token """
    for token in gs["white"]:
        print_boom(token[1], token[2])

def bfs(gsStart):
    """ This function finds a solution using an a-star search algorithm, with the estimatedCost function combined with the real cost of the paths as a heuristic
    
    Arguments:
        gsStart {gamestate} -- The initial gamestate
    
    Returns:
        list(node) -- List of the nodes from the initial to the final one
    """
    sortGs(gsStart)
    print_gamestate(gsStart)
    groups = groupBlacks(gsStart)

    # The type of the nodes is as follow : ((gamestate, moveRecap), int, node)
    # which corresponds to : node = ((gameState, last_action), cost_so_far, parent_node)
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
         