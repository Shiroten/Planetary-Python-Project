from random import randint
import numpy as np


def generate_random_tuple(min_tuple, max_tuple):
    """
    Gibt ein zufälliges n tuple der größe der übergebenen Tuple zurück. Beide params müssen die
    selbe länge haben.
    :param min_tuple: Ein Tuple mit den minimalen Werten des zurückzugebenen Tuples
    :param max_tuple: Ein Tuple mit den maximalen Werten des zurückzugebenen Tuples
    :return: Ein zufällig erzeugtes Tuple mit den Schranken min_ und max_
    """
    created_tuple = []
    if len(min_tuple) == len(max_tuple):
        for i in range(len(min_tuple)):
            created_tuple.append(randint(min_tuple[i], max_tuple[i]))
    return tuple(created_tuple)


def generate_n_rand_tuples(n, min_tuple, max_tuple):
    """
    Generiert n zufällige Tuple, siehe generate_random_tuple
    :param n: Anzahl der zu erstellenden Tuple
    :param min_tuple: Ein Tuple mit den minimalen Werten des zurückzugebenen Tuples
    :param max_tuple: Ein Tuple mit den maximalen Werten des zurückzugebenen Tuples
    :return: N zufällig erzeugte Tuple mit den Schranken min_ und max_
    """
    tuple_list = []
    for i in range(n):
        tuple_list.append(generate_random_tuple(min_tuple, max_tuple))
    return tuple_list


def random_mass(min_v, max_v):
    return randint(min_v, max_v)


def calculate_init_speeds(positions, masses):
    """
    Berechnet für alle Körper eines Systems die Startgeschwindigkeiten. positions und masses müssen
    gleich lang sein
    :param positions: Die Positionen der Planeten
    :param masses: Die Massen der Planeten
    :return: Startgeschwindkeiten, die annähernde Kreisbahnen erzeugen sollten
    """
    if not len(positions) == len(masses):
        return
    speeds = []
    total_mass = sum(masses)
    g = 6.672 * 10 ** -11
    for i in range(len(positions)):
        # Masse des Körpers
        m_i = masses[i]
        # Masse-Schwerpunkt aller Körper
        r_i = 1 / total_mass * sum_mult(positions, masses)
        # Masse-Schwerpunkt ohne Körper i
        r_si = 1 / (total_mass - m_i) * sum_mult(positions, masses, i)
        r = r_i - r_si
        # Geschwindigkeit in allen drei Dimensionen:
        v_unsigned = ((total_mass - m_i) / total_mass) * np.sqrt(g*total_mass/np.abs(r))
        z = (0,0,1)
        # Endgültige Geschwindkeit
        # Diese Zeile macht noch Probleme (Division durch null)
        # Mir ist auch nicht ganz klar, was die Formel (9) erreichen soll, bzw ob z nicht (1,1,0) sein müsste
        # v = v_unsigned * (r * z) / np.abs(r * z)
        # Hier dann auf v ändern
        speeds.append(v_unsigned)
    return speeds


def sum_mult(positions, masses, skip=-1):
    sum_r = 0
    positions = np.array(positions, dtype=np.float64)
    for i in range(len(positions)):
        if not skip == i:
            sum_r += positions[i] * masses[i]
    return sum_r


print(calculate_init_speeds([(1, 1, 1), (2, 2, 2)], [3, 1]))
