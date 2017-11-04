import solar_system as ss
from universe import Universe


def main():
    print(ss.sun.grav_force(ss.earth))
    print(ss.earth.grav_force(ss.sun))

    print()

    simple = [ss.sun, ss.earth, ss.moon]
    u = Universe(simple)

    print(u.initial_speed(ss.earth))


if __name__ == "__main__":
    main()
