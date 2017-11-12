from names import get_first_name, get_last_name
from random import choice

INITAL_FERTILITY = 0
INITAL_IMMUNITY = 0


class Person:

    def __init__(self, dna):
        self.age = 0
        self.gender = choice(['male', 'female'])
        self.first_name = get_first_name(gender=self.gender)
        if len(self.dna) > 0:
            self.dna = {
                'generation': dna['generation'] + 1,
                'surname': dna['surname'],
                'immunity': self.get_immunity(dna['immunity']),
                'fertility': self.get_fertility(dna['fertility'])
            }
        else:
            self.dna = {
                'generation': 0,
                'surname': get_last_name(),
                'immunity': INITAL_IMMUNITY,
                'fertility': INITAL_FERTILITY
            }

        self.name = (self.first_name, self.dna['surname'])
        self.children = 0

    def get_immunity(self, input):
        return 0

    def get_fertility(self, input):
        return 0
