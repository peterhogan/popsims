from probability import P_n
from random import choice, sample
from tqdm import trange
from time import time
from argparse import ArgumentParser
from statistics import mean

INITAL_POPULATION = 1000
SIMULATION_LENGTH = 500
FERT_START = 16
FERT_END = 50

class Food:

    def __init__(self):



parser = ArgumentParser()
parser.add_argument('--output', '-o', action='store_true',
                    default=False)
parser.add_argument('--sample-output', action='store_true',
                    default=False)
parser.add_argument('--full-output', action='store_true',
                    default=False)
parser.add_argument('--initial-population', '-i', action='store',
                    type=int, default=INITAL_POPULATION)
parser.add_argument('--simulation-length', '-l', action='store',
                    type=int, default=SIMULATION_LENGTH)
cli = parser.parse_args()

if __name__ == '__main__':
    pass
