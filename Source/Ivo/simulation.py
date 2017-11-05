import sys

import solar_system as ss
from simulation_constants import END_MESSAGE
from universe import Universe


def initialize():
    dt = 600  # a minute
    # simple = [ss.sun, ss.earth, ss.mars]
    simple = [ss.sun, ss.mercury, ss.venus, ss.earth, ss.mars, ss.jupiter, ss.saturn, ss.uranus, ss.neptune]
    u = Universe(dt, simple)
    u.init_velocities()

    return u


def startup(sim_pipe):
    u = initialize()
    while True:
        if sim_pipe.poll():
            message = sim_pipe.recv()
            if isinstance(message, str) and message == END_MESSAGE:
                print('simulation exiting ...')
                sys.exit(0)
        u.simulate()
        sim_pipe.send(u.listify_oschis())
