from random import sample
from collections import Counter
from tqdm import trange
from time import time
from argparse import ArgumentParser
from statistics import mean
from stateful_person import StatePerson
import matplotlib.pyplot as plt

INITAL_POPULATION = 1000
SIMULATION_LENGTH = 500
FERT_START = 16
FERT_END = 50


class Sim:

    x, y1 = [], []

    def __init__(self, entitytype, initpop, simlength):
        self.entitytype = entitytype
        self.initpop = initpop
        self.simlength = simlength
        self.extinction = False
        self.children_born = 0
        self.population = [self.entitytype({})
                           for i in trange(self.initpop)]

    def capture(self, i):
        self.x.append(i)
        self.y1.append(len(self.population)/self.initpop)

    def run(self):
        start = time()
        for i in trange(self.simlength):
            if i % 10 == 0:
                self.capture(i)
            if len(self.population) == 0:
                self.extinction = True
                break
            for entity in self.population:
                entity.step()
                if entity.state == 'REPRODUCE':
                    self.population.append(self.entitytype(entity.dna))
                    entity.children += 1
                    self.children_born += 1
                elif entity.state == 'DEAD':
                    self.population.remove(entity)
        self.finish(start, self.population)

    def finish(self, start, pop):
        if self.extinction:
            print('EXTINCTION!')
        elif cli.output:
            left = [p for p in pop if p.state != 'DEAD']
            max_gen = max([i.dna['generation'] for i in pop])
            min_gen = min([i.dna['generation'] for i in pop])
            avg_age = mean([i.age for i in pop])
            all_surs = Counter([i.dna['surname'] for i in pop])
            print(str(len(left)), 'still alive...')
            print("Generation gap: ({}, {})".format(max_gen, min_gen))
            print("Average age: {}".format(avg_age))
            print("Children born: {}".format(self.children_born))
            print("All Surnames: {}".format(all_surs))
            if cli.sample_output:
                if len(pop) < 5:
                    samp = pop
                else:
                    samp = sample(pop, 5)
                for i in samp:
                    print(i)
            elif cli.full_output:
                for i in pop:
                    print(i)
        print('time taken: {}'.format(time() - start))
        if cli.barchart:
            self.barchart()

    def barchart(self):
        plt.plot(self.x, self.y1, alpha=0.6, label='Population')
        plt.legend()
        plt.show()


parser = ArgumentParser()
parser.add_argument('--barchart', '-b', action='store_true',
                    default=False)
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
    s = Sim(StatePerson, cli.initial_population, cli.simulation_length)
    s.run()
