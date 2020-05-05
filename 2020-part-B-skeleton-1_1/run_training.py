
import subprocess

def run_training(nb_games):
    for _ in range(nb_games):
        subprocess.run("python -m referee -v 0 tdleaf_pybros pybros")
        subprocess.run("python -m referee -v 0 pybros tdleaf_pybros")

run_training(5)