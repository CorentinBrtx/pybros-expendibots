
from math import inf, tanh


class Minimax:

    def __init__(self, colour, weights, turn, time_left):

        self.colour = colour
        self.weights = weights
        self.turn = turn
        self.enemy = self.enemy_colour(self.colour)
        self.time_left = time_left

    def best_action(self, gs):
        """
        Returns the best action to make using minimax strategy.

        - The maximum depth is set depending on the number of tokens remaining, and the
        time remaining.
        - The extra_depth allows to search one step further, but this step only allows
        to boom and not to move
        """

        nb_mine = 0
        for token in gs[self.colour]:
            nb_mine += token[0]

        if self.time_left < 10:
            max_depth = 2
            extra_depth = True
        elif nb_mine <= 6 and self.time_left < 20:
            max_depth = 3
            extra_depth = True
        elif self.time_left < 20 and nb_mine >= 10:
            max_depth = 2
            extra_depth = True
        elif self.time_left < 20:
            max_depth = 3
            extra_depth = False
        elif nb_mine <= 2:
            max_depth = 5
            extra_depth = True
        elif nb_mine <= 6:
            max_depth = 4
            extra_depth = True
        elif nb_mine <= 10 or (self.time_left > 40 and self.turn > 2):
            max_depth = 3
            extra_depth = True
        else:
            max_depth = 3
            extra_depth = False

        alpha = -inf
        beta = inf
        best_move = None

        children = self.possible_children(gs, self.colour)

        for child in children:
            value = self.minimax_value(child[0], 1, alpha, beta, max_depth, extra_depth)
            if value > alpha:
                best_move = child[1]
                alpha = value

        return best_move

    def minimax_value(self, gs, depth, alpha, beta, max_depth, extra_depth):

        dead = (len(gs[self.colour]) == 0)
        enemy_dead = (len(gs[self.enemy]) == 0)

        if dead and enemy_dead:
            return 0
        elif dead:
            return -1
        elif enemy_dead:
            return 1

        elif depth >= max_depth:
            if extra_depth:
                if depth % 2 == 0:
                    value = self.minimax_value(gs, depth+1, alpha, beta, max_depth, False)
                    if value > alpha:
                        alpha = value
                    if alpha >= beta:
                        return beta
                    for child in self.possible_children_boom(gs, self.colour):
                        value = self.minimax_value(child[0], depth+1, alpha, beta, max_depth, False)
                        if value > alpha:
                            alpha = value
                        if alpha >= beta:
                            return beta
                    return alpha
                else:
                    value = self.minimax_value(gs, depth+1, alpha, beta, max_depth, False)
                    if value < beta:
                        beta = value
                    if beta <= alpha:
                        return alpha
                    for child in self.possible_children_boom(gs, self.enemy):
                        value = self.minimax_value(child[0], depth+1, alpha, beta, max_depth, False)
                        if value < beta:
                            beta = value
                        if beta <= alpha:
                            return alpha
                    return beta

            else:
                return tanh(self.evaluation(gs))

        else:
            if depth % 2 == 0:
                for child in self.possible_children(gs, self.colour):
                    value = self.minimax_value(child[0], depth+1, alpha, beta, max_depth, extra_depth)
                    if value > alpha:
                        alpha = value
                    if alpha >= beta:
                        return beta
                return alpha
            else:
                for child in self.possible_children(gs, self.enemy):
                    value = self.minimax_value(child[0], depth+1, alpha, beta, max_depth, extra_depth)
                    if value < beta:
                        beta = value
                    if beta <= alpha:
                        return alpha
                return beta

    def evaluation(self, gs):

        f = self.features(gs)

        return sum([self.weights[i]*f[i] for i in range(len(f))])

    def features(self, gs):

        total_mine = 0
        total_enemy = 0
        total_neighbours = 0
        agressivity = 0

        nb_mine = len(gs[self.colour])
        nb_enemy = len(gs[self.enemy])

        for token in gs[self.enemy]:
            total_enemy += token[0]

        for i in range(nb_mine):
            stack = gs[self.colour][i][0]
            token = gs[self.colour][i]
            total_mine += stack

            for j in range(i+1, nb_mine):
                if self.within_reach(token, gs[self.colour][j]):
                    total_neighbours += 2

            for j in range(nb_enemy):
                agressivity += stack*gs[self.enemy][j][0] * \
                    self.distance(token, gs[self.enemy][j])

        return [total_mine/12,
                total_enemy/12,
                total_neighbours/(8*nb_mine+1)-(1/8),
                ((total_mine+1)/(total_enemy+1))-1,
                agressivity/(6*total_mine*total_enemy+1)-0.7]

    def distance(self, t1, t2):
        """ 
        Returns the "boom" distance between two tokens
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

    def within_reach(self, t1, t2):
        """
        Returns True if t1 and t2 and in an explosion radius (1 square apart)
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
            return difx <= 1
        else:
            return dify <= 1

    def manhattan_distance(self, t1, t2):
        """ 
        Returns the manhattan distance between two tokens
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

    def boom(self, gameState, boomed_token, groups):
        """ 
        This function return the new gamestate after the explosion of the stack of tokens placed in (x,y),
        and the action in the requested format
        """

        new_gs = {"white": gameState["white"].copy(), "black": gameState["black"].copy()}

        for group in groups:
            if boomed_token in group:
                for token in group:
                    try:
                        new_gs["white"].remove(token)
                    except:
                        new_gs["black"].remove(token)
                break

        return (new_gs, ("BOOM", (boomed_token[1], boomed_token[2])))

    def move(self, gameState, colour, token_moved, action):
        """ 
        This function returns the new gamestate after moving the token as specified, along with the
        action in the requested format
        """

        (n, (x1, y1), (x2, y2)) = action

        gameStateCopy = {"white": gameState["white"].copy(), "black": gameState["black"].copy()}

        tokens_on_target = self.occupied_mine(gameStateCopy, colour, x2, y2)

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

    def occupied_mine(self, gs, colour, x, y):
        """ 
        Returns the number of your tokens on the specified position (None if there isn't any)
        """
        for token in gs[colour]:
            if (token[1], token[2]) == (x, y):
                return token
        return None

    def occupied_enemy(self, gs, colour, x, y):
        """ 
        Returns True if there is an enemy token on the specified position, False otherwise 
        """
        other = self.enemy_colour(colour)

        for token in gs[other]:
            if (token[1], token[2]) == (x, y):
                return True
        return False

    def possible_children(self, gs, colour):
        """ 
        This function returns all the gamestates reachable from the current one with one action
        """

        groups = self.group_tokens(gs, colour)
        my_groups = self.group_my_tokens(gs, colour)
        for group in my_groups:
            yield self.boom(gs, group[0], groups)
        for token in gs[colour]:
            for i in range(token[0], 0, -1):
                if (token[2]+i) <= 7 and not(self.occupied_enemy(gs, colour, token[1], token[2]+i)):
                    for k in range(1, token[0]+1):
                        yield self.move(gs, colour, token, (k, (token[1], token[2]), (token[1], token[2]+i)))
                if (token[2]-i) >= 0 and not(self.occupied_enemy(gs, colour, token[1], token[2]-i)):
                    for k in range(1, token[0]+1):
                        yield self.move(gs, colour, token, (k, (token[1], token[2]), (token[1], token[2]-i)))
                if (token[1]+i) <= 7 and not(self.occupied_enemy(gs, colour, token[1]+i, token[2])):
                    for k in range(1, token[0]+1):
                        yield self.move(gs, colour, token, (k, (token[1], token[2]), (token[1]+i, token[2])))
                if (token[1]-i) >= 0 and not(self.occupied_enemy(gs, colour, token[1]-i, token[2])):
                    for k in range(1, token[0]+1):
                        yield self.move(gs, colour, token, (k, (token[1], token[2]), (token[1]-i, token[2])))

    def group_tokens(self, gs, colour):
        """
        Returns a list of groups of tokens that boom together
        """

        enemy = self.enemy_colour(colour)

        all_tokens = gs[colour]+gs[enemy]
        nb_tokens = len(all_tokens)
        nb_my_tokens = len(gs[colour])
        groups = []
        grouped = [False for _ in range(nb_tokens)]

        for i in range(nb_my_tokens):
            if not grouped[i]:
                grouped[i] = True
                new_group = [all_tokens[i]]
                border = [all_tokens[i]]
                while border:
                    token = border.pop()
                    for j in range(i+1, nb_tokens):
                        if not grouped[j] and self.within_reach(all_tokens[j], token):
                            new_group.append(all_tokens[j])
                            border.append(all_tokens[j])
                            grouped[j] = True
                groups.append(new_group)

        return groups

    def group_my_tokens(self, gs, colour):
        """
        Returns a list of groups of your tokens that boom together
        """

        my_tokens = gs[colour]
        nb_tokens = len(my_tokens)
        groups = []
        grouped = [False for _ in range(nb_tokens)]

        for i in range(nb_tokens):
            if not grouped[i]:
                grouped[i] = True
                new_group = [my_tokens[i]]
                border = [my_tokens[i]]
                while border:
                    token = border.pop()
                    for j in range(i+1, nb_tokens):
                        if not grouped[j] and self.within_reach(my_tokens[j], token):
                            new_group.append(my_tokens[j])
                            border.append(my_tokens[j])
                            grouped[j] = True
                groups.append(new_group)

        return groups

    def group_enemy_tokens(self, gs, colour):
        """
        Returns a list of groups of the enemy's tokens that boom together
        """

        enemy = self.enemy_colour(colour)

        nb_others = len(gs[enemy])
        groups = []
        grouped = [False for _ in range(nb_others)]

        for i in range(nb_others):
            if not grouped[i]:
                grouped[i] = True
                new_group = [gs[enemy][i]]
                not_grouped = len([t for t in grouped if not(t)])
                for _ in range(not_grouped):
                    for j in range(i+1, nb_others):
                        if not grouped[j]:
                            for token in new_group:
                                if self.distance(gs[enemy][j], token) <= 1:
                                    new_group.append(gs[enemy][j])
                                    grouped[j] = True
                                    break
                groups.append(new_group)

        return groups

    def possible_children_boom(self, gs, colour):
        """ 
        This function returns all the gamestates reachable from the current one within one boom
        """

        groups = self.group_tokens(gs, colour)
        my_groups = self.group_my_tokens(gs, colour)
        for group in my_groups:
            yield self.boom(gs, group[0], groups)

    def enemy_colour(self, colour):
        """ 
        Returns the colour of the enemy
        """
        if colour == "white":
            return "black"
        else:
            return "white"
