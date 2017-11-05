
from universe import Universe
import solar_system as ss
import sys

from simulation_constants import END_MESSAGE

def initialize():
    dt = 60  # a minute
    simple = [ss.sun, ss.earth]
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
        list = u.listify_oschis()
        sim_pipe.send(list)