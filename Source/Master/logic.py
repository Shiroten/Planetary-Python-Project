#
from random import randint
import math
import data

def initPlanets():
    number_of_planets = randint(2, 5)
    for _ in range(number_of_planets):
        planet_weight = randint(1, 9) * math.pow(10, 24)
        data.planet_weights.append(planet_weight)

    for planet in data.planet_weights:
        print(planet)


initPlanets()