
# pylint: disable=import-error

from pybros.utilPrint import print_move, print_boom, print_board, print_gamestate


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


def boom(gameState, colour, action):
    """ This function return the new gamestate after the explosion of the stack of tokens placed in (x,y)

    Arguments:
        gameState {gamestate} -- The current gamestate
        x {int} -- x coordinate
        y {int} -- y coordinate

    Returns:
        (gamestate, [str,int,int]) -- (new_gamestate, explaination of the boom)
    """

    (x, y) = action

    gameStateCopy = {"white": gameState["white"].copy(), "black": gameState["black"].copy()}

    for token in gameStateCopy[colour]:
        if (token[1], token[2]) == (x, y):
            boomedTokens = [token]
            break

    explosion = True
    while explosion:
        explosion = False
        for c in gameStateCopy.keys():
            for token in gameStateCopy[c]:
                for boomedToken in boomedTokens:
                    if distance(token, boomedToken) <= 1:
                        boomedTokens.append(token)
                        gameStateCopy[c].remove(token)
                        explosion = True
                        break

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


def possible_children(gs, colour):
    """ This function returns all the gamestates reachable from the current one within one move

    Arguments:
        gs {gamestate} -- current gamestate

    Returns:
        list((gamestate, moveRecap)) -- ((new gamestate, recap of the move made))
    """

    result = []
    for token in gs[colour]:
        boomResult = boom(gs, colour, (token[1], token[2]))
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


def minimax(gs, colour):

    children = possible_children(gs, colour)

    values = []
    for i in range(len(children)):
        values.append(minimax_value(children[i], colour, 1))

    max_value = values[0]
    max_index = 0
    for i in range(len(children)):
        if values[i] > max_value:
            max_index = i
            max_value = values[i]

    return children[max_index][1]


def minimax_value(operation, colour, depth):

    gs = operation[0]

    other = other_colour(colour)

    if depth >= 2:
        return utility_value(gs, colour)
    else:
        if depth % 2 == 0:
            children = possible_children(gs, colour)
            if children == []:
                return utility_value(gs, colour)
            else:
                return max(list(map(lambda op: minimax_value(op, colour, depth+1), children)))
        else:
            children = possible_children(gs, other)
            if children == []:
                return utility_value(gs, colour)
            else:
                return min(list(map(lambda op: minimax_value(op, colour, depth+1), children)))


def utility_value(gs, colour):
    other = other_colour(colour)

    nb_mine = 0
    for token in gs[colour]:
        nb_mine += token[0]

    nb_other = 0
    for token in gs[other]:
        nb_other += token[0]

    return nb_mine - nb_other


def other_colour(colour):
    if colour == "white":
        return "black"
    else:
        return "white"