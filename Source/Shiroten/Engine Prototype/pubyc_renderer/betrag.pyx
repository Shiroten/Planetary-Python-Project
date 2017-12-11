cimport cython
from libc.math cimport sqrt


#Betrags Funktion
#Betrag_Erde  = sqrt( Abstand_Erde**2 + Abstand_Erde**2 + Abstand_Erde**2)
@cython.boundscheck(False)
@cython.cdivision(True)
cdef void Betrag (double [:] abstand_view , double[:] result) nogil:
    result[0] = sqrt(abstand_view[0]**2 + abstand_view[1]**2 + abstand_view[2]**2)