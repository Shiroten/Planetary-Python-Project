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
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

import galaxy_renderer
import helper
import simulation
from simulation_constants import END_MESSAGE


class SimulationGUI(QMainWindow):
    """
        Widget with two buttons
    """

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.setupUI()

        self.btn_random.clicked.connect(self.start_random)
        self.btn_solar.clicked.connect(self.start_solar)
        self.btn_stop.clicked.connect(self.stop_simulation)
        self.btn_quit.clicked.connect(self.exit_application)

        self.pos = []
        self.vel = []
        self.mass = []
        self.rad = []
        self.max_size = 100
        self.is_running = False

        self.renderer_conn, self.simulation_conn = None, None
        self.render_process = None
        self.simulation_process = None
        multiprocessing.set_start_method('spawn')

    def start_random(self):
        if self.is_running:
            return

        # reset
        self.max_size = self.size_max.value()
        self.pos = []
        self.vel = []
        self.mass = []
        self.rad = []

        amount = self.get_amount()
        black_hole = self.do_black_hole()

        print('Generating', amount, 'random objects')
        if black_hole:
            # todo: code
            print('Black Hole done')

        for _ in range(amount):
            self.pos.append(self.get_random_position())
            self.mass.append(self.get_random_mass())
            self.rad.append(self.get_random_radius())
            print('Object', _ + 1, 'done')

        print('Calculating speeds')
        self.vel = helper.calc_init_speeds(self.pos, self.mass)

        print()
        print('Launch Render and Simulation...')

        self.mass = np.array(self.mass, dtype=np.float64)
        self.rad = np.array(self.rad, dtype=np.float64)
        self.pos = np.array(self.pos, dtype=np.float64)
        self.vel = np.array(self.vel, dtype=np.float64)

        self.renderer_conn, self.simulation_conn = multiprocessing.Pipe()
        self.simulation_process = multiprocessing.Process(
            target=simulation.startup,
            args=(
                self.simulation_conn,
                self.pos, self.vel, self.mass, self.rad, self.max_size
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
        radius =  [
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
        self.mass = np.array(python_masse, dtype=np.float64)
        self.rad = np.array(python_rads, dtype=np.float64)
        self.pos = np.array(python_position, dtype=np.float64)
        self.vel = np.array(python_geschwindigkeit, dtype=np.float64)
        self.max_size = 4_498_252_900_000

        print()
        print('Launch Render and Simulation...')

        self.renderer_conn, self.simulation_conn = multiprocessing.Pipe()
        self.simulation_process = multiprocessing.Process(
            target=simulation.startup,
            args=(
                self.simulation_conn,
                self.pos, self.vel, self.mass, self.rad, self.max_size
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

    '''
    def start_simulation(self):
        """
        Start simulation and render process connected with a pipe.
        """
        self.renderer_conn, self.simulation_conn = multiprocessing.Pipe()
        self.simulation_process = multiprocessing.Process(
            target=simulation.startup,
            args=(
                self.simulation_conn,
                self.pos, self.vel, self.mass, self.rad, self.max_size
            )
        )
        self.render_process = multiprocessing.Process(
            target=galaxy_renderer.startup,
            args=(self.renderer_conn, 60),
        )
        self.simulation_process.start()
        self.render_process.start()
    '''

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

    def get_random_mass(self):
        mini = self.mass_min.value()
        maxi = self.mass_max.value()
        return helper.random_int(mini, maxi)

    def get_random_radius(self):
        mini = self.rad_min.value()
        maxi = self.rad_max.value()
        return helper.random_int(mini, maxi)

    def get_random_position(self):
        size = self.size_max.value()
        return helper.random_numpy(0, size)

    def get_amount(self):
        return self.number.value()

    def do_black_hole(self):
        return self.black_hole.isChecked()

    def setupUI(self):
        self.setGeometry(100, 100, 260, 200)
        self.setWindowTitle('PPP')
        self.resize(471, 250)
        icon = QIcon()
        icon.addPixmap(QtGui.QPixmap("ppp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.group_other = QtWidgets.QGroupBox(self.centralwidget)
        self.group_other.setGeometry(QtCore.QRect(10, 130, 261, 111))
        self.group_other.setObjectName("group_other")
        self.label_4 = QtWidgets.QLabel(self.group_other)
        self.label_4.setGeometry(QtCore.QRect(10, 20, 81, 20))
        self.label_4.setObjectName("label_4")
        self.black_hole = QtWidgets.QCheckBox(self.group_other)
        self.black_hole.setGeometry(QtCore.QRect(10, 80, 151, 21))
        self.black_hole.setObjectName("black_hole")
        self.size_max = QtWidgets.QDoubleSpinBox(self.group_other)
        self.size_max.setGeometry(QtCore.QRect(90, 20, 161, 22))
        self.size_max.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.size_max.setDecimals(0)
        self.size_max.setMinimum(10000.0)
        self.size_max.setMaximum(1e+19)
        self.size_max.setSingleStep(10000.0)
        self.size_max.setProperty("value", 3000000000000.0)
        self.size_max.setObjectName("size_max")
        self.label_5 = QtWidgets.QLabel(self.group_other)
        self.label_5.setGeometry(QtCore.QRect(10, 50, 81, 20))
        self.label_5.setObjectName("label_5")
        self.number = QtWidgets.QSpinBox(self.group_other)
        self.number.setGeometry(QtCore.QRect(90, 50, 61, 22))
        self.number.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.number.setMinimum(0)
        self.number.setMaximum(9999)
        self.number.setProperty("value", 20)
        self.number.setObjectName("number")
        self.btn_solar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_solar.setGeometry(QtCore.QRect(380, 130, 81, 71))
        self.btn_solar.setObjectName("btn_solar")
        self.group_mass = QtWidgets.QGroupBox(self.centralwidget)
        self.group_mass.setGeometry(QtCore.QRect(10, 10, 261, 111))
        self.group_mass.setObjectName("group_mass")
        self.label = QtWidgets.QLabel(self.group_mass)
        self.label.setGeometry(QtCore.QRect(10, 20, 31, 21))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.group_mass)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 31, 21))
        self.label_3.setObjectName("label_3")
        self.mass_min = QtWidgets.QDoubleSpinBox(self.group_mass)
        self.mass_min.setGeometry(QtCore.QRect(40, 20, 211, 22))
        self.mass_min.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.mass_min.setDecimals(0)
        self.mass_min.setMinimum(1.0)
        self.mass_min.setMaximum(10000000000000.0)
        self.mass_min.setSingleStep(1000.0)
        self.mass_min.setProperty("value", 1.0)
        self.mass_min.setObjectName("mass_min")
        self.mass_max = QtWidgets.QDoubleSpinBox(self.group_mass)
        self.mass_max.setGeometry(QtCore.QRect(40, 50, 211, 22))
        self.mass_max.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.mass_max.setDecimals(0)
        self.mass_max.setMinimum(1.0)
        self.mass_max.setMaximum(10000000000000.0)
        self.mass_max.setSingleStep(1000.0)
        self.mass_max.setProperty("value", 200000.0)
        self.mass_max.setObjectName("mass_max")
        self.mass_xten = QtWidgets.QSpinBox(self.group_mass)
        self.mass_xten.setGeometry(QtCore.QRect(190, 80, 61, 22))
        self.mass_xten.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.mass_xten.setMinimum(0)
        self.mass_xten.setMaximum(9999)
        self.mass_xten.setProperty("value", 20)
        self.mass_xten.setObjectName("mass_xten")
        self.label_2 = QtWidgets.QLabel(self.group_mass)
        self.label_2.setGeometry(QtCore.QRect(140, 80, 51, 21))
        self.label_2.setObjectName("label_2")
        self.group_rad = QtWidgets.QGroupBox(self.centralwidget)
        self.group_rad.setGeometry(QtCore.QRect(280, 10, 181, 111))
        self.group_rad.setObjectName("group_rad")
        self.label_6 = QtWidgets.QLabel(self.group_rad)
        self.label_6.setGeometry(QtCore.QRect(10, 20, 31, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.group_rad)
        self.label_7.setGeometry(QtCore.QRect(10, 50, 31, 21))
        self.label_7.setObjectName("label_7")
        self.rad_min = QtWidgets.QDoubleSpinBox(self.group_rad)
        self.rad_min.setGeometry(QtCore.QRect(40, 20, 131, 22))
        self.rad_min.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.rad_min.setDecimals(0)
        self.rad_min.setMinimum(1.0)
        self.rad_min.setMaximum(10000000000.0)
        self.rad_min.setSingleStep(1.0)
        self.rad_min.setProperty("value", 1000.0)
        self.rad_min.setObjectName("rad_min")
        self.rad_max = QtWidgets.QDoubleSpinBox(self.group_rad)
        self.rad_max.setGeometry(QtCore.QRect(40, 50, 131, 22))
        self.rad_max.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.rad_max.setDecimals(0)
        self.rad_max.setMinimum(1.0)
        self.rad_max.setMaximum(10000000000.0)
        self.rad_max.setSingleStep(1.0)
        self.rad_max.setProperty("value", 700000.0)
        self.rad_max.setObjectName("rad_max")
        self.rad_xten = QtWidgets.QSpinBox(self.group_rad)
        self.rad_xten.setGeometry(QtCore.QRect(110, 80, 61, 22))
        self.rad_xten.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.rad_xten.setMinimum(0)
        self.rad_xten.setMaximum(9999)
        self.rad_xten.setProperty("value", 3)
        self.rad_xten.setObjectName("rad_xten")
        self.label_8 = QtWidgets.QLabel(self.group_rad)
        self.label_8.setGeometry(QtCore.QRect(57, 80, 51, 21))
        self.label_8.setObjectName("label_8")
        self.btn_random = QtWidgets.QPushButton(self.centralwidget)
        self.btn_random.setEnabled(True)
        self.btn_random.setGeometry(QtCore.QRect(280, 130, 91, 71))
        self.btn_random.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.btn_random.setObjectName("btn_random")
        self.btn_stop = QtWidgets.QPushButton(self.centralwidget)
        self.btn_stop.setEnabled(True)
        self.btn_stop.setGeometry(QtCore.QRect(280, 210, 91, 31))
        self.btn_stop.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.btn_stop.setObjectName("btn_stop")
        self.btn_quit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quit.setEnabled(True)
        self.btn_quit.setGeometry(QtCore.QRect(380, 210, 81, 31))
        self.btn_quit.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.btn_quit.setObjectName("btn_quit")
        self.setCentralWidget(self.centralwidget)

        _translate = QtCore.QCoreApplication.translate
        self.group_other.setTitle(_translate("MainWindow", "Andere Werte"))
        self.label_4.setText(_translate("MainWindow", "Raumgröße (m)"))
        self.black_hole.setText(_translate("MainWindow", "Schwarzes Loch im Zentrum"))
        self.label_5.setText(_translate("MainWindow", "Anzahl Körper"))
        self.btn_solar.setText(_translate("MainWindow", "Sonnen\nSystem"))
        self.group_mass.setTitle(_translate("MainWindow", "Masse (kg)"))
        self.label.setText(_translate("MainWindow", "min"))
        self.label_3.setText(_translate("MainWindow", "max"))
        self.label_2.setText(_translate("MainWindow", "x 10 hoch"))
        self.group_rad.setTitle(_translate("MainWindow", "Radien (m)"))
        self.label_6.setText(_translate("MainWindow", "min"))
        self.label_7.setText(_translate("MainWindow", "max"))
        self.label_8.setText(_translate("MainWindow", "x 10 hoch"))
        self.btn_random.setText(_translate("MainWindow", "Zufällige \nErstellen"))
        self.btn_stop.setText(_translate("MainWindow", "Stoppen"))
        self.btn_quit.setText(_translate("MainWindow", "Quit"))

        self.setTabOrder(self.mass_min, self.mass_max)
        self.setTabOrder(self.mass_max, self.mass_xten)
        self.setTabOrder(self.mass_xten, self.rad_min)
        self.setTabOrder(self.rad_min, self.rad_max)
        self.setTabOrder(self.rad_max, self.rad_xten)
        self.setTabOrder(self.rad_xten, self.size_max)
        self.setTabOrder(self.size_max, self.number)
        self.setTabOrder(self.number, self.black_hole)
        self.setTabOrder(self.black_hole, self.btn_random)
        self.setTabOrder(self.btn_random, self.btn_solar)


def _main(argv):
    """
    Main function to avoid pylint complains concerning constant names.
    """
    app = QtWidgets.QApplication(argv)
    simulation_gui = SimulationGUI()
    simulation_gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    _main(sys.argv)
