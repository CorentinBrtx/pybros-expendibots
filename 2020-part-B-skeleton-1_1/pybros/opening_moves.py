import csv
import os
import pathlib


def sort_gs(gs):
    """ Sorts the lists of tokens in the gamestate """
    gs["white"].sort()
    gs["black"].sort()

def flat_tuple(gs):
    """ This function turns the gamestate in a tuple of tuples, in order to make it hashable """
    return tuple(map(tuple, gs["white"] + gs["black"]))


def add_opening_move(gs, move):
    with open(os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), "opening_moves.csv"), "a", newline='') as csvfile:
        w = csv.writer(csvfile, delimiter=";")
        sort_gs(gs)
        book = read_opening_moves()
        if flat_tuple(gs) not in book:
            w.writerow([str(gs), str(move)])


def read_opening_moves():
    with open(os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), "opening_moves.csv"), newline='') as csvfile:
        book = {}
        r = csv.reader(csvfile, delimiter=";")
        for row in r:
            gs = eval(row[0])
            move = eval(row[1])
            book[flat_tuple(gs)] = move
    return book

add_opening_move({
    "white": [[1, 0, 0], [1, 0, 2], [1, 1, 0], [1, 1, 1], [1, 3, 0], [1, 3, 1], [1, 4, 0], [1, 4, 1], [1, 6, 0], [1, 6, 1], [1, 7, 0], [1, 7, 1]],
    "black": [[1, 0, 7], [1, 0, 6], [1, 1, 7], [1, 1, 6], [1, 3, 7], [1, 3, 6], [1, 4, 7], [1, 4, 6], [1, 6, 7], [1, 6, 6], [1, 7, 7], [1, 7, 6]]
}, ("MOVE", 1, (0, 1), (0, 2)))

print(read_opening_moves())

