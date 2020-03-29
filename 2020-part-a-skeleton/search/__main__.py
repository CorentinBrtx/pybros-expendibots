import sys
import json

# pylint: disable=import-error

from search.util import print_move, print_boom, print_board
from search.useful import getCoords, distance

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    me = getCoords(data["white"][0])
    target = getCoords(data["black"][0])

    while distance(me,target) > 1:
        if me[0]<(target[0]-1):
            print_move(1, me[0], me[1], (me[0]+1), me[1])
            me[0] += 1
        elif me[1]<(target[1]-1):
            print_move(1, me[0], me[1], me[0], (me[1]+1))
            me[1] += 1
        elif me[0]>(target[0]+1):
            print_move(1, me[0], me[1], (me[0]-1), me[1])
            me[0] -= 1
        else:
            print_move(1, me[0], me[1], me[0], (me[1]-1))
            me[1] -= 1

    print_boom(me[0], me[1])




if __name__ == '__main__':
    main()
