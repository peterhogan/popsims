from random import randint
from collections import Counter
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


def P_n(l):
    sample_space = [0]
    multi = max([len(str(i[1]).split('.')[1]) for i in l])
    for name, p in l:
        numerator = int(p * 10**multi)
        sample_space.append(sample_space[-1] + numerator)
    choice = randint(0, sample_space[-1]-1)
    index = 0
    for i in range(len(sample_space)):
        try:
            if sample_space[i] <= choice < sample_space[i+1]:
                index = i
                break
        except IndexError:
            if sample_space[i] <= choice:
                index = i
    return l[index][0]


def assessPn(l, n):
    results = []
    for i in trange(int(n)):
        results.append(P_n(l))
    return Counter(results)


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
    ls = [('A', 0.55), ('B', 0.05), ('C', 0.1), ('D', 0.1), ('E', 0.1), ('F', 0.1)]
    print(ls)
    cnt = assessPn(ls, int(sys.argv[1]))
    sm = []
    for k, v in cnt.items():
        print(k, v/int(sys.argv[1]))
        sm.append(v/int(sys.argv[1]))
    print(sum(sm))
    # assess(sys.argv[1], sys.argv[2])
