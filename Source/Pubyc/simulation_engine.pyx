from cython.parallel import prange , threadid
from multiprocessing import cpu_count

from calculation_function cimport calculate_distance
from calculation_function cimport calculate_magnitude
from calculation_function cimport calculate_force
from calculation_function cimport calculate_acceleration
from calculation_function cimport update_position
from calculation_function cimport update_speed
import numpy as np
cimport cython

@cython.boundscheck(False)
@cython.cdivision(True)
cpdef single_step (_args_dt, position, speed, masse):
    
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
    
    cdef int id
    cdef int thread_num = cpu_count()  
    #cdef int chunksize_number=number_planets//(4*thread_num)
    cdef int chunksize_number=10
    
    #Temporaere MemoryView zum ZwischenSpeichern
    cdef double [:, :] distance = np.zeros((thread_num, 3),  dtype=np.float64)
    cdef double [:] magnitude = np.zeros(thread_num,  dtype=np.float64)
    cdef double [:, :] single_force = np.zeros((thread_num, 3),  dtype=np.float64)
    cdef double [:, :] all_force = np.zeros((thread_num, 3),  dtype=np.float64)
    cdef double [:, :] acceleration = np.zeros((thread_num, 3),  dtype=np.float64)
    
    for current_planet in prange (number_planets, nogil=True, 
                            schedule='runtime'):
                            #schedule='guided', chunksize=chunksize_number):
        id = threadid()
        all_force[id][0] = 0
        all_force[id][1] = 0
        all_force[id][2] = 0

        for planet in range(number_planets):  
            
            if (planet != current_planet):
                calculate_distance(position_view, distance, planet, current_planet, id)
                calculate_magnitude(distance, magnitude, id)
                calculate_force(masse_view, distance, magnitude, planet, current_planet, single_force, id)
                all_force[id][0] += single_force[id][0]
                all_force[id][1] += single_force[id][1]
                all_force[id][2] += single_force[id][2]

        calculate_acceleration(all_force, masse_view, current_planet, acceleration, id)
        update_position(position_view, new_position_view, speed_view, acceleration, dt, current_planet, id) 
        update_speed(speed_view , new_speed_view, acceleration, dt, current_planet, id)          

    position_view = new_position_view
    speed_view = new_speed_view
    
    position = np.asarray(position_view)
    speed = np.asarray(speed_view)