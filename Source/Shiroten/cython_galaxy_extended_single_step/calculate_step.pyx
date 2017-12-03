from cython.parallel import prange
from abstand cimport Abstand
from betrag cimport Betrag
from kraft cimport Kraft
from beschleunigung cimport Beschleunigung
from update_position cimport update_position
from update_speed cimport update_speed
import numpy as np
cimport cython

#@cython.boundscheck(False)
cpdef void calculate_step(double [:, :] position_view, double [:, :] speed_view, \
                   double [:, :] new_position_view, double [:, :] new_speed_view, \
                   double [:] masse_view, double dt, int target_planet, int upper, int lower):

    #Statische Variable
    cdef int planet
    
    #Temporaere MemoryView zum ZwischenSpeichern
    cdef double [:] distance = np.array([0,0,0],  dtype=np.float64)
    cdef double [:] magnitude = np.array([0],  dtype=np.float64)
    cdef double [:] single_force = np.array([0,0,0],  dtype=np.float64)
    cdef double [:] all_force = np.array([0,0,0],  dtype=np.float64)
    cdef double [:] acceleration = np.array([0,0,0],  dtype=np.float64)
    
    for planet in prange(lower, upper, nogil=True):                
        if (planet != target_planet):
            Abstand(position_view, distance, planet, target_planet)
            
            with gil:
                print("distance", distance[0])
                print("distance", distance[1])
                print("distance", distance[2])
                
            Betrag(distance, magnitude)
            Kraft(masse_view, distance, magnitude, planet, target_planet, single_force)
            all_force[0] += single_force[0]
            all_force[1] += single_force[1]
            all_force[2] += single_force[2]
            
    Beschleunigung(all_force, masse_view, target_planet, acceleration)
    update_position(position_view, new_position_view, speed_view, acceleration, dt, target_planet) 
    update_speed(speed_view , new_speed_view, acceleration, dt, target_planet)   