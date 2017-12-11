cdef void calculate_distance (double [:, :], double[:, :], int, int, int) nogil
cdef void calculate_magnitude (double [:, :], double[:], int) nogil
cdef void calculate_force (double [:], double [:, :],  double [:], int, int, double[:, :], int) nogil
cdef void calculate_acceleration (double [:, :], double [:], int, double[:, :], int) nogil
cdef void update_position (double [:, :], double [:, :], double [:, :],double [:, :], double, int, int) nogil
cdef void update_speed (double [:, :], double [:, :], double [:, :], double, int, int) nogil