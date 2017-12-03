import math
import sys
import time

import numpy as np

from simulation_constants import END_MESSAGE

__FPS = 60
__DELTA_ALPHA = 0.01


def _move_bodies(bodies, delta_t):
    for body_index, body in enumerate(bodies):
        j = len(bodies) - body_index
        sin_a = math.sin(__DELTA_ALPHA * j * delta_t)
        cos_a = math.cos(__DELTA_ALPHA * j * delta_t)
        pos_x = body[0]
        pos_y = body[1]
        body[0] = pos_x * cos_a - pos_y * sin_a
        body[1] = pos_x * sin_a + pos_y * cos_a
    time.sleep(1 / __FPS)


def _initialise_bodies(nr_of_bodies):
    body_array = np.zeros((nr_of_bodies, 4), dtype=np.float64)
    for body_index in range(nr_of_bodies):
        body_array[body_index][0] = 0.9 / (nr_of_bodies - body_index)
        body_array[body_index][3] = 0.1 * body_array[body_index][0]
    return body_array


def startup(sim_pipe, pos, vel, mass, rad, max_size):
    # TODO: init here
    bodies = _initialise_bodies(15)

    while True:
        if sim_pipe.poll():
            message = sim_pipe.recv()
            if isinstance(message, str) and message == END_MESSAGE:
                print('simulation exiting ...')
                sys.exit(0)
        else:
            # TODO: simulate here
            _move_bodies(bodies, 1)
            sim_pipe.send(bodies)
