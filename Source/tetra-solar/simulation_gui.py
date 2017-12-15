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

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow

import galaxy_renderer
import tetra_sim
from simulation_constants import END_MESSAGE


class SimulationGUI(QMainWindow):
    """
        Widget with two buttons
    """

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('ppp.ui', self)
        self.setWindowTitle('Tetra Sim')

        self.btn_random.clicked.connect(self.start_random)
        self.btn_solar.clicked.connect(self.start_solar)
        self.btn_stop.clicked.connect(self.stop_simulation)
        self.btn_quit.clicked.connect(self.exit_application)

        self.log_slider.valueChanged.connect(self.send_log)
        self.delta_t.textChanged.connect(self.send_delta_t)

        self.renderer_conn, self.simulation_conn = None, None
        self.render_process = None
        self.simulation_process = None
        multiprocessing.set_start_method('spawn')

    def start_random(self):
        black_hole = self.do_black_hole()
        amount = self.get_amount()
        mass_range = self.get_mass_range()
        density_range = self.get_density_range()
        pos_max = self.get_pos_max()

        self.renderer_conn, self.simulation_conn = multiprocessing.Pipe()
        self.simulation_process = multiprocessing.Process(
            target=tetra_sim.startup,
            args=(self.simulation_conn, True, amount, mass_range, density_range, pos_max, black_hole, self.get_log(),
                  self.get_delta_t()),
        )
        self.render_process = multiprocessing.Process(target=galaxy_renderer.startup, args=(self.renderer_conn, 60), )
        self.simulation_process.start()
        self.render_process.start()

    def start_solar(self):

        self.renderer_conn, self.simulation_conn = multiprocessing.Pipe()
        self.simulation_process = multiprocessing.Process(
            target=tetra_sim.startup,
            args=(self.simulation_conn, False, 0, 0, 0, 0, False, self.get_log(), self.get_delta_t()),
        )
        self.render_process = multiprocessing.Process(target=galaxy_renderer.startup, args=(self.renderer_conn, 60), )
        self.simulation_process.start()
        self.render_process.start()

    def send_log(self):
        print('send log')
        if self.simulation_process is not None:
            self.renderer_conn.send('LOGN:' + str(self.get_log()))

    def send_delta_t(self):
        print('send delta')
        if self.simulation_process is not None:
            self.renderer_conn.send('TIME:' + str(self.get_delta_t()))

    def stop_simulation(self):
        if self.simulation_process is not None:
            self.simulation_conn.send(END_MESSAGE)
            self.simulation_process = None
        if self.render_process is not None:
            self.renderer_conn.send(END_MESSAGE)
            self.render_process = None

    def exit_application(self):
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


def _main(argv):
    app = QtWidgets.QApplication(argv)
    simulation_gui = SimulationGUI()
    simulation_gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    _main(sys.argv)
