cimport cython
#Abstands Funktion
#Abstand_Sonne = position[1] - position[0]

@cython.boundscheck(False)
@cython.cdivision(True)
cdef void Abstand (double [:, :] position_view , double[:] result ,int head, int tail) nogil:   
    result[0] = position_view[head][0] - position_view[tail][0]
    result[1] = position_view[head][1] - position_view[tail][1]
    result[2] = position_view[head][2] - position_view[tail][2]