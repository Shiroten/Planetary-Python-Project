
import sys
from loop import Loop
from simulation_constants import END_MESSAGE
import numpy as np
import math

def startup(sim_pipe):
    python_position = [
        #"Sun"
        [0, 0, 0],     
        #"Mercury"
        [57_909_175_000, 0, 0], 
        #"Venus"
        [108_208_930_000, 0, 0],    
        #"Earth"
        [149_597_890_000, 0, 0],    
        #"Moon"
        [149_597_890_000, 384_400_000, 0],    
        #"Mars"
        [227_936_640_000, 0, 0],    
        #"Jupiter"
        [778_412_020_000, 0, 0],    
        #"Saturn"
        [1_426_725_400_000, 0, 0],    
        #"Uranus"
        [2_870_972_200_000, 0, 0],    
        #"Neptune"
        [4_498_252_900_000, 0, 0]
    ]

    python_speed = [
        #"Sun"
        [0, 0, 0],     
        #"Mercury"
        [0, 47_872, 0], 
        #"Venus"
        [0, 35_021, 0],    
        #"Earth"
        [0, 29_786, 0],    
        #"Moon"
        [-1_022, 0, 0],    
        #"Mars"
        [0, 24_131, 0],    
        #"Jupiter"
        [0, 13_069, 0],    
        #"Saturn"
        [0, 9_672, 0],    
        #"Uranus"
        [0, 6_835, 0],    
        #"Neptune"
        [0, 5_477, 0]
    ]

    python_masse = [
        #"Sun"
        1.9889 * 10 ** 30,     
        #"Mercury"
        3.3022 * 10 ** 23, 
        #"Venus"
        4.8685 * 10 ** 24,    
        #"Earth"
        5.97219 * 10 ** 24,    
        #"Moon"
        7.34767309 * 10 ** 22,    
        #"Mars"
        6.4185 * 10 ** 23,    
        #"Jupiter"
        1.8987 * 10 ** 27,    
        #"Saturn"
        5.6851 * 10 ** 26,    
        #"Uranus"
        8.6849 * 10 ** 25,    
        #"Neptune"
        1.0244 * 10 ** 26
    ]

    FACTOR = 1
    radius =  [
        0.25 * FACTOR,
        0.02 * FACTOR,
        0.06 * FACTOR,
        0.06 * FACTOR,
        0.01 * FACTOR,
        0.03 * FACTOR,
        0.18 * FACTOR,
        0.15 * FACTOR,
        0.1 * FACTOR,
        0.1 * FACTOR
    ]
    position = np.array(python_position, dtype=np.float64)
    speed = np.array(python_speed, dtype=np.float64)
    masse = np.array(python_masse, dtype=np.float64)

    while True:
        if sim_pipe.poll():
            message = sim_pipe.recv()
            if isinstance(message, str) and message == END_MESSAGE:
                print('simulation exiting ...')
                sys.exit(0)

        Loop(position, speed, masse)

        body_array = np.zeros((len(python_position), 4), dtype=np.float64)
        normalization = -11
        
        for body_index in range(len(python_position)):
            body_array[body_index][0] = python_position[body_index][0] * math.pow(10, normalization)
            body_array[body_index][1] = python_position[body_index][1] * math.pow(10, normalization)
            body_array[body_index][2] = python_position[body_index][2] * math.pow(10, normalization)
            body_array[body_index][3] = radius[body_index]

        sim_pipe.send(body_array)