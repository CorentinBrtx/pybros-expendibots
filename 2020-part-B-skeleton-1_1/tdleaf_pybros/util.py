
# pylint: disable=import-error

from tdleaf_pybros.utilPrint import print_move, print_boom, print_board, print_gamestate
from math import inf, tanh


def get_coords(token):
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


def boom(gameState, colour, action, groups):
    """ This function return the new gamestate after the explosion of the stack of tokens placed in (x,y)

    Arguments:
        gameState {gamestate} -- The current gamestate
        x {int} -- x coordinate
        y {int} -- y coordinate

    Returns:
        (gamestate, [str,int,int]) -- (new_gamestate, explaination of the boom)
    """

    (x, y) = action
    other = other_colour(colour)

    gameStateCopy = {"white": gameState["white"].copy(), "black": gameState["black"].copy()}

    for token in gameStateCopy[colour]:
        if (token[1], token[2]) == (x, y):
            boomed_tokens = [token]
            break

    explosion = True
    while explosion:
        explosion = False
        old_boomed_tokens = boomed_tokens
        old_groups = groups
        boomed_tokens = []
        groups = []

        for token in gameStateCopy[colour]:
            for boomed_token in old_boomed_tokens:
                if distance(token, boomed_token) <= 1:
                    boomed_tokens.append(token)
                    gameStateCopy[colour].remove(token)
                    explosion = True
                    break

        for group in old_groups:
            boomed = False
            for boomed_token in old_boomed_tokens:
                for token in group:
                    if distance(token, boomed_token) <= 1:
                        for t in group:
                            boomed_tokens.append(t)
                            gameStateCopy[other].remove(t)
                        explosion = True
                        boomed = True
                        break
                if boomed:
                    break
            if not boomed:
                groups.append(group)

    return (gameStateCopy, ("BOOM", (x, y)))


def move(gameState, colour, action):
    """ This function returns the new gamestate after moving the token as specified, along with a list explaining what the move was

    Arguments:
        gameState {dict(str, list([int, int, int]))} -- current gamestate
        n int -- nb of tokens to move
        x1, y1 {int, int} -- original coordinates 
        x2, y2 {int, int} -- target

    Returns:
        (gamestate, [str, int, int, int, int, int]) -- new gamestate, a list to recap the move made
    """

    (n, (x1, y1), (x2, y2)) = action

    gameStateCopy = {"white": gameState["white"].copy(), "black": gameState["black"].copy()}

    token_moved = list(filter(lambda token: get_coords(token) == [x1, y1], gameStateCopy[colour]))[0]
    tokens_on_target = occupied_mine(gameStateCopy, colour, x2, y2)

    if token_moved[0] == n:
        if tokens_on_target is None:
            gameStateCopy[colour].remove(token_moved)
            gameStateCopy[colour].append([n, x2, y2])
        else:
            gameStateCopy[colour].remove(token_moved)
            alreadyHere = tokens_on_target[0]
            gameStateCopy[colour].remove(tokens_on_target)
            gameStateCopy[colour].append([n+alreadyHere, x2, y2])
    else:
        here = token_moved[0]
        gameStateCopy[colour].remove(token_moved)
        gameStateCopy[colour].append([here-n, x1, y1])
        if tokens_on_target is None:
            gameStateCopy[colour].append([n, x2, y2])
        else:
            alreadyHere = tokens_on_target[0]
            gameStateCopy[colour].remove(tokens_on_target)
            gameStateCopy[colour].append([n+alreadyHere, x2, y2])

    return (gameStateCopy, ("MOVE", n, (x1, y1), (x2, y2)))


def occupied_mine(gs, colour, x, y):
    """ Returns the number of white tokens on the specified position (None if there isn't any)

    Arguments:
        gs {gamestate} -- current gamestate
        x {int} -- x coordinate
        y {int} -- y coordinate

    Returns:
        int -- Number of white tokens
    """
    for token in gs[colour]:
        if (token[1], token[2]) == (x, y):
            return token
    return None


def occupied_other(gs, colour, x, y):
    """ Returns True if there is a black token on the specified position, False otherwise """
    other = other_colour(colour)

    for token in gs[other]:
        if (token[1], token[2]) == (x, y):
            return True
    return False


def group_other_tokens(gs, colour):
    other = other_colour(colour)

    nb_others = len(gs[other])
    groups = []
    grouped = [False for _ in range(nb_others)]

    for i in range(nb_others):
        if not grouped[i]:
            grouped[i] = True
            new_group = [gs[other][i]]
            not_grouped = len([t for t in grouped if not(t)])
            for _ in range(not_grouped):
                for j in range(i+1, nb_others):
                    if not grouped[j]:
                        for token in new_group:
                            if distance(gs[other][j], token) <= 1:
                                new_group.append(gs[other][j])
                                grouped[j] = True
                                break
            groups.append(new_group)

    return groups


def possible_children(gs, colour):
    """ This function returns all the gamestates reachable from the current one within one move

    Arguments:
        gs {gamestate} -- current gamestate

    Returns:
        list((gamestate, moveRecap)) -- ((new gamestate, recap of the move made))
    """

    result = []
    groups = group_other_tokens(gs, colour)
    for token in gs[colour]:
        boomResult = boom(gs, colour, (token[1], token[2]), groups)
        result.append(boomResult)
        for i in range(1, token[0]+1):
            if (token[1]+i) <= 7 and not(occupied_other(gs, colour, token[1]+i, token[2])):
                for k in range(1, token[0]+1):
                    moveResult = move(gs, colour, (k, (token[1], token[2]), (token[1]+i, token[2])))
                    result.append(moveResult)
            if (token[1]-i) >= 0 and not(occupied_other(gs, colour, token[1]-i, token[2])):
                for k in range(1, token[0]+1):
                    moveResult = move(gs, colour, (k, (token[1], token[2]), (token[1]-i, token[2])))
                    result.append(moveResult)
            if (token[2]+i) <= 7 and not(occupied_other(gs, colour, token[1], token[2]+i)):
                for k in range(1, token[0]+1):
                    moveResult = move(gs, colour, (k, (token[1], token[2]), (token[1], token[2]+i)))
                    result.append(moveResult)
            if (token[2]-i) >= 0 and not(occupied_other(gs, colour, token[1], token[2]-i)):
                for k in range(1, token[0]+1):
                    moveResult = move(gs, colour, (k, (token[1], token[2]), (token[1], token[2]-i)))
                    result.append(moveResult)
    return result


def sort_gs(gs):
    """ Sorts the lists of tokens in the gamestate """
    gs["white"].sort()
    gs["black"].sort()


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


def flat_tuple(gs):
    """ This function turns the gamestate in a tuple of tuples, in order to make it hashable """
    return tuple(map(tuple, gs["white"] + gs["black"]))


def minimax(gs, colour, weights):

    children = possible_children(gs, colour)

    nb_mine = 0
    for token in gs[colour]:
        nb_mine += token[0]

    if nb_mine < 5:
        max_depth = 4
    else:
        max_depth = 3

    alpha = -inf
    beta = inf
    best_move = None
    best_leaf = None
    for child in children:
        value, gs_leaf = minimax_value(child, colour, 1, alpha, beta, max_depth, weights)
        if value > alpha:
            best_move = child[1]
            best_leaf = gs_leaf
            alpha = value

    print(alpha)
    # print_gamestate(best_leaf)
    return best_move, alpha, best_leaf


def minimax_value(operation, colour, depth, alpha, beta, max_depth, weights):

    gs = operation[0]

    other = other_colour(colour)

    if (len(gs[colour]) == 0):
        return -1, gs
    elif (len(gs[other]) == 0):
        return 1, gs
    elif depth >= max_depth:
        return tanh(evaluation(gs, colour, weights)), gs
    else:
        if depth % 2 == 0:
            children = possible_children(gs, colour)
            best = None
            for child in children:
                value, gs_leaf = minimax_value(child, colour, depth+1, alpha, beta, max_depth, weights)
                if value > alpha:
                    alpha = value
                    best = gs_leaf
                if alpha >= beta:
                    return beta, None
            return alpha, best
        else:
            children = possible_children(gs, other)
            best = None
            for child in children:
                value, gs_leaf = minimax_value(child, colour, depth+1, alpha, beta, max_depth, weights)
                if value < beta:
                    beta = value
                    best = gs_leaf
                if beta <= alpha:
                    return alpha, None
            return beta, best


def evaluation(gs, colour, w):
    other = other_colour(colour)

    mine, other, within_reach, neighbours, stacks, agressivity = features(gs, colour)

    return w[0]*mine + w[1]*other + w[2]*neighbours + w[3]*stacks + w[4]*within_reach + w[5]*agressivity


def features(gs, colour):
    other = other_colour(colour)
    total_mine = 0
    total_other = 0
    within_reach = 0
    total_neighbours = 0
    total_stacks = 0
    agressivity = 0

    for token in gs[other]:
        total_other += token[0]

    for i in range(len(gs[colour])):
        total_stacks += gs[colour][i][0] - 1
        total_mine += gs[colour][i][0]
        agressivity += gs[colour][i][2]*gs[colour][i][0]
        for j in range(i+1, len(gs[colour])):
            if distance(gs[colour][i], gs[colour][j]) <= 1:
                total_neighbours += 2
        for j in range(len(gs[other])):
            if distance(gs[colour][i], gs[other][j]) <= 1:
                within_reach += gs[other][j][0]

    if colour=="black":
        agressivity = 7*total_mine - agressivity

    return total_mine/12, total_other/12, within_reach/(total_other+1), total_neighbours/(8*len(gs[colour])+1), total_stacks/(total_mine+1), agressivity/(7*total_mine+1)


def other_colour(colour):
    if colour == "white":
        return "black"
    else:
        return "white"
