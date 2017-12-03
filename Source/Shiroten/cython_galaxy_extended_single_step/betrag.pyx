cimport cython
from libc.math cimport sqrt


#Betrags Funktion
#Betrag_Erde  = sqrt( Abstand_Erde**2 + Abstand_Erde**2 + Abstand_Erde**2)
@cython.boundscheck(False)
@cython.cdivision(True)
cdef void Betrag (double [:, :] temp_view) nogil:
    
    #index magnitude 1
    temp_view[1][0] = sqrt(temp_view[0][0]**2 + temp_view[0][1]**2 + temp_view[0][2]**2)