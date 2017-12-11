from libc.math cimport sqrt
cimport cython

#Betrags Funktion
#Betrag_Erde  = sqrt( Abstand_Erde**2 + Abstand_Erde**2 + Abstand_Erde**2)
@cython.boundscheck(False)
@cython.cdivision(True)
cdef void Betrag (double [:, :] abstand_view , double[:] result, int id) nogil:
    result[id] = sqrt(abstand_view[id][0]**2 + abstand_view[id][1]**2 + abstand_view[id][2]**2)