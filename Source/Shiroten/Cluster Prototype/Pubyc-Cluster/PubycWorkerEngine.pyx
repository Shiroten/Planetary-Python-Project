from cython.parallel import prange, threadid
from multiprocessing import cpu_count
from libc.math cimport sqrt
import numpy as np
cimport cython 

cpdef single_planet(dt, position, speed, masse, current_planet):  
    #Umwandlung in MemoryView
    cdef double [:, :] position_view = position
    cdef double [:, :] speed_view = speed
    cdef double [:]    mass_view = masse
    cdef double [:]    single_pos_speed
    
    single_pos_speed = cdef_single_planet(dt, position_view, speed_view, mass_view, current_planet)
    return ((single_pos_speed[0], single_pos_speed[1], single_pos_speed[2], \
            single_pos_speed[3], single_pos_speed[4], single_pos_speed[5]), current_planet)

@cython.boundscheck(False)
@cython.cdivision(True)
cdef double [:] cdef_single_planet(double dt, double [:, :] position_view, \
                        double [:, :] speed_view, double [:] mass_view, int current_planet):

    cdef int number_planets = len(position_view)
    cdef int i, planet, thread_id
    cdef int thread_num = cpu_count()
    cdef double G = 6.672e-11
    
    #Temporaere MemoryView zum ZwischenSpeichern
    cdef double [:, :]     distance = np.zeros((thread_num, 3),  dtype=np.float64)
    cdef double [:]       magnitude = np.zeros(thread_num,  dtype=np.float64)
    cdef double [:]  temp_magnitude = np.zeros(thread_num,  dtype=np.float64)
    cdef double [:]   mass_multyply = np.zeros(thread_num,  dtype=np.float64)
    cdef double [:]         gravity = np.zeros(thread_num,  dtype=np.float64)
    cdef double [:, :] single_force = np.zeros((thread_num, 3),  dtype=np.float64)
    
    cdef double [:]       all_force = np.zeros(3,  dtype=np.float64)
    cdef double [:]    acceleration = np.zeros(3,  dtype=np.float64)
    cdef double [:]    return_value = np.zeros(6,  dtype=np.float64)
    
    for planet in prange(number_planets, nogil=True, schedule='runtime'):  
        thread_id = threadid()
            
        if (planet != current_planet):                 
            distance[thread_id][0] = position_view[planet][0] - position_view[current_planet][0]
            distance[thread_id][1] = position_view[planet][1] - position_view[current_planet][1]
            distance[thread_id][2] = position_view[planet][2] - position_view[current_planet][2]

            magnitude[thread_id] = sqrt(distance[thread_id][0] * distance[thread_id][0] 
                                      + distance[thread_id][1] * distance[thread_id][1]
                                      + distance[thread_id][2] * distance[thread_id][2])

            temp_magnitude[thread_id] = magnitude[thread_id] * magnitude[thread_id] * magnitude[thread_id]
            mass_multyply[thread_id] = mass_view[planet] * mass_view[current_planet]
            gravity[thread_id] = G * (mass_multyply[thread_id] / temp_magnitude[thread_id])
            
            single_force[thread_id][0] = gravity[thread_id] * distance[thread_id][0]
            single_force[thread_id][1] = gravity[thread_id] * distance[thread_id][1]
            single_force[thread_id][2] = gravity[thread_id] * distance[thread_id][2]

            all_force[0] += single_force[thread_id][0]
            all_force[1] += single_force[thread_id][1]
            all_force[2] += single_force[thread_id][2]
            
    acceleration[0] = all_force[0] / mass_view[current_planet]
    acceleration[1] = all_force[1] / mass_view[current_planet]
    acceleration[2] = all_force[2] / mass_view[current_planet]        

    return_value[0] = position_view[current_planet][0]  \
                    + dt * speed_view[current_planet][0] \
                    + ((dt * dt) / 2) * acceleration[0]

    return_value[1] = position_view[current_planet][1] \
                    + dt * speed_view[current_planet][1] \
                    + ((dt * dt) / 2) * acceleration[1]

    return_value[2] = position_view[current_planet][2]  \
                    + dt * speed_view[current_planet][2] \
                    + ((dt * dt) / 2) * acceleration[2]

    return_value[3] = speed_view[current_planet][0] + dt * acceleration[0]
    return_value[4] = speed_view[current_planet][1] + dt * acceleration[1]
    return_value[5] = speed_view[current_planet][2] + dt * acceleration[2]             

    return return_value