import unittest
from universe import Oschi
from universe import Universe
import matplotlib.pyplot as plt


class TestMethods(unittest.TestCase):

    def test_grav_force(self):
        g = Universe.G
        sun = Oschi(
            "Sun",
            (0, 0, 0),
            1,
            (0, 0, 0),
            0.2
        )
        earth = Oschi(
            "Earth",
            (1, 2, 2),
            27,
            (0, 0, 0),
            0.1
        )
        t = sun.grav_force(earth)
        self.assertTrue((sun.grav_force(earth) == (g,2 *g, 2 *g)).all())

    def test_total_mass(self):
        sun = Oschi(
            "Sun",
            (0, 0, 0),
            1,
            (0, 0, 0),
            0.2
        )
        earth = Oschi(
            "Earth",
            (1, 1, 1),
            27 * 10 ** 11,
            (0, 0, 0),
            0.1
        )

        universe = Universe(60, [sun, earth])
        self.assertEqual(universe.total_mass(earth), 1)

    def test_center_of_mass(self):
        sun = Oschi(
            "Sun",
            (0, 0, 0),
            1,
            (0, 0, 0),
            0.2
        )
        earth = Oschi(
            "Earth",
            (1, 1, 1),
            27 * 10 ** 11,
            (0, 0, 0),
            0.1
        )

        universe = Universe(60, [sun, earth])

        u = universe.center_of_mass(earth)
        self.assertTrue((universe.center_of_mass(earth) == (0,0,0)).all())

    def test_total_impulse(self):
        sun = Oschi(
            "Sun",
            (0, 0, 0),
            1,
            (0, 0, 0),
            0.2
        )
        earth = Oschi(
            "Earth",
            (1, 1, 1),
            10,
            (1, 1, 1),
            0.1
        )

        universe = Universe(60, [sun, earth])
        self.assertTrue((universe.total_impulse() == (10, 10, 10)).all())


if __name__ == '__main__':
    unittest.main()

