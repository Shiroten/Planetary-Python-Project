from calculate_step cimport calculate_step
from calculate_step import calculate_step
import numpy as np
cimport cython

@cython.boundscheck(False)
cpdef Loop (args_dt, args_iteration, python_position, python_speed, python_masse, pos_list):
    
    #Umwandeln in Numpy Arrays
    position = np.array(python_position, dtype=np.float64)
    speed = np.array(python_speed, dtype=np.float64)
    masse = np.array(python_masse, dtype=np.float64)

    #Umwandlung in MemoryView
    cdef double [:, :] position_view = position
    cdef double [:, :] speed_view = speed
    cdef double [:, :] new_position_view = position
    cdef double [:, :] new_speed_view = speed 
    cdef double [:] masse_view = masse

    #Statische Variable
    cdef double dt = args_dt
    cdef int number_planets = len(python_position)
    cdef int i, current_planet, list_index
    cdef int iteration = args_iteration
    
    #Dynamische Variable
    cdef double [:, :]  temp_view = np.arange(15, dtype=np.dtype("d")).reshape((5, 3))
            
    for i in range (iteration): 
        for current_planet in range (number_planets):
            calculate_step(position_view, speed_view, new_position_view, \
            new_speed_view, masse_view, temp_view, dt, current_planet, number_planets, 0)
        
        position_view = new_position_view
        speed_view = new_speed_view
        
        pos_list_entry = []
        for list_index in range(number_planets):
            pos_list_entry.append(np.array((position_view[list_index][0], position_view[list_index][1],\
            position_view[list_index][2]), np.float64))
        
        pos_list.append(np.array(pos_list_entry, np.float64))