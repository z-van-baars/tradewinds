import random
import math


def check_if_inside(x1, x2, y1, y2, pos):
    return x1 < pos[0] < x2 and y1 < pos[1] < y2


def distance(a, b, x, y):
    a1 = abs(a - x)
    b1 = abs(b - y)
    c = math.sqrt((a1 * a1) + (b1 * b1))
    return c


def roll_dice(number_of_dice, sides):
    # Sum of N dice each of which goes from 0 to sides
    value = 0
    for i in range(number_of_dice):
        value += random.randint(1, sides)
    return value
