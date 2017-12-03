cimport cython

#Kraft Funktion
#Kraft_Erde = G * (masse_erde * masse_sonne / (Betrag_Erde  ** 3)) * Abstand_Erde
@cython.boundscheck(False)
@cython.cdivision(True)
cdef void Kraft (double [:] masse_view, double [:] abstand_view,  double [:] Betrag, \
                  int head, int tail, double[:] result) nogil:
    
    cdef double g1 = 6.672
    cdef double g2 = 10
    cdef double g3 = -11
    
    cdef double G = g1 * g2 ** g3
    cdef double betrag = Betrag[0] ** 3

    cdef double masse_multyply = masse_view[head] * masse_view[tail]
    
    result[0] = G * (masse_multyply / betrag) * abstand_view[0]
    result[1] = G * (masse_multyply / betrag) * abstand_view[1]
    result[2] = G * (masse_multyply / betrag) * abstand_view[2]