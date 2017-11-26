from popsim.stateful_person import StatePerson


class EatingPerson(StatePerson):

    def __init__(self, dna, foodsource):
        self.dna = dna
        StatePerson.__init__(self, dna)
        self.food = foodsource

    def hungry(self):
        self.state = 'HUNGRY'
        eat = self.food.eat()
        if eat > 0:
            self.states = [(self.healthy, 0.6), (self.sick, 0.15),
                           (self.hungry, 0.25), (self.dead, 0.0),
                           (self.reproduce, 0.0)]
        else:
            self.states = [(self.healthy, 0.6), (self.sick, 0.15),
                           (self.hungry, 0.25), (self.dead, 0.0),
                           (self.reproduce, 0.0)]
