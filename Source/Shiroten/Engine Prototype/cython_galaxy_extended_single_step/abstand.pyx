cimport cython
#Abstands Funktion
#Abstand_Sonne = position[1] - position[0]

@cython.boundscheck(False)
@cython.cdivision(True)
cdef void Abstand (double [:, :] position_view , double[:, :] temp_view, int head, int tail) nogil:  
    
    #index distance 0
    temp_view[0][0] = position_view[head][0] - position_view[tail][0]
    temp_view[0][1] = position_view[head][1] - position_view[tail][1]
    temp_view[0][2] = position_view[head][2] - position_view[tail][2]