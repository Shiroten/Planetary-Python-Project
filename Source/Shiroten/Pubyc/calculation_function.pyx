cimport cython
#Abstands Funktion
#Abstand_Sonne = position[1] - position[0]

@cython.boundscheck(False)
@cython.cdivision(True)
cdef void calculate_distance (double [:, :] position_view , double[:, :] result ,int head, int tail, int id) nogil: 
    result[id][0] = position_view[head][0] - position_view[tail][0]
    result[id][1] = position_view[head][1] - position_view[tail][1]
    result[id][2] = position_view[head][2] - position_view[tail][2]
    
from libc.math cimport sqrt
#Betrags Funktion
#Betrag_Erde  = sqrt( Abstand_Erde**2 + Abstand_Erde**2 + Abstand_Erde**2)
@cython.boundscheck(False)
@cython.cdivision(True)
cdef void calculate_magnitude (double [:, :] abstand_view , double[:] result, int id) nogil:
    result[id] = sqrt(abstand_view[id][0]**2 + abstand_view[id][1]**2 + abstand_view[id][2]**2)
    
#Kraft Funktion
#Kraft_Erde = G * (masse_erde * masse_sonne / (Betrag_Erde  ** 3)) * Abstand_Erde
@cython.boundscheck(False)
@cython.cdivision(True)
cdef void calculate_force (double [:] masse_view, double [:, :] abstand_view,  double [:] Betrag, \
                  int head, int tail, double[:, :] result, int id) nogil:
    
    cdef double g1 = 6.672
    cdef double g2 = 10
    cdef double g3 = -11
    
    cdef double G = g1 * g2 ** g3
    cdef double betrag = Betrag[id] ** 3

    cdef double masse_multyply = masse_view[head] * masse_view[tail]
    
    result[id][0] = G * (masse_multyply / betrag) * abstand_view[id][0]
    result[id][1] = G * (masse_multyply / betrag) * abstand_view[id][1]
    result[id][2] = G * (masse_multyply / betrag) * abstand_view[id][2]
    
#Beschleunigungs Funktion
#Beschleunigung_Erde  = Kraft_Erde  / masse
@cython.boundscheck(False)
@cython.cdivision(True)
cdef void calculate_acceleration (double [:, :] kraft_view , double [:] masse_view, \
                          int massen_index, double[:, :] result, int id) nogil:
    cdef float G = 6.672 * 10 ** -11
    result[id][0] = kraft_view[id][0]  / masse_view[massen_index]
    result[id][1] = kraft_view[id][1]  / masse_view[massen_index]
    result[id][2] = kraft_view[id][2]  / masse_view[massen_index]
    
#Positions Aktualliersierung
#position = position + dt * geschwindigkeit  + ((dt ** 2) / 2) * Beschleunigung_Erde
@cython.boundscheck(False)
@cython.cdivision(True)
cdef void update_position (double [:, :] position_view , double [:, :] new_postion_view, \
                   double [:, :] speed_view, double [:, :] beschleunigung_view, \
                        double dt, int planet_index, int id) nogil:
    
    new_postion_view[planet_index][0] = position_view[planet_index][0]  + dt * speed_view[planet_index][0] \
                                                + ((dt ** 2) / 2) * beschleunigung_view[id][0]
        
    new_postion_view[planet_index][1] = position_view[planet_index][1]  + dt * speed_view[planet_index][1] \
                                                + ((dt ** 2) / 2) * beschleunigung_view[id][1]
        
    new_postion_view[planet_index][2] = position_view[planet_index][2]  + dt * speed_view[planet_index][2] \
                                                + ((dt ** 2) / 2) * beschleunigung_view[id][2]
        
#Geschwindigkeits Aktuallisierung
#geschwindigkeit[0][0]  += dt * Beschleunigung_Erde[0]
@cython.boundscheck(False)
@cython.cdivision(True)
cdef void update_speed (double [:, :] speed_view, double [:, :] new_speed_view, \
                        double [:, :] beschleunigung_view, double dt ,int planet_index, int id) nogil:
    new_speed_view[planet_index][0] = speed_view[planet_index][0] + dt * beschleunigung_view[id][0]
    new_speed_view[planet_index][1] = speed_view[planet_index][1] + dt * beschleunigung_view[id][1]
    new_speed_view[planet_index][2] = speed_view[planet_index][2] + dt * beschleunigung_view[id][2]