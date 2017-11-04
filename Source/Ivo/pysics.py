import numpy as np

from universe import Oschi

G = 6.672 * 10 ** -11


def grav_force(o1: Oschi, o2: Oschi):
    if not (isinstance(o1, Oschi) and isinstance(o2, Oschi)):
        raise TypeError("can only gravitate Oschis!")

    delta = o2.position - o1.position
    dist = np.linalg.norm(delta)  # length of a vector

    # everything except delta is a scalar
    return G * o1.mass * o2.mass * delta / dist ** 3
