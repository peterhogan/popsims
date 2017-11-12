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


class Person:

    def __init__(self, dna={}):
        self.age = 0
        self.gender = choice(['male', 'female'])
        self.dna = dna
        if len(self.dna) > 0:
            self.dna['gen'] += 1
        else:
            self.dna['gen'] = 0
        self.generation = self.dna['gen']
        self.state = 'HEALTHY'
        self.all_states = [(self.healthy, 1.0), (self.sick, 0.0),
                           (self.dead, 0.0), (self.reproduce, 0.0)]

    def step(self):
        if self.state == 'DEAD':
            pass
        else:
            self.age += 1
            result = P_n(self.all_states)
            result()

    def healthy(self):
        self.state = 'HEALTHY'
        if self.gender == 'female':
            if self.age in range(FERT_START, FERT_END):
                self.all_states = [(self.healthy, 0.7), (self.sick, 0.1),
                                   (self.dead, 0.0), (self.reproduce, 0.2)]
            else:
                self.all_states = [(self.healthy, 0.7), (self.sick, 0.3),
                                   (self.dead, 0.0), (self.reproduce, 0.0)]
        else:
            self.all_states = [(self.healthy, 0.65), (self.sick, 0.35),
                               (self.dead, 0.0), (self.reproduce, 0.0)]

    def sick(self):
        self.state = 'SICK'
        self.all_states = [(self.healthy, 0.5), (self.sick, 0.4),
                           (self.dead, 0.1), (self.reproduce, 0.0)]

    def dead(self):
        self.state = 'DEAD'
        self.all_states = [(self.healthy, 0.0), (self.sick, 0.0),
                           (self.dead, 1.0), (self.reproduce, 0.0)]

    def reproduce(self):
        self.state = 'REPRODUCING'
        self.all_states = [(self.healthy, 1.0), (self.sick, 0.0),
                           (self.dead, 0.0), (self.reproduce, 0.0)]

    def __str__(self):
        return str((self.gender, self.age, self.generation, self.state))


class Sim:

    def __init__(self, initpop, simlength):
        self.initpop = initpop
        self.simlength = simlength
        self.extinction = False
        self.children_born = 0

    def run(self):
        start = time()
        pop = [Person() for i in range(self.initpop)]
        for i in trange(self.simlength):
            if len(pop) == 0:
                self.extinction = True
                break
            for person in pop:
                person.step()
                if person.state == 'REPRODUCING':
                    pop.append(Person(dna=person.dna))
                    self.children_born += 1
                elif person.state == 'DEAD':
                    pop.remove(person)
        self.finish(start, pop)

    def finish(self, start, pop):
        if self.extinction:
            print('EXTINCTION!')
        elif cli.output:
            left = [p for p in pop if p.state != 'DEAD']
            max_gen = max([i.generation for i in pop])
            min_gen = min([i.generation for i in pop])
            avg_age = mean([i.age for i in pop])
            print(str(len(left)), 'still alive...')
            print("Generation gap: ({}, {})".format(max_gen, min_gen))
            print("Average age: {}".format(avg_age))
            print("Children born: {}".format(self.children_born))
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
    s = Sim(cli.initial_population, cli.simulation_length)
    s.run()
