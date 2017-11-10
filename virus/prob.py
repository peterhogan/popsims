from random import randint
import sys
from tqdm import trange


def P(x):
    if x == 1:
        return True
    elif x == 0:
        return False
    # num = format(x, '.10f').split('.')
    num = str(x).split('.')
    dec = num[1]
    multi = len(dec)
    numerator = int(x * 10**multi)
    choice = randint(1, 10**multi)
    if choice <= numerator:
        return True
    elif choice > numerator:
        return False


def assess(n, p):
    hits = 0
    misses = 0
    for i in trange(int(n)):
        prob = P(float(p))
        if prob:
            hits += 1
        else:
            misses += 1
    print(hits/int(n))


if __name__ == '__main__':
    assess(sys.argv[1], sys.argv[2])
