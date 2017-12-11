cimport cython

#Geschwindigkeits Aktuallisierung
#geschwindigkeit[0][0]  += dt * Beschleunigung_Erde[0]
@cython.boundscheck(False)
@cython.cdivision(True)
cdef void update_speed (double [:, :] speed_view, double [:, :] new_speed_view, \
                        double [:, :] temp_view, double dt ,int planet_index) nogil:
    
    #index acceleration 4
    new_speed_view[planet_index][0] = speed_view[planet_index][0] + dt * temp_view[4][0]
    new_speed_view[planet_index][1] = speed_view[planet_index][1] + dt * temp_view[4][1]
    new_speed_view[planet_index][2] = speed_view[planet_index][2] + dt * temp_view[4][2]