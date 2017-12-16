""" simple PyQt5 simulation controller """
import multiprocessing
#
# Copyright (C) 2017  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# or open http://www.fsf.org/licensing/licenses/gpl.html
#

import sys

import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

import galaxy_renderer
import random
import simulation
from simulation_constants import END_MESSAGE


class SimulationGUI(QMainWindow):
    """
        Widget with two buttons
    """

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('ppp.ui', self)
        self.setWindowTitle('PPP')

        self.btn_random.clicked.connect(self.start_random)
        self.btn_solar.clicked.connect(self.start_solar)
        self.btn_stop.clicked.connect(self.stop_simulation)
        self.btn_quit.clicked.connect(self.exit_application)

        self.is_running = False
        self.log_slider.valueChanged.connect(self.send_log)
        self.delta_t.textChanged.connect(self.send_delta_t)
        
        self.renderer_conn, self.simulation_conn = None, None
        self.render_process = None
        self.simulation_process = None
        multiprocessing.set_start_method('spawn')

    def start_random(self):
        if self.is_running:
            return

        black_hole = self.do_black_hole()
        amount = self.get_amount()
        mass_range = self.get_mass_range()
        density_range = self.get_density_range()
        pos_max = self.get_pos_max()
        max_size = max(pos_max)

        print('Generating', amount, 'random objects')

        # -------------------------------------------------------

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

        # -------------------------------------------------------

        for j in range(pos.__len__()):
            print(pos[j], mass[j], vel[j], rad[j])
            
        self.renderer_conn, self.simulation_conn = multiprocessing.Pipe()
        self.simulation_process = multiprocessing.Process(
            target=simulation.startup,
            args=(
                self.simulation_conn,
                pos, vel, mass, rad, max_size, self.get_log(), self.get_delta_t()
            )
        )
        self.render_process = multiprocessing.Process(
            target=galaxy_renderer.startup,
            args=(self.renderer_conn, 60),
        )
        self.simulation_process.start()
        self.render_process.start()
        self.is_running = True

    def start_solar(self):
        if self.is_running:
            return

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

        FACTOR = 0.1
        radius = [
            0.25 * FACTOR,
            0.02 * FACTOR,
            0.06 * FACTOR,
            0.06 * FACTOR,
            0.01 * FACTOR,
            0.03 * FACTOR,
            0.18 * FACTOR,
            0.15 * FACTOR,
            0.1 * FACTOR,
            0.1 * FACTOR
        ]

        print('Loading Solar System')
        # convert to numpy
        mass = np.array(python_masse, dtype=np.float64)
        rad = np.array(python_rads, dtype=np.float64)
        pos = np.array(python_position, dtype=np.float64)
        vel = np.array(python_geschwindigkeit, dtype=np.float64)
        max_size = 4_498_252_900_000

        print()
        print('Launch Render and Simulation...')

        self.renderer_conn, self.simulation_conn = multiprocessing.Pipe()
        self.simulation_process = multiprocessing.Process(
            target=simulation.startup,
            args=(
                self.simulation_conn,
                pos, vel, mass, rad, max_size, self.get_log(), self.get_delta_t()
            )
        )
        self.render_process = multiprocessing.Process(
            target=galaxy_renderer.startup,
            args=(self.renderer_conn, 60),
        )
        self.simulation_process.start()
        self.render_process.start()
        self.is_running = True
        pass

    def stop_simulation(self):
        """
            Stop simulation and render process by sending END_MESSAGE
            through the pipes.
        """
        if self.simulation_process is not None:
            self.simulation_conn.send(END_MESSAGE)
            self.simulation_process = None

        if self.render_process is not None:
            self.renderer_conn.send(END_MESSAGE)
            self.render_process = None

        self.is_running = False
        
    def exit_application(self):
        """
        Stop simulation and exit.
        """
        self.stop_simulation()
        self.close()

    def get_mass_range(self):
        mini = eval(self.mass_min.text())
        maxi = eval(self.mass_max.text())
        return mini, maxi

    def get_density_range(self):
        mini = eval(self.density_min.text())
        maxi = eval(self.density_max.text())
        return mini, maxi

    def get_pos_max(self):
        x = eval(self.size_x.text())
        y = eval(self.size_y.text())
        z = eval(self.size_z.text())
        return x, y, z

    def get_amount(self):
        return self.amount.value()

    def do_black_hole(self):
        return self.black_hole.isChecked()

    def get_delta_t(self):
        try:
            return float(self.delta_t.text())
        except ValueError:
            return 60.0 * 60.0

    def get_log(self):
        return float(self.log_slider.value())
        
    def send_log(self):
        print('send log')
        if self.simulation_process is not None:
            self.renderer_conn.send('LOGN:' + str(self.get_log()))

    def send_delta_t(self):
        print('send delta')
        if self.simulation_process is not None:
            self.renderer_conn.send('TIME:' + str(self.get_delta_t()))

        
def _main(argv):
    app = QtWidgets.QApplication(argv)
    simulation_gui = SimulationGUI()
    simulation_gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    _main(sys.argv)
