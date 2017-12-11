cimport cython

#Kraft Funktion
#Kraft_Erde = G * (masse_erde * masse_sonne / (Betrag_Erde  ** 3)) * Abstand_Erde
@cython.boundscheck(False)
@cython.cdivision(True)
cdef void Kraft (double [:] masse_view, int head, int tail, double[:, :] temp_view) nogil:
    
    cdef double g1 = 6.672
    cdef double g2 = 10
    cdef double g3 = -11
    
    cdef double G = g1 * g2 ** g3
    
    #index magnitude 1
    cdef double betrag = temp_view[1][0] ** 3

    cdef double masse_multyply = masse_view[head] * masse_view[tail]
    
    #index distance 0
    #index single_force 2
    temp_view[2][0] = G * (masse_multyply / betrag) * temp_view[0][0]
    temp_view[2][1] = G * (masse_multyply / betrag) * temp_view[0][1]
    temp_view[2][2] = G * (masse_multyply / betrag) * temp_view[0][2]