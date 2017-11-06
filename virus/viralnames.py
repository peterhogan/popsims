from random import sample
from csv import reader

with open('viral_pairs.txt', 'r') as pairs:
    all_pairs = list(reader(pairs))


def get_virus_pair():
    return sample(all_pairs, 1)[0]


def get_virus_name():
    return sample(set([i[0] for i in all_pairs]), 1)[0]


def get_virus_family():
    return sample(set([i[1] for i in all_pairs]), 1)[0]
