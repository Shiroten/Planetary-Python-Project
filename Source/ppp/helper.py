from random import randint

import numpy as np


def random_numpy(mini, maxi, n=3):
    """
    Random Vector
    Args:
        mini: minimum
        maxi: maximum
        n: length of vector

    Returns:
        np.array
    """
    vec = np.zeros(n, dtype=np.float64)

    for i in range(n):
        vec[i] = randint(mini, maxi)

    return vec


def random_int(mini, maxi):
    """
    Mirror of randint
    Args:
        mini: minimum int
        maxi: maximum int

    Returns:
        random
    """
    return randint(mini, maxi)


def calc_init_speeds(pos_list, mass_list):
    """
    Calculate speeds for objects
    Args:
        pos_list:
        mass_list:

    Returns:
        list of velocities
    """

    if len(pos_list) != len(mass_list):
        raise TypeError('Length must be the same')

    z = np.array((0.0, 0.0, 1.0), dtype=np.float64)
    g = 6.67408e-11

    speeds = []
    total_mass = sum(mass_list)

    mr_sum = np.array((0.0, 0.0, 0.0), dtype=np.float64)
    for i in range(len(pos_list)):
        mr_sum += mass_list[i] * pos_list[i]

    for i in range(len(pos_list)):
        pos = pos_list[i]
        mass = mass_list[i]
        total_mass_ex = total_mass - mass

        # Abziehen von eigenem mr-Produkt, teilen durch Gesamtmasse ohne eigene
        center_ex = (mr_sum - mass * pos) / total_mass_ex

        # skalar Geschwindigkeit
        r = np.linalg.norm(new_oschi.position - center_ex)
        vel_scalar = (total_mass_ex / total_mass) * np.sqrt(g * total_mass / r)

        # gerichtet
        top = np.cross((pos - center_ex), z)
        bottom = np.linalg.norm(top)
        vel = top / bottom * vel_scalar

        speeds.append(vel)
    return speeds
