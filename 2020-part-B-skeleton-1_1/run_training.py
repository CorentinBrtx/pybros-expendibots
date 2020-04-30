
import subprocess

def run_training(nb_games):
    for _ in range(nb_games):
        subprocess.run("python -m referee -s 100 -v 2 -d -1 pybros tdleaf_pybros")

run_training(1)