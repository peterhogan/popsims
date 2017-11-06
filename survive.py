import numpy as np
from statistics import mean, StatisticsError
from random import randint,random,sample
from names import get_first_name
from tqdm import tqdm,trange
from time import time
from argparse import ArgumentParser
import matplotlib.pyplot as plt

parser = ArgumentParser()
parser.add_argument('--verbose','-v',action='store_true')
parser.add_argument('--running','-r',action='store_true')
parser.add_argument('--population','-p',action='store')
parser.add_argument('--length','-l',action='store')
parser.add_argument('--barchart','-b',action='store_true')
clargs = parser.parse_args()

if clargs.population is not None: INITIAL_POPULATION = int(clargs.population)
else: INITIAL_POPULATION = 1000
if clargs.length is not None: SIMULATION_LENGTH = int(clargs.length)
else: SIMULATION_LENGTH = 500
REPRODUCTIVE_RATE = 40
AVERAGE_AGE = 28
AGE_VARIANCE = 5
INCREMENT = 1
DISEASE_RATE = 15
START = time()
FRMT = "Entity: {:12} Age: {:4} Sex: {:7} DNA: {:3} Children: {:3}"

class Entity:

    def __init__(self, alive=True, dna=None):
        self.alive = alive
        self.gender = np.random.choice(['male', 'female'])
        self.diseased = False
        self.unwell = False
        self.dna = dna
        if self.dna is not None:
            self.dna = {'mortality_index': abs(np.random.normal(loc=dna['mortality_index'],scale=2)),
                        'reproductive_rate': int(abs(np.random.normal(loc=dna['reproductive_rate'],scale=10))),
                        'immunity': int(abs(np.random.normal(loc=dna['immunity'],scale=5))),
                        'generation': dna['generation'] + 1
                        }
        else:
            self.dna = {'mortality_index': np.random.normal(loc=AVERAGE_AGE, scale=AGE_VARIANCE),
                        'reproductive_rate': int(abs(np.random.normal(loc=REPRODUCTIVE_RATE,scale=10))),
                        'immunity': int(abs(np.random.normal(loc=1,scale=1))),
                        'generation': 1
                        }
        self.lifespan = abs(np.random.normal(loc=self.dna['mortality_index'], scale=5))
        self.name = get_first_name(gender=self.gender)
        self.life = float(self.lifespan)
        self.years_old = 0
        self.children = 0
        if self.gender == 'female':
            self.fertile_range = (int(float(self.lifespan)*0.2), int(float(self.lifespan)*0.6))
            #self.fertile_range = (16, 50)
            self.reproduce = False

    def __str__(self):
        return self.name

    def age(self):
        if not self.alive:
            pass
        self.life -= INCREMENT
        self.years_old += INCREMENT
        if randint(0,self.dna['immunity']) == 0:
            if self.unwell:
                self.unwell = False
            else:
                self.unwell = True
        if self.gender == 'female' and self.years_old in range(self.fertile_range[0],self.fertile_range[1]):
            reproductive_index = randint(0,self.dna['reproductive_rate'] + int(self.children/2))
            if reproductive_index == 0:
                self.reproduce = True
        if self.life <= 0:
            self.alive = False

class Population:

    def __init__(self, size, iterations, dis_rt):
        self.size = size
        self.iterations = iterations
        self.population = [ Entity() for i in trange(self.size) ]
        self.disease_rate = dis_rt

    def generation(self,f):
        try:
            return f([float(i.dna['generation']) for i in self.population])
        except (StatisticsError, ValueError):
            return 0

    def immunity(self, f):
        try:
            return f([float(i.dna['immunity']) for i in self.population])
        except (StatisticsError, ValueError):
            return 0

    def lifespan(self, f):
        try:
            return f([float(i.lifespan) for i in self.population])
        except (StatisticsError, ValueError):
            return 0

    def fertility(self, f):
        try:
            return f([float(i.dna['reproductive_rate']) for i in self.population])
        except (StatisticsError, ValueError):
            return 0

    def children(self, f):
        try:
            return f([float(i.children) for i in self.population if i.gender == 'female'])
        except (StatisticsError, ValueError):
            return 0

    def start(self):
        x,y1,y2,y3,y4,y5,y6,y7,y8,y9 = [],[],[],[],[],[],[],[],[],[]
        for i in range(self.iterations):
            if len(self.population)/self.size < 0.1:
                self.disease_rate += 1
            if len(self.population)/self.size > 1.5 and self.disease_rate > 0:
                self.disease_rate -= 1
            if len(self.population) == 0:
                break
            if i % 10 == 0:
                x.append(i)
                y1.append(len(self.population)/100)
                y2.append(self.immunity(mean))
                y3.append(self.lifespan(mean))
                y4.append(self.generation(max))
                y5.append(self.fertility(mean))
                y6.append(self.children(mean))
                y7.append(len([i for i in self.population if i.unwell])/100)
                y8.append(len([i for i in self.population if i.diseased])/100)
                y9.append(100/1+self.disease_rate)
            if clargs.running:
                if i % 10 == 0:
                    form = 'Population: {} Average Lifespan: {:4} Iteration: {}'
                    print(form.format(len(self.population),round(self.lifespan(mean),2), i))
            for ent in self.population:
                ent.age()
                if ent.unwell and randint(0,self.disease_rate) == 0:
                    ent.diseased = True
                if ent.diseased:# and ent.years_old not in range(10,40):
                    ent.alive = False
                if ent.gender == 'female' and ent.reproduce:
                    ent.reproduce = False
                    ent.children += 1
                    self.population.append(Entity(dna = ent.dna))
                if not ent.alive:
                    self.population.remove(ent)
        if clargs.barchart and len(self.population) != 0:
            plt.plot(x,y1, alpha=0.6, label='Population')
            plt.plot(x,y2, alpha=0.6, color='green', label='Average Immunity')
            plt.plot(x,y3, alpha=0.5, color='yellow', label='Average Lifespan')
            plt.plot(x,y4, alpha=0.4, color='red', label='Max Generation')
            plt.plot(x,y5, alpha=0.4, color='purple', label='Average Fertility')
            plt.plot(x,y6, alpha=0.4, color='pink', label='Average Children')
            plt.plot(x,y7, alpha=0.4, color='black', label='Unwell')
            plt.plot(x,y8, alpha=0.4, label='Diseased')
            #plt.plot(x,y9, alpha=0.6, label='Disease Rate')
            plt.legend()
            plt.show()
        if clargs.verbose:
            try:
                for ent in sample(self.population,10):
                    print(FRMT.format(str(ent), ent.years_old, ent.gender, str(ent.dna), ent.children))
            except ValueError:
                for ent in self.population:
                    print(FRMT.format(str(ent), ent.years_old, ent.gender, str(ent.dna), ent.children))
        print('Population: {}'.format(len(self.population)))


def main():
    print('Populating ...')
    p = Population(INITIAL_POPULATION, SIMULATION_LENGTH, DISEASE_RATE)
    print('Average lifespan: %r' % p.lifespan(mean))
    print('Maximum lifespan: %r' % p.lifespan(max))
    print('Running simulation...')
    p.start()
    print('Population left: {}%'.format(100*len(p.population)/INITIAL_POPULATION))

if __name__ == '__main__':
    main()
    print('Time Taken: {:10}'.format(round(time() - START,3)))
