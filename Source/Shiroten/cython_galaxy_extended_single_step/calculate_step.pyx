from cython.parallel import prange
from abstand cimport Abstand
from betrag cimport Betrag
from kraft cimport Kraft
from beschleunigung cimport Beschleunigung
from update_position cimport update_position
from update_speed cimport update_speed
import numpy as np
cimport cython

@cython.boundscheck(False)
cpdef void calculate_step(double [:, :] position_view, double [:, :] speed_view, \
                          double [:, :] new_position_view, double [:, :] new_speed_view, \
                          double [:] masse_view, double [:, :] temp_view, \
                          double dt, int target_planet, int upper, int lower):

    #Statische Variable
    cdef int planet
    
    #index distance 0
    #index magnitude 1
    #index single_force 2
    #index all_force 3
    #index acceleration 4
    
    temp_view[3][0] = 0
    temp_view[3][1] = 0
    temp_view[3][2] = 0
    
    for planet in prange(lower, upper, nogil=True):      
        if (planet != target_planet):
            Abstand(position_view, temp_view, planet, target_planet)              
            Betrag(temp_view)
            Kraft(masse_view, planet, target_planet, temp_view)
            temp_view[3][0] += temp_view[2][0]
            temp_view[3][1] += temp_view[2][1]
            temp_view[3][2] += temp_view[2][2]
            
    Beschleunigung(masse_view, target_planet, temp_view)
    update_position(position_view, new_position_view, speed_view, temp_view, dt, target_planet) 
    update_speed(speed_view , new_speed_view, temp_view, dt, target_planet)   