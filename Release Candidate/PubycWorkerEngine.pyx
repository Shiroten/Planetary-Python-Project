from cython.parallel import prange, threadid
from multiprocessing import cpu_count
from libc.math cimport sqrt
import numpy as np
cimport cython 

cpdef single_planet(dt, position, speed, masse, lower_planet_index, upper_planet_index):  
    #Umwandlung in MemoryView
    cdef double [:, :] position_view = position
    cdef double [:, :] speed_view = speed
    cdef double [:]    mass_view = masse
    cdef double [:]    single_pos_speed
    
    return_list = []
        
    pos_speed = cdef_single_planet(dt, 
                                  position_view, 
                                  speed_view, 
                                  mass_view, 
                                  lower_planet_index, 
                                  upper_planet_index)
    
    for i in range(len(pos_speed)):
        return_list.append(((pos_speed[i][0], 
                             pos_speed[i][1], 
                             pos_speed[i][2], 
                             pos_speed[i][3], 
                             pos_speed[i][4], 
                             pos_speed[i][5]),
                             pos_speed[i][6]))   
        
    #print(return_list)    
    return return_list

@cython.boundscheck(False)
@cython.cdivision(True)
cdef double [:, :] cdef_single_planet(double dt, 
                                   double [:, :] position_view, 
                                   double [:, :] speed_view, 
                                   double [:] mass_view, 
                                   int lower_planet_index, 
                                   int upper_planet_index):

    cdef int number_planets = len(position_view)
    cdef int planet, current_planet, thread_id
    cdef int thread_num = cpu_count()
    cdef double G = 6.672e-11
    
    cdef int number_of_planets = upper_planet_index - lower_planet_index + 1
    cdef int result_index
    
    #Temporaere MemoryView zum ZwischenSpeichern
    cdef double [:, :]     distance = np.zeros((thread_num, 3),  dtype=np.float64)
    cdef double [:]       magnitude = np.zeros(thread_num,  dtype=np.float64)
    cdef double [:]  temp_magnitude = np.zeros(thread_num,  dtype=np.float64)
    cdef double [:]   mass_multyply = np.zeros(thread_num,  dtype=np.float64)
    cdef double [:]         gravity = np.zeros(thread_num,  dtype=np.float64)
    cdef double [:, :] single_force = np.zeros((thread_num, 3),  dtype=np.float64)
    
    cdef double [:, :]       all_force = np.zeros((thread_num, 3),  dtype=np.float64)
    cdef double [:, :]    acceleration = np.zeros((thread_num, 3),  dtype=np.float64)
    cdef double [:, :] return_value = np.zeros((number_of_planets, 7),  dtype=np.float64)
    
    for current_planet in prange (lower_planet_index, 
                                  upper_planet_index + 1, 
                                  nogil=True, 
                                  schedule='runtime'):
        
        result_index = current_planet - lower_planet_index
        thread_id = threadid()
        
        for planet in range(number_planets):  
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

                all_force[thread_id][0] += single_force[thread_id][0]
                all_force[thread_id][1] += single_force[thread_id][1]
                all_force[thread_id][2] += single_force[thread_id][2]

        acceleration[thread_id][0] = all_force[thread_id][0] / mass_view[current_planet]
        acceleration[thread_id][1] = all_force[thread_id][1] / mass_view[current_planet]
        acceleration[thread_id][2] = all_force[thread_id][2] / mass_view[current_planet]        

        return_value[result_index][0] = position_view[current_planet][0]  \
                                      + dt * speed_view[current_planet][0] \
                                      + ((dt * dt) / 2) * acceleration[thread_id][0]

        return_value[result_index][1] = position_view[current_planet][1] \
                                      + dt * speed_view[current_planet][1] \
                                      + ((dt * dt) / 2) * acceleration[thread_id][1]

        return_value[result_index][2] = position_view[current_planet][2]  \
                                      + dt * speed_view[current_planet][2] \
                                      + ((dt * dt) / 2) * acceleration[thread_id][2]

        return_value[result_index][3] = speed_view[current_planet][0] + dt * acceleration[thread_id][0]
        return_value[result_index][4] = speed_view[current_planet][1] + dt * acceleration[thread_id][1]
        return_value[result_index][5] = speed_view[current_planet][2] + dt * acceleration[thread_id][2]
        return_value[result_index][6] = current_planet

    return return_value