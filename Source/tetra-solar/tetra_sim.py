import datetime
import random
import sys

import numpy as np
from numba import jit

from simulation_constants import END_MESSAGE


@jit
def grav_force(pos, mass, start):
    f = np.zeros(3, dtype=np.float64)
    for other in range(len(pos)):
        if start != other:
            delta = pos[other] - pos[start]
            dist = np.math.sqrt(delta[0] * delta[0] + delta[1] * delta[1] + delta[2] * delta[2])
            f += (6.672 * 10 ** -11) * delta * (mass[start] * mass[other] / dist ** 3)

    return f

@jit
def tick(pos, vel, mass, delta_t):
    pos_new = pos.copy()
    vel_new = vel.copy()

    for i in range(len(pos)):
        m = mass[i]
        p = pos[i]
        v = vel[i]

        a = grav_force(pos, mass, i) / m
        vel_new[i] = v + a * delta_t
        pos_new[i] = p + delta_t * v + 0.5 * delta_t * delta_t * a

    return pos_new, vel_new

@jit
def get_render_data(pos, rad, max_pos, log, black_hole):
    data = np.zeros((len(pos), 4), dtype=np.float64)

    for i in range(len(pos)):
        data[i, 0] = pos[i, 0] / max_pos
        data[i, 1] = pos[i, 1] / max_pos
        data[i, 2] = pos[i, 2] / max_pos
        data[i, 3] = 0.008  # rad[i]

    if black_hole:
        data[0, 3] = 0.016

    return data

@jit
def create_random(amount: int, mass_range: tuple, density_range: tuple, pos_max: tuple, black_hole=True):
    pos = np.zeros((amount, 3), np.float64)
    mass = np.zeros(amount, np.float64)
    vel = np.zeros((amount, 3), np.float64)
    rad = np.zeros(amount, np.float64)

    for i in range(amount):
        pos[i, 0] = random.uniform(-pos_max[0], pos_max[0])
        pos[i, 1] = random.uniform(-pos_max[1], pos_max[1])
        pos[i, 2] = random.uniform(-pos_max[2], pos_max[2])

        mass[i] = random.uniform(mass_range[0], mass_range[1])
        density = random.uniform(density_range[0], density_range[1])
        rad[i] = (3 * (mass[i] / density) / 4 * 3.141592) ** (1. / 3.)

    z = np.array((0.0, 0.0, 1.0), dtype=np.float64)
    g = 6.67408e-11

    if black_hole:
        # replace first with black hole
        vel[0, 0] = 0.0
        vel[0, 1] = 0.0
        vel[0, 2] = 0.0
        pos[0, 0] = 0.0
        pos[0, 1] = 0.0
        pos[0, 2] = 0.0
        mass[0] = mass_range[1] * 4_000
        rad[0] = (3 * (mass[0] / 1000.0) / 4 * 3.141592) ** (1. / 3.)

    mass_pos_sum = np.array((0.0, 0.0, 0.0), dtype=np.float64)
    for i in range(amount):
        mass_pos_sum += mass[i] * pos[i]
    total_mass = mass.sum()

    for i in range(amount):
        my_pos = pos[i]
        my_mass = mass[i]
        total_mass_ex = total_mass - my_mass
        center_ex = (mass_pos_sum - my_mass * my_pos) / total_mass_ex

        # skalar Geschwindigkeit
        r = np.linalg.norm(my_pos - center_ex)
        vel_scalar = (total_mass_ex / total_mass) * np.sqrt(g * total_mass / r)

        # gerichtet
        top = np.cross((my_pos - center_ex), z)
        bottom = np.linalg.norm(top)
        vel[i] = top / bottom * vel_scalar

    return pos, mass, vel, rad


def create_solar():
    python_position = [
        [0, 0, 0],  # "Sun"
        [57_909_175_000, 0, 0],  # "Mercury"
        [108_208_930_000, 0, 0],  # "Venus"
        [149_597_890_000, 0, 0],  # "Earth"
        [227_936_640_000, 0, 0],  # "Mars"
        [778_412_020_000, 0, 0],  # "Jupiter"
        [1_426_725_400_000, 0, 0],  # "Saturn"
        [2_870_972_200_000, 0, 0],  # "Uranus"
        [4_498_252_900_000, 0, 0]  # "Neptune"
    ]
    python_geschwindigkeit = [
        [0, 0, 0],  # "Sun"
        [0, 47_872, 0],  # "Mercury"
        [0, 35_021, 0],  # "Venus"
        [0, 29_786, 0],  # "Earth"
        [0, 24_131, 0],  # "Mars"
        [0, 13_069, 0],  # "Jupiter"
        [0, 9_672, 0],  # "Saturn"
        [0, 6_835, 0],  # "Uranus"
        [0, 5_477, 0]  # "Neptune"
    ]
    python_masse = [
        1.9889 * 10 ** 30,  # "Sun"
        3.3022 * 10 ** 23,  # "Mercury"
        4.8685 * 10 ** 24,  # "Venus"
        5.97219 * 10 ** 24,  # "Earth"
        6.4185 * 10 ** 23,  # "Mars"
        1.8987 * 10 ** 27,  # "Jupiter"
        5.6851 * 10 ** 26,  # "Saturn"
        8.6849 * 10 ** 25,  # "Uranus"
        1.0244 * 10 ** 26  # "Neptune"
    ]
    python_rads = [
        695_500_000,  # "Sun"
        2_439_764,  # "Mercury"
        6_051_590,  # "Venus"
        6_378_150,  # "Earth"
        3_397_000,  # "Mars"
        71_492_680,  # "Jupiter"
        60_267_140,  # "Saturn"
        25_559_000,  # "Uranus"
        24_764_000  # "Neptune"
    ]

    pos = np.array(python_position, dtype=np.float64)
    mass = np.array(python_masse, dtype=np.float64)
    vel = np.array(python_geschwindigkeit, dtype=np.float64)
    rad = np.array(python_rads, dtype=np.float64)

    return pos, mass, vel, rad


def startup(sim_pipe, do_random, amount, mass_range, density_range, pos_max, black_hole, log, dt):
    max_pos = 10 ** 7
    delta_t = dt
    log_n = log

    print('creating TetraSim')
    if do_random:
        pos, mass, vel, rad = create_random(amount, mass_range, density_range, pos_max, black_hole)
        max_pos = max(pos_max)
    else:
        pos, mass, vel, rad = create_solar()
        max_pos = 4_498_252_900_000

    cnt = 0
    time = datetime.datetime.now()
    print('starting TetraSim')
    while True:
        if sim_pipe.poll():
            message = sim_pipe.recv()
            if isinstance(message, str):
                if 'LOGN' in message:
                    log_n = float(message[5:])
                    print('Set log:', log_n)
                elif 'TIME' in message:
                    delta_t = float(message[5:])
                    print('Set delta time:', delta_t)
                elif message == END_MESSAGE:
                    print('simulation exiting ...')
                    sys.exit(0)

        pos, vel = tick(pos, vel, mass, delta_t)

        sim_pipe.send(
            get_render_data(pos, rad, max_pos, log_n, black_hole)
        )

        cnt = (cnt + 1) % 50
        time_end = datetime.datetime.now()
        if cnt == 1:
            print(time_end - time)
        time = time_end
