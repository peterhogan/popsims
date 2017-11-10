import numpy as np
import matplotlib.pyplot as plt
from viralnames import get_virus_pair
from names import get_first_name
from tqdm import trange
from time import time
from argparse import ArgumentParser
from operator import mul
from functools import reduce
from random import randint
from statistics import mean
from prob import P


def prod(l):
    return reduce(mul, l)


INITIAL_POPULATION = 100000
SIMULATION_LENGTH = 500
FOOD_START = 1000
FOOD_GROW = 2000
REPRODUCTIVE_RATE = 40
AVERAGE_AGE = 50
AGE_VARIANCE = 5
INCREMENT = 1
DISEASE_RATE = 15
START = time()
FRMT = "Entity: {:12} Age: {:4} Sex: {:7} DNA: {:3} Children: {:3}"


class Simulation:

    def __init__(self, size, length, food_init, food_grw):
        self.length = length
        self.size = size
        self.food = Food(food_init, food_grw)
        self.population = [Person(self.food) for i in trange(self.size)]

    def run(self):
        x, y1, y2 = [], [], []
        msg = '{:3}: Pop: {:5} Food: {:5}'
        for i in range(self.length):
            if len(self.population) < 1:
                break
            print(msg.format(i, len(self.population), self.food.total))
            self.food.grow()
            for ent in self.population:
                ent.step()
                if not ent.alive:
                    self.population.remove(ent)
                if ent.gender == 'female':
                    self.birth(ent)
            x.append(i)
            y1.append(len(self.population))
            y2.append(self.food.total)
        print('Population: {}'.format(len(self.population)))
        # self.population_stats()
        self.plot(x, {'Population': y1,
                      'Food': y2})

    def population_stats(self):
        max_gen = max([i.dna['generation'] for i in self.population])
        avg_age = mean([i.dna['avg_age'] for i in self.population])
        avg_cld = mean([i.children for i in self.population
                        if i.gender == 'female'])
        msg = "Max Generation: {:4} Average Age: {:4} Average Children: {:4}"
        print(msg.format(max_gen, avg_age, avg_cld))

    def birth(self, entity):
        chld = entity.children <= 2
        fert = (entity.life_x * 0.25) < entity.age < (entity.life_x * 0.5)
        hung = not entity.hungry
        chnc = randint(0, 1) == 0
        conds = [fert, hung, chld, chnc]
        if prod(conds) == 1:
            entity.children += 1
            self.population.append(Person(self.food, dna=entity.dna))
        else:
            pass

    def plot(self, x, variables):
        for key, value in variables.items():
            plt.plot(x, value, alpha=0.6, label=key)
        plt.legend()
        plt.show()


class Food:

    def __init__(self, starting, growth):
        self.start = starting
        self.total = starting
        self.growth = growth
        self.active = True

    def grow(self):
        # if self.total > 0:
        growth_amt = np.random.normal(loc=self.growth, scale=5)
        self.total += int(growth_amt)
        # else:
        # self.active = False

    def eat(self):
        if self.total > 0:
            self.total -= 1
            return 1
        else:
            # self.active = False
            return 0


class Person:

    def __init__(self, food, dna=None):
        self.alive = True
        self.hungry = False
        self.gender = np.random.choice(['male', 'female'])
        self.name = get_first_name(gender=self.gender)
        self.dna = dna
        if self.dna is not None:
            self.dna = {
                'fertility': int(abs(np.random.normal(
                    loc=dna['fertility'],
                    scale=10))),
                'avg_age': int(abs(np.random.normal(
                    loc=dna['avg_age'],
                    scale=2))),
                'immunity': int(abs(np.random.normal(
                    loc=dna['immunity'],
                    scale=5))),
                'generation': dna['generation'] + 1
                }
        else:
            self.dna = {
                'fertility': int(abs(np.random.normal(
                    loc=REPRODUCTIVE_RATE,
                    scale=10))),
                'avg_age': int(abs(np.random.normal(
                    loc=AVERAGE_AGE,
                    scale=AGE_VARIANCE))),
                'immunity': int(abs(np.random.normal(loc=1, scale=1))),
                'generation': 1
                }
        self.life_x = self.dna.get('avg_age')
        self.age = 0
        self.food = food
        self.blood = []
        if self.gender == 'female':
            self.children = 0

    def step(self):
        self.age += 1
        self.life_x -= 1
        if self.life_x < 1:
            self.alive = False
            return
        self.hunger_fn()
        if self.gender == 'female':
            self.reproduce()

    def hunger_fn(self):
        food_res = self.food.eat()
        if food_res > 0:
            self.hungry = False
        else:
            if self.hungry:
                self.alive = False
            else:
                self.hungry = True

    def reproduce(self):
        pass


def main():
    print('Populating ...')
    p = Simulation(INITIAL_POPULATION,
                   SIMULATION_LENGTH,
                   FOOD_START,
                   FOOD_GROW)
    print('Running simulation...')
    p.run()
    msg = 'Population left: {}%'
    print(msg.format(100*len(p.population)/INITIAL_POPULATION))


if __name__ == '__main__':
    main()
    msg = 'Time taken: {:10}'
    print(msg.format(round(time() - START, 3)))


parser = ArgumentParser()
parser.add_argument('--verbose', '-v', action='store_true')
parser.add_argument('--running', '-r', action='store_true')
parser.add_argument('--population', '-p', action='store')
parser.add_argument('--length', '-l', action='store')
parser.add_argument('--barchart', '-b', action='store_true')
clargs = parser.parse_args()


class Virus:

    def __init__(self, alive=True, dna=None):
        self.alive = alive
        self.name, self.family = get_virus_pair()
        self.dna = dna

        if self.dna is not None:
            self.dna = {
                'reproductive_rate': int(abs(np.random.normal(
                    loc=dna['reproductive_rate'],
                    scale=10))),
                'immunity': int(abs(np.random.normal(
                    loc=dna['immunity'],
                    scale=5))),
                'generation': dna['generation'] + 1
                }
        else:
            self.dna = {
                'mortality_index': np.random.normal(
                    loc=AVERAGE_AGE,
                    scale=AGE_VARIANCE),
                'reproductive_rate': int(abs(np.random.normal(
                    loc=REPRODUCTIVE_RATE,
                    scale=10))),
                'immunity': int(abs(np.random.normal(loc=1, scale=1))),
                'generation': 1
                }
        self.lifespan = abs(np.random.normal(
            loc=self.dna['mortality_index'],
            scale=5))
        self.years_old = 0
        self.children = 0
        if self.gender == 'female':
            self.fertile_range = (int(float(self.lifespan)*0.2),
                                  int(float(self.lifespan)*0.6))
            self.reproduce = False

    def __str__(self):
        return self.name

    def age(self):
        self.life -= INCREMENT
        self.years_old += INCREMENT
        if self.gender == 'female':
            pass
        if self.life <= 0:
            self.alive = False
