from cython.parallel import prange , threadid
from multiprocessing import cpu_count

from abstand cimport Abstand
from betrag cimport Betrag
from kraft cimport Kraft
from beschleunigung cimport Beschleunigung
from update_position cimport update_position
from update_speed cimport update_speed
import numpy as np
cimport cython

@cython.boundscheck(False)
cpdef Loop (_args_dt, position, speed, masse):
    
    #Umwandlung in MemoryView
    cdef double [:, :] position_view = position
    cdef double [:, :] speed_view = speed
    cdef double [:, :] new_position_view = position
    cdef double [:, :] new_speed_view = speed 
    cdef double [:] masse_view = masse

    #Statische Variable
    cdef int dt = _args_dt
    cdef int number_planets = len(position)
    cdef int i, current_planet, planet
    
    #Temporaere MemoryView zum ZwischenSpeichern
    cdef int id
    cdef thread_num = cpu_count()  
    
    cdef double [:, :] distance = np.zeros((thread_num, 3),  dtype=np.float64)
    cdef double [:] magnitude = np.zeros(thread_num,  dtype=np.float64)
    cdef double [:, :] single_force = np.zeros((thread_num, 3),  dtype=np.float64)
    cdef double [:, :] all_force = np.zeros((thread_num, 3),  dtype=np.float64)
    cdef double [:, :] acceleration = np.zeros((thread_num, 3),  dtype=np.float64)
    
    for current_planet in range (number_planets):
        id = threadid()
        all_force[id][0] = 0
        all_force[id][1] = 0
        all_force[id][2] = 0

        for planet in prange(number_planets, nogil=True):                
            if (planet != current_planet):
                Abstand(position_view, distance, planet, current_planet, id)
                Betrag(distance, magnitude, id)
                Kraft(masse_view, distance, magnitude, planet, current_planet, single_force, id)
                all_force[id][0] += single_force[id][0]
                all_force[id][1] += single_force[id][1]
                all_force[id][2] += single_force[id][2]

        Beschleunigung(all_force, masse_view, current_planet, acceleration, id)
        update_position(position_view, new_position_view, speed_view, acceleration, dt, current_planet, id) 
        update_speed(speed_view , new_speed_view, acceleration, dt, current_planet, id)          

    position_view = new_position_view
    speed_view = new_speed_view
    
    position = np.asarray(position_view)
    speed = np.asarray(speed_view)