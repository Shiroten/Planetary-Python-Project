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
cpdef Loop (python_position, python_speed, python_masse):
    
    #Umwandeln in Numpy Arrays
    position = np.array(python_position, dtype=np.float64)
    speed = np.array(python_speed,dtype=np.float64)
    masse = np.array(python_masse,dtype=np.float64)

    #Umwandlung in MemoryView
    cdef double [:, :] position_view = position
    cdef double [:, :] speed_view = speed
    cdef double [:, :] new_position_view = position
    cdef double [:, :] new_speed_view = speed 
    cdef double [:] masse_view = masse

    #Statische Variable
    cdef int dt = 60
    cdef int number_planets = len(python_position)
    cdef int i, current_planet, planet
    cdef int list_index
    
    #Temporaere MemoryView zum ZwischenSpeichern
    cdef double [:] distance = np.array([0,0,0],  dtype=np.float64)
    cdef double [:] magnitude = np.array([0],  dtype=np.float64)
    cdef double [:] single_force = np.array([0,0,0],  dtype=np.float64)
    cdef double [:] all_force = np.array([0,0,0],  dtype=np.float64)
    cdef double [:] acceleration = np.array([0,0,0],  dtype=np.float64)
      
    for current_planet in prange (number_planets, nogil=True):

        all_force[0] = 0
        all_force[1] = 0
        all_force[2] = 0

        for planet in prange(number_planets):                
            if (planet != current_planet):
                Abstand(position_view, distance, planet, current_planet)
                Betrag(distance, magnitude)
                Kraft(masse_view, distance, magnitude, planet, current_planet, single_force)
                all_force[0] += single_force[0]
                all_force[1] += single_force[1]
                all_force[2] += single_force[2]

        Beschleunigung(all_force, masse_view, current_planet, acceleration)
        update_position(position_view, new_position_view, speed_view, acceleration, dt, current_planet) 
        update_speed(speed_view , new_speed_view, acceleration, dt, current_planet)          
    
    position = np.asarray(new_position_view)
    speed = np.asarray(new_speed_view)
    
    print(position)
    
    python_position = position.tolist()
    python_speed = speed.tolist()