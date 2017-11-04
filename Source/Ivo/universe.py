"""
Universe Module
"""
import math
import string
from random import randint, choice
from typing import List

import numpy as np


class Oschi:
    """
    A thing in the Universe
    """

    def __init__(self, name, position, mass, velocity, rad):
        """
        Constructor
        Args:
            name: unique name
            position: 3-tuple, in m
            mass: mass in kg
            velocity: velocity in m/s
            rad: radius in m
        """
        self.name = name
        self.position = np.array(position, dtype=np.float64)
        self.mass = mass
        self.velocity = np.array(velocity, dtype=np.float64)
        self.radius = rad

    @staticmethod
    def random(position_max, mass_min, mass_max, max_velocity, radius_min, radius_max):
        """
        Creates a random Oschi inside set limits.

        Args:
            position_max: max value a coordinate can have
            mass_min: minimum random mass
            mass_max: minimum random mass
            max_velocity: max speed
            radius_min: minimum random mass
            radius_max: minimum random mass
            flat: if true z coordinate is zero
        Returns:

        """

        pos = (randint(0, position_max), randint(0, position_max), 0)

        m = randint(mass_min, mass_max)
        v = (0, 0, 0)
        rad = randint(radius_min, radius_max)

        name = ''.join(choice(string.ascii_uppercase) for _ in range(3))
        name += '-' + randint(1, 999).__str__()

        return Oschi(name, pos, m, v, rad)

    def grav_force(self, other: 'Oschi') -> np.array:
        if not isinstance(other, Oschi):
            raise TypeError("can only gravitate Oschis!")

        delta = self.position - other.position
        dist = np.linalg.norm(delta)  # length of a vector

        # everything except delta is a scalar
        return Universe.G * self.mass * other.mass * delta / dist ** 3

    def __repr__(self):
        return '{:10} {:e} {:e} {:e}'.format(
            self.name,
            self.position[0],
            self.position[1],
            self.position[2]
        )

    def __hash__(self):
        return hash(self.name)

    def __cmp__(self, other):
        if not isinstance(other, Oschi):
            return False
        return self.name == other.name


class Universe:
    G = 6.672 * 10 ** -11

    def __init__(self, init_oschis: List[Oschi]):
        self.delta_time = 60 * 60
        self.oschis = init_oschis

    def add(self, oschi):
        self.oschis.append(oschi)

    def init_velocities(self):
        pass

    # (3)
    def total_mass(self, exclude: Oschi = None):
        total = 0
        for o in self.oschis:
            if o == exclude:
                continue
            total += o.mass
        return total

    # (4) and (5)
    def center_of_mass(self, exclude: Oschi = None):
        center = np.array((0.0, 0.0, 0.0), dtype=np.float64)
        for o in self.oschis:
            if o == exclude:
                continue
            center += o.mass * o.position

        return center / self.total_mass(exclude)

    # (6)
    def total_impulse(self):
        impulse = np.array((0.0, 0.0, 0.0), dtype=np.float64)
        for o in self.oschis:
            impulse += o.mass * o.velocity

    # (8)
    def initial_speed_scalar(self, new_oschi: Oschi):

        center_ex = self.center_of_mass(new_oschi)
        tm = self.total_mass()

        r = np.linalg.norm(new_oschi.position - center_ex)

        return (tm - new_oschi.mass) / tm * math.sqrt(Universe.G * tm / r)

    # (9)
    def initial_speed(self, new_oschi: Oschi):
        z = np.array((0.0, 0.0, 1.0), dtype=np.float64)
        center_ex = self.center_of_mass(new_oschi)

        top = np.cross((new_oschi.position - center_ex), z)
        bottom = np.linalg.norm(top)

        return top / bottom * self.initial_speed_scalar(new_oschi)
