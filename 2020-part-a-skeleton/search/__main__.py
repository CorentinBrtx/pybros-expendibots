import sys
import json
import time

# pylint: disable=import-error

from search.util import print_move, print_boom, print_board, print_gamestate
from search.useful import bfs

def main():
    start_time = time.time()
    with open(sys.argv[1]) as file:
        data = json.load(file)

    bfs(data)
    print("# Time of execution : " + str(time.time() - start_time))

if __name__ == '__main__':
    main()
