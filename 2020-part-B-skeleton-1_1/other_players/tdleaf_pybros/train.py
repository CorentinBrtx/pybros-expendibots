
import os
import csv
from math import tanh
from tdleaf_pybros.util import Minimax


def train(states_list, colour):

    with open(os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), "weights.csv"), newline='') as csvfile:
        r = csv.reader(csvfile, delimiter=";")
        row = next(r)
        header = next(r)
        w = list(map(float, row))

    old_w = w.copy()
    print(old_w)
    d = []
    N = len(states_list)

    for i in range(N-1):
        d.append(states_list[i+1][0] - states_list[i][0])

    # print(d)

    minimax = Minimax(colour, old_w, 1, 1)

    for i in range(N-1):
        features_i = minimax.features(states_list[i][1])
        # print(features_i)
        for j in range(len(features_i)-1):
            w[j] += 0.1*((1-tanh(minimax.evaluation(states_list[i][1]))**2) *
                         features_i[j])*sum([(0.2**(m-i))*d[m] for m in range(i, N-1)])

    with open(os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), "weights.csv"), "w", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(w)
        writer.writerow(header)

    print(w)
