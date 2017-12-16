from cython.parallel import prange , threadid
from multiprocessing import cpu_count
from libc.math cimport sqrt
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
    cdef double [:] mass_view = masse

    #Statische Variable
    cdef int dt = _args_dt
    cdef int number_planets = len(position)
    cdef int i, current_planet, planet, thread_id
    
    cdef int id
    cdef int thread_num = cpu_count()  
    #cdef int chunksize_number=number_planets//(4*thread_num)
    cdef int chunksize_number=10
    #cdef double G = 6.672 * 10.0e-11
    cdef double G = 6.672e-11
    cdef double temp_magnitude
    cdef double mass_multyply
    
    #Temporaere MemoryView zum ZwischenSpeichern
    cdef double [:, :] distance = np.zeros((thread_num, 3),  dtype=np.float64)
    cdef double [:]    magnitude = np.zeros(thread_num,  dtype=np.float64)
    cdef double [:, :] single_force = np.zeros((thread_num, 3),  dtype=np.float64)
    cdef double [:, :] all_force = np.zeros((thread_num, 3),  dtype=np.float64)
    cdef double [:, :] acceleration = np.zeros((thread_num, 3),  dtype=np.float64)
    
    for current_planet in prange (number_planets, nogil=True, 
                            schedule='runtime'):
                            #schedule='guided', chunksize=chunksize_number):
        id = threadid()
        thread_id = threadid()
        
        all_force[id][0] = 0
        all_force[id][1] = 0
        all_force[id][2] = 0

        for planet in range(number_planets):  
            if (planet != current_planet):
                distance[thread_id][0] = position_view[planet][0] - position_view[current_planet][0]
                distance[thread_id][1] = position_view[planet][1] - position_view[current_planet][1]
                distance[thread_id][2] = position_view[planet][2] - position_view[current_planet][2]

                magnitude[thread_id] = sqrt(distance[thread_id][0] * distance[thread_id][0] 
                                          + distance[thread_id][1] * distance[thread_id][1]
                                          + distance[thread_id][2] * distance[thread_id][2])

                temp_magnitude = magnitude[thread_id] * magnitude[thread_id] * magnitude[thread_id]
                mass_multyply = mass_view[planet] * mass_view[current_planet]

                single_force[thread_id][0] = G * (mass_multyply / temp_magnitude) * distance[thread_id][0]
                single_force[thread_id][1] = G * (mass_multyply / temp_magnitude) * distance[thread_id][1]
                single_force[thread_id][2] = G * (mass_multyply / temp_magnitude) * distance[thread_id][2]

                all_force[thread_id][0] += single_force[thread_id][0]
                all_force[thread_id][1] += single_force[thread_id][1]
                all_force[thread_id][2] += single_force[thread_id][2]

        acceleration[thread_id][0] = all_force[thread_id][0]  / mass_view[current_planet]
        acceleration[thread_id][1] = all_force[thread_id][1]  / mass_view[current_planet]
        acceleration[thread_id][2] = all_force[thread_id][2]  / mass_view[current_planet]

        new_position_view[current_planet][0] = position_view[current_planet][0]  \
                                    + dt * speed_view[current_planet][0] \
                                    + ((dt * dt) / 2) * acceleration[thread_id][0]

        new_position_view[current_planet][1] = position_view[current_planet][1] \
                                    + dt * speed_view[current_planet][1] \
                                    + ((dt * dt) / 2) * acceleration[thread_id][1]

        new_position_view[current_planet][2] = position_view[current_planet][2]  \
                                    + dt * speed_view[current_planet][2] \
                                    + ((dt * dt) / 2) * acceleration[thread_id][2]

        new_speed_view[current_planet][0] = speed_view[current_planet][0] + dt * acceleration[thread_id][0]
        new_speed_view[current_planet][1] = speed_view[current_planet][1] + dt * acceleration[thread_id][1]
        new_speed_view[current_planet][2] = speed_view[current_planet][2] + dt * acceleration[thread_id][2]          

    position_view = new_position_view
    speed_view = new_speed_view
    
    position = np.asarray(position_view)
    speed = np.asarray(speed_view)