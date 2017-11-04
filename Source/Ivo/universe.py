from random import randint, random

import numpy as np


class Oschi:
    def __init__(self, position, mass, velocity, rad):
        self.position = np.array(position, dtype=np.float64)
        self.mass = mass
        self.velocity = np.array(velocity, dtype=np.float64)
        self.radius = rad

    @staticmethod
    def random(position_max, mass_min, mass_max, max_velocity, radius_min, radius_max, flat=True):
        if flat:
            z = 0.0
        else:
            z = random(position_max)
        pos = (random(position_max), random(position_max), z)

        m = randint(mass_min, mass_max)
        v = random(max_velocity)
        rad = randint(radius_min, radius_max)
        return Oschi(pos, m, v, rad)


class Universe:
    def __init__(self, init_oschis):
        self.oschis = init_oschis

    def add(self, oschi):
        self.oschis.append(oschi)
