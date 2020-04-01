"""
This module contains some useful functions for different actions.
"""

# pylint: disable=import-error

import copy
import time
from search.util import print_move, print_boom, print_board, print_gamestate

timeEstimate = 0
time2 = 0
time3 = 0
count = 0
timeGoalCheck = 0
timeChild = 0


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
    result = max(abs(t1[1]-t2[1]), abs(t1[2]-t2[2]))
    return result


def manhattanDistance(t1, t2):
    """ Returns the manhattan distance between two tokens

    Arguments:
        t1 {[int, int, int]}
        t2 {[int, int, int]}

    Returns:
        int -- manhattan distance
    """
    x1, y1 = getCoords(t1)
    x2, y2 = getCoords(t2)
    return abs(x1-x2) + abs(y1-y2)


def goalAchieved(gameState, groups):
    """ Returns True if the goal is reached with the specified gamestate

    Arguments:
        gameState {gamestate} -- dictionary with the lists of the white and the black tokens
        groups {list(list(token))} -- groups of black tokens

    Returns:
        bool -- True if all the black tokens would be killed by the explosion of all the white tokens, False otherwise
    """
    global timeGoalCheck

    start_time = time.time()
    nbBlack = len(gameState["black"])
    killed = [False for _ in groups]

    if len(gameState["white"]) == 0:
        return nbBlack == 0

    for wToken in gameState["white"]:
        for i in range(len(groups)):
            if min([distance(wToken, token) for token in groups[i]]) <= 1:
                killed[i] = True

    timeGoalCheck += (time.time() - start_time)

    return all(killed)


def boom(gameState, x, y, groupsOld):
    """ This function return the new gamestate after the explosion of the stack of tokens placed in (x,y)

    Arguments:
        gameState {gamestate} -- The current gamestate
        x {int} -- x coordinate
        y {int} -- y coordinate
        groupsOld {list(list(token))} -- groups of black tokens in the current gamestate

    Returns:
        (gamestate, [str,int,int], list(list(token))) -- (new_gamestate, explaination of the boom, new_groups)
    """
    gameStateCopy = copy.deepcopy(gameState)
    groups = []

    tokenBoomed = list(filter(lambda token: getCoords(token) == [x, y], gameStateCopy["white"]))[0]

    for group in groupsOld:
        if min([distance(tokenBoomed, token) for token in group]) <= 1:
            for token in group:
                gameStateCopy["black"].remove(token)
        else:
            groups.append(group)

    for wToken in gameState["white"]:
        if min([distance(wToken, token) for group in groupsOld for token in group if (group not in groups)] + [distance(wToken, tokenBoomed)]) <= 1:
            gameStateCopy["white"].remove(wToken)

    if tokenBoomed in gameStateCopy["white"]:
        gameStateCopy["white"].remove(tokenBoomed)

    return (gameStateCopy, ["boom", x, y], groups)


def move(gameState, n, x1, y1, x2, y2, groups):
    """ This function returns the new gamestate after moving the token as specified, along with a list explaining what the move was

    Arguments:
        gameState {dict(str, list([int, int, int]))} -- current gamestate
        n int -- nb of tokens to move
        x1, y1 {int, int} -- original coordinates 
        x2, y2 {int, int} -- target
        groups {list(list(token))} -- groups of black tokens

    Returns:
        (gamestate, [str, int, int, int, int, int], groups) -- new gamestate, a list to recap the move made, and the groups of black tokens
    """
    gameStateCopy = copy.deepcopy(gameState)
    tokenMoved = list(filter(lambda token: getCoords(token) == [x1, y1], gameStateCopy["white"]))[0]
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
            gameStateCopy["white"].append([n, x2, y2])
        else:
            tokensOnTarget[0] += n
    return (gameStateCopy, ["move", n, x1, y1, x2, y2], groups)


def occupiedWhite(gs, x, y):
    """ Returns the number of white tokens on the specified position (None if there isn't any)

    Arguments:
        gs {gamestate} -- current gamestate
        x {int} -- x coordinate
        y {int} -- y coordinate

    Returns:
        int -- Number of white tokens
    """
    tokens = list(filter(lambda token: getCoords(token) == [x, y], gs["white"]))
    if len(tokens) > 0:
        return tokens[0]
    else:
        return None


def occupied(gs, x, y):
    """ Returns True if there is a black token on the specified position, False otherwise """
    return (len(list(filter(lambda token: getCoords(token) == [x, y], gs["black"]))) > 0)


def possibleChildren(gs, cost, groups):
    """ This function returns all the gamestates reachable from the current one within one move

    Arguments:
        gs {gamestate} -- current gamestate
        cost {int} -- cost of the path to the current gamestate
        groups {list(list(token))} -- groups of black tokens

    Returns:
        list((gamestate, moveRecap), int, int, gamestate) -- ((new gamestate, recap of the move made), cost of the path to the new gamestate, estimated cost until a goal state, parent gamestate)
    """

    global timeChild

    start_time = time.time()
    result = []
    for token in gs["white"]:
        boomResult = boom(gs, token[1], token[2], groups)
        result.append((boomResult, cost+1, estimatedCost(boomResult[0], boomResult[2]), gs))
        for i in range(1, token[0]+1):
            if (token[1]+i) <= 7 and not(occupied(gs, token[1]+i, token[2])):
                for k in range(i, token[0]+1):
                    moveResult = move(gs, k, token[1], token[2], token[1]+i, token[2], groups)
                    result.append((moveResult, cost+1, estimatedCost(moveResult[0], moveResult[2]), gs))
            if (token[1]-i) >= 0 and not(occupied(gs, token[1]-i, token[2])):
                for k in range(i, token[0]+1):
                    moveResult = move(gs, k, token[1], token[2], token[1]-i, token[2], groups)
                    result.append((moveResult, cost+1, estimatedCost(moveResult[0], moveResult[2]), gs))
            if (token[2]+i) <= 7 and not(occupied(gs, token[1], token[2]+i)):
                for k in range(i, token[0]+1):
                    moveResult = move(gs, k, token[1], token[2], token[1], token[2]+i, groups)
                    result.append((moveResult, cost+1, estimatedCost(moveResult[0], moveResult[2]), gs))
            if (token[2]-i) >= 0 and not(occupied(gs, token[1], token[2]-i)):
                for k in range(i, token[0]+1):
                    moveResult = move(gs, k, token[1], token[2], token[1], token[2]-i, groups)
                    result.append((moveResult, cost+1, estimatedCost(moveResult[0], moveResult[2]), gs))
    timeChild += (time.time() - start_time)
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
            left = len([t for t in grouped if not(t)])
            for _ in range(left):
                for j in range(i+1, nbBlacks):
                    if (not grouped[j]) and (min([distance(gs["black"][j], token) for token in newGroup]) <= 1):
                        newGroup.append(gs["black"][j])
                        grouped[j] = True
            groups.append(newGroup)

    return groups


def estimatedCost(gs, groupsParam):
    """ This function returns an estimated cost to get from the current gamestate to a goal state. 

    Arguments:
        gs {gamestate} -- current gamestate
        groupsParam {list(list(token))} -- groups of black tokens

    Returns:
        int -- estimated cost
    """
    global timeEstimate
    global time2
    global time3
    global count

    count += 1
    start_time = time.time()

    groups = []

    start_time2 = time.time()

    # Here, if a white token can kill a group of black tokens by exploding, then we don't take this token into account for the estimated cost, and we consider the related group of black tokens as killed
    availableTokens = copy.deepcopy(gs["white"])
    killed = [False for _ in range(len(groupsParam))]
    for token in availableTokens:
        explode = False
        for i in range(len(groupsParam)):
            if not killed[i]:
                group = groupsParam[i]
                if min([distance(token, target) for target in group]) <= 1:
                    explode = True
                    killed[i] = True
        if explode:
            token[0] -= 1

    time2 += (time.time() - start_time2)

    groups = [groupsParam[i] for i in range(len(groupsParam)) if not killed[i]]

    if groups == []:
        timeEstimate += (time.time() - start_time)
        return 0

    start_time3 = time.time()
    # For each remaining white token, we compute the average manhattan distance with any black tokens group still alive, and we finally sum all these averages
    total = 0
    for token in availableTokens:
        total += sum([token[0]*manhattanDistance(token, target) for group in groups for target in group])
    timeEstimate += (time.time() - start_time)
    time3 += (time.time() - start_time3)
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
        result = findPath(list(filter(lambda n: n[0][0] == node[3], visited))[0], visited) + [node[0]]
        if node[0][1][0] == "move":
            print_move(node[0][1][1:])
        elif node[0][1][0] == "boom":
            print_boom(node[0][1][1], node[0][1][2])
        return result


def boomAll(gs):
    """ Prints "boom" for every white token """
    if len(gs["white"]) > 0:
        token = gs["white"][0] 
        print_boom(token[1], token[2])
        newGs = boom(gs, token[1], token[2], groupBlacks(gs))[0]
        boomAll(newGs)


def insort(l, node, f):
    """ Insert a node in a sorted list using a key function f

    Arguments:
        l {list} -- A sorted list
        node {node} -- The node to insert in the list
        f {lambda node: int} -- Key function allowing to sort the list
    """
    lo = 0
    hi = len(l)
    while lo < hi:
        mid = (lo+hi)//2
        if f(l[mid]) < f(node):
            lo = mid+1
        elif f(l[mid]) == f(node):
            l.insert(mid, node)
            return
        else:
            hi = mid
    l.insert(lo, node)


def flatTuple(gs):
    """ This function turns the gamestate in a tuple of tuples, in order to make it hashable """
    return tuple(map(tuple, gs["white"] + gs["black"]))


def bfs(gsStart):
    """ This function finds a solution using an a-star search algorithm, with the estimatedCost function as a heuristic

    Arguments:
        gsStart {gamestate} -- The initial gamestate

    Returns:
        list(node) -- List of the nodes from the initial to the final one
    """
    timeSortGs = 0
    timeTest = 0

    start_total = time.time()

    sortGs(gsStart)
    print_gamestate(gsStart)
    groups = groupBlacks(gsStart)

    # The type of the nodes is as follow : ((gamestate, moveRecap, list(list(token))), int, int, node)
    # which corresponds to : node = ((gameState, last_action, groups_of_blacks), cost_so_far, estimated_cost, parent_node)
    estimCost = estimatedCost(gsStart, groups)
    visited = [((gsStart, [], groups), 0, estimCost, None)]
    # The use of a set instead of a list increases the performances
    visitedGs = set(flatTuple(gsStart))
    queue = [((gsStart, [], groups), 0, estimCost, None)]

    while queue:
        node = queue.pop(0)
        gs = node[0][0]
        if goalAchieved(gs, groups):
            result = findPath(node, visited)
            boomAll(gs)
            print_gamestate(gs)
            print("# Nb of estimation cost : " + str(count))
            print("# TimeEstimation : " + str(timeEstimate))
            print("# Time estimation selection : " + str(time2))
            print("# Time estimation calculation : " + str(time3))
            print("# Time Goal : " + str(timeGoalCheck))
            print("# Time find children : " + str(timeChild))
            print("# Time insort : " + str(timeSortGs))
            print("# Time total : " + str(time.time() - start_total))
            print("# Time test : " + str(timeTest))
            return result

        else:
            for nextNode in possibleChildren(gs, node[1], node[0][2]):
                sortGs(nextNode[0][0])
                startTest = time.time()

                if flatTuple(nextNode[0][0]) not in visitedGs:
                    timeTest += (time.time() - startTest)
                    start_time_insorting = time.time()
                    insort(queue, nextNode, (lambda newNode: 2*newNode[1] + newNode[2]))
                    visited.append(nextNode)
                    visitedGs.add(flatTuple(nextNode[0][0]))
                    timeSortGs += (time.time() - start_time_insorting)

                else:
                    timeTest += (time.time() - startTest)
