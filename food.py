import numpy as np


class Food:

    def __init__(self, start, growth, maximum):
        self.start = start
        self.total = start
        self.growth = growth
        self.maximum = maximum

    def grow(self):
        if self.total < self.maximum:
            growth_amt = np.random.normal(loc=self.growth, scale=10)
            self.total += int(growth_amt)
        else:
            pass

    def eat(self):
        if self.total > 0:
            self.total -= 1
            return 1
        else:
            return 0
