import solor_system as ss
from pysics import grav_force


def main():
    print(grav_force(ss.sun, ss.earth))
    print(grav_force(ss.earth, ss.sun))

    # solar_system = [sun, earth]
    # u = Universe(solar_system)


if __name__ == "__main__":
    main()
