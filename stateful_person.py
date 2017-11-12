from master_person import Person
from probability import P_n

FERT0 = 15
FERT1 = 55


class StatePerson(Person):

    def __init__(self, dna):
        self.dna = dna
        Person.__init__(self, dna)
        self.state = 'HEALTHY'
        self.states = [(self.healthy, 1.0), (self.sick, 0.0),
                       (self.hungry, 0.0), (self.dead, 0.0),
                       (self.reproduce, 0.0)]

    def healthy(self):
        self.state = 'HEALTHY'
        if self.gender == 'female' and self.age in range(FERT0, FERT1 + 1):
            self.states = [(self.healthy, 0.3), (self.sick, 0.1),
                           (self.hungry, 0.5), (self.dead, 0.0),
                           (self.reproduce, 0.2)]
        else:
            self.states = [(self.healthy, 0.3), (self.sick, 0.2),
                           (self.hungry, 0.5), (self.dead, 0.0),
                           (self.reproduce, 0.0)]

    def hungry(self):
        self.state = 'HUNGRY'
        self.states = [(self.healthy, 0.6), (self.sick, 0.15),
                       (self.hungry, 0.25), (self.dead, 0.0),
                       (self.reproduce, 0.0)]

    def sick(self):
        self.state = 'SICK'
        self.states = [(self.healthy, 0.4), (self.sick, 0.4),
                       (self.hungry, 0.1), (self.dead, 0.1),
                       (self.reproduce, 0.0)]

    def dead(self):
        self.state = 'DEAD'
        self.states = [(self.healthy, 0.0), (self.sick, 0.0),
                       (self.hungry, 0.0), (self.dead, 1.0),
                       (self.reproduce, 0.0)]

    def reproduce(self):
        self.state = 'REPRODUCE'
        self.states = [(self.healthy, 0.8), (self.sick, 0.0),
                       (self.hungry, 0.1), (self.dead, 0.0),
                       (self.reproduce, 0.1)]

    def step(self):
        if self.state == 'DEAD':
            pass
        else:
            self.age += 1
            result = P_n(self.states)
            result()

    def __str__(self):
        msg = (self.state, self.age, self.name,
               self.gender, self.children, self.dna)
        return str(msg)
