import sys

from simulation_constants import END_MESSAGE


def initialize():
    return None


def startup(sim_pipe):
    while True:
        if sim_pipe.poll():
            message = sim_pipe.recv()
            if isinstance(message, str) and message == END_MESSAGE:
                print('simulation exiting ...')
                sys.exit(0)
                # u.simulate()
                # sim_pipe.send(u.listify_oschis())
