"""
Start simulation and renderer in separate processes connected by a pipe.
"""
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
import multiprocessing
import time

import galaxy_renderer
import tetra_sim
from simulation_constants import END_MESSAGE


def _startup():
    amount = 80
    mass_range = (10 ** 20, 10 ** 25)
    density_range = (1.00, 5.00)
    pos_max = (10 ** 9, 10 ** 9, 3 * 10 ** 8)
    renderer_conn, simulation_conn = multiprocessing.Pipe()
    simulation_process = multiprocessing.Process(
        target=tetra_sim.startup,
        args=(simulation_conn, True, amount, mass_range, density_range, pos_max),
    )
    render_process = multiprocessing.Process(target=galaxy_renderer.startup, args=(renderer_conn, 60), )
    simulation_process.start()
    render_process.start()
    time.sleep(60 * 10)
    simulation_conn.send(END_MESSAGE)
    renderer_conn.send(END_MESSAGE)
    simulation_process.join()
    render_process.join()


if __name__ == '__main__':
    _startup()
