
import os
import csv
from math import tanh
from tdleaf_pybros.util import evaluation, features


def train(states_list, colour):

    with open(os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), "weights.csv"), newline='') as csvfile:
        r = csv.reader(csvfile, delimiter=";")
        row = next(r)
        header = next(r)
        w = list(map(float, row))

    old_w = w.copy()
    print(old_w)
    d = []
    print(states_list)
    N = len(states_list)

    for i in range(N-1):
        d.append(states_list[i+1][0] - states_list[i][0])

    print(d)

    for i in range(N-1):
        features_i = features(states_list[i][1], colour)
        for j in range(len(features_i)):
            w[j] += 1*((1-tanh(evaluation(states_list[i][1], colour, old_w))**2) *
                         features_i[j])*sum([(0.2**(m-i))*d[m] for m in range(i, N-1)])

    with open(os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), "weights.csv"), "w", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(w)
        writer.writerow(header)

    print(w)
