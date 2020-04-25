# pylint: disable=import-error
# pylint: disable=no-name-in-module

import csv
import os
import pathlib
from util import possible_children, other_colour


def sort_gs(gs):
    """ Sorts the lists of tokens in the gamestate """
    gs["white"].sort()
    gs["black"].sort()


def flat_tuple(gs):
    """ This function turns the gamestate in a tuple of tuples, in order to make it hashable """
    return (tuple(map(tuple, gs["white"])), tuple(map(tuple, gs["black"])))


def reverse_flat_tuple(gs_tuple):
    return {"white": list(map(list, gs_tuple[0])), "black": list(map(list, gs_tuple[1]))}


def add_opening_move(gs, colour, move, symetric=True, replace=False):
    book = read_opening_moves()
    with open(os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), "opening_moves.csv"), "w", newline='') as csvfile:
        w = csv.writer(csvfile, delimiter=";")
        sort_gs(gs)
        if (flat_tuple(gs), colour) not in book or replace:
            book[(flat_tuple(gs), colour)] = move

        if symetric:
            symetric_gs = {"white": [], "black": []}
            for token in gs["white"]:
                symetric_gs["black"].append([token[0], 7-token[1], 7-token[2]])
            for token in gs["black"]:
                symetric_gs["white"].append([token[0], 7-token[1], 7-token[2]])
            sort_gs(symetric_gs)
            if move[0] == "MOVE":
                new_move = ("MOVE", move[1], (7-move[2][0], 7-move[2][1]), (7-move[3][0], 7-move[3][1]))
            else:
                new_move = ("BOOM", (7-move[1][0], 7-move[1][1]))
            new_colour = other_colour(colour)
            if (flat_tuple(symetric_gs), new_colour) not in book or replace:
                book[(flat_tuple(symetric_gs), new_colour)] = new_move

        for (gs_tuple, colour) in book.keys():
            w.writerow([str((reverse_flat_tuple(gs_tuple), colour)), str(book[(gs_tuple, colour)])])


def read_opening_moves():
    with open(os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), "opening_moves.csv"), newline='') as csvfile:
        book = {}
        r = csv.reader(csvfile, delimiter=";")
        for row in r:
            (gs, colour) = eval(row[0])
            move = eval(row[1])
            book[(flat_tuple(gs), colour)] = move
    return book


# for child in possible_children({
#     "white": [[1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1], [1, 3, 0], [1, 3, 1], [1, 4, 0], [1, 4, 1], [1, 6, 0], [1, 6, 1], [1, 7, 0], [1, 7, 1]],
#     "black": [[1, 0, 7], [1, 0, 6], [1, 1, 7], [1, 1, 6], [1, 3, 7], [1, 3, 6], [1, 4, 7], [1, 4, 6], [1, 6, 7], [1, 6, 6], [1, 7, 7], [1, 7, 6]]
# }, "black"):
#     add_opening_move(child[0], "white", ("MOVE", 1, (3, 1), (3, 2)), replace=True)


# add_opening_move({
#     "white": [[1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1], [1, 3, 0], [1, 3, 1], [1, 4, 0], [1, 4, 1], [1, 6, 0], [1, 6, 1], [1, 7, 0], [1, 7, 1]],
#     "black": [[1, 0, 7], [1, 0, 6], [1, 1, 7], [1, 1, 6], [1, 3, 7], [1, 3, 6], [1, 4, 7], [1, 4, 6], [1, 6, 7], [1, 6, 6], [1, 7, 7], [1, 7, 6]]
# }, "white", ("MOVE", 1, (3, 1), (3, 2)), replace=True)


print(read_opening_moves())
