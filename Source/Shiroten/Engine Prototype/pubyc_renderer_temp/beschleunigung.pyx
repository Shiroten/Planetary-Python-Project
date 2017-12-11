cimport cython

#Beschleunigungs Funktion
#Beschleunigung_Erde  = Kraft_Erde  / masse
@cython.boundscheck(False)
@cython.cdivision(True)
cdef void Beschleunigung (double [:] kraft_view , double [:] masse_view, int massen_index, double[:] result) nogil:
    cdef float G = 6.672 * 10 ** -11
    result[0] = kraft_view[0]  / masse_view[massen_index]
    result[1] = kraft_view[1]  / masse_view[massen_index]
    result[2] = kraft_view[2]  / masse_view[massen_index]