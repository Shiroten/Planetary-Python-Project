import numpy as np

import solar_system as ss
from universe import Universe


def main():
    print(ss.earth.grav_force(ss.sun))

    dt = 60  # a minute
    simple = [ss.sun, ss.earth]
    u = Universe(dt, simple)
    u.init_velocities()

    print("------------------- init speeds --------------------")
    for o in u.oschis:
        print(o.name, np.linalg.norm(o.velocity))
    print()

    counter = 0
    while u.simulate():

        if counter > (370 * 24 * 60):
            break  # after a year

        if counter % (31 * 24 * 60) == 0:  # each month
            print('')
            for o in u.oschis:
                print('{:10} | {:15e} {:15e} {:15e} | {:15f} {:15f} {:15f} | {:15e} | {:15f}'.format(
                    o.name,
                    o.position[0],
                    o.position[1],
                    o.position[2],
                    o.velocity[0],
                    o.velocity[1],
                    o.velocity[2],
                    np.linalg.norm(o.position),
                    np.linalg.norm(o.velocity)
                ))
        counter += 1

    print()
    print("------------------- After a Year --------------------")
    print(u.oschis)




if __name__ == "__main__":
    main()
