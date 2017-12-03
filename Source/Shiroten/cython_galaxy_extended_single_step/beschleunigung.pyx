cimport cython

#Beschleunigungs Funktion
#Beschleunigung_Erde  = Kraft_Erde  / masse
@cython.boundscheck(False)
@cython.cdivision(True)
cdef void Beschleunigung (double [:] masse_view, int massen_index, double[:, :] temp_view) nogil:
    cdef float G = 6.672 * 10 ** -11
    
    #index single_force 2
    #index acceleration 4
    temp_view[4][0] = temp_view[2][0]  / masse_view[massen_index]
    temp_view[4][1] = temp_view[2][1]  / masse_view[massen_index]
    temp_view[4][2] = temp_view[2][2]  / masse_view[massen_index]