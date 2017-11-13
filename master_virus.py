from popsim.virus.viralnames import get_virus_name, get_virus_family
from random import choice


class Virus:

    def __init__(self, dna):
        self.age = 0
        self.first_name = get_virus_name()
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
                'family': get_virus_family(),
                'immunity': 0,
                'fertility': 0
            }

        self.name = (self.first_name, self.dna['family'])
