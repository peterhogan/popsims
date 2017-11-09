from random import randint


def P(x):
    if x == 1:
        return True
    elif x == 0:
        return False
    num = format(x, '.10f').split('.')
    dec = num[1]
    multi = len(dec)
    numerator = int(x * 10**multi)
    choice = randint(1, 10**multi)
    if choice <= numerator:
        return True
    elif choice > numerator:
        return False
