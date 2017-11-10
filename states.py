from probability import P_n
from tqdm import trange
from time import time
import sys

class Person:

    def __init__(self):
        self.state = 'HEALTHY'
        self.all_states = [(self.healthy, 1.0),(self.sick, 0.0),
                           (self.dead, 0.0),(self.reproduce, 0.0)]

    def step(self):
        if self.state == 'DEAD':
            pass
        else:
            result = P_n(self.all_states)
            result()

    def healthy(self):
        self.state = 'HEALTHY'
        self.all_states = [(self.healthy, 0.65),(self.sick, 0.3),
                           (self.dead, 0.0),(self.reproduce, 0.05)]

    def sick(self):
        self.state = 'SICK'
        self.all_states = [(self.healthy, 0.5),(self.sick, 0.4),
                           (self.dead, 0.1),(self.reproduce, 0.0)]

    def dead(self):
        self.state = 'DEAD'
        self.all_states = [(self.healthy, 0.0),(self.sick, 0.0),
                           (self.dead, 1.0),(self.reproduce, 0.0)]

    def reproduce(self):
        self.state = 'REPRODUCING'
        self.all_states = [(self.healthy, 1.0),(self.sick, 0.0),
                           (self.dead, 0.0),(self.reproduce, 0.0)]

if __name__ == '__main__':
    start = time()
    pop = [Person() for i in range(100)]
    for i in trange(int(sys.argv[1])):
        #print(str(i)+': '+str(len([p for p in pop if p.state != 'DEAD'])))
        for person in pop:
            person.step()
            if person.state == 'REPRODUCING':
                pop.append(Person())
            elif person.state == 'DEAD':
                pop.remove(person)
    print(str(len([p for p in pop if p.state != 'DEAD'])), 'still alive...')
    print('time taken: {}'.format(time() - start))
