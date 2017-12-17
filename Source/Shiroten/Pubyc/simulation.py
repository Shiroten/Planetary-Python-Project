from PubycMaster import single_step
from PubycTaskManager import TaskManager
import matplotlib.pyplot as plt
import numpy as np

import math
import sys
import time
import datetime

from simulation_constants import END_MESSAGE

def startup(sim_pipe, pos, vel, mass, rad, max_size, log, dt):
    position = np.array(pos, dtype=np.float64)
    speed = np.array(vel,dtype=np.float64)
    masse = np.array(mass,dtype=np.float64)

    TaskManager.register('get_job_queue')
    TaskManager.register('get_result_queue')
    server_ip = "192.168.178.210"
    server_socket = 12345
    taskmanager = TaskManager(address=(server_ip, server_socket), authkey = b'secret')
    taskmanager.connect()

    cnt = 0
    timer = datetime.datetime.now()
    
    while True:
        if sim_pipe.poll():
            message = sim_pipe.recv()
            if isinstance(message, str):
                if 'LOGN' in message:
                    log = float(message[5:])
                    print('Set log:', log)
                elif 'TIME' in message:
                    dt = float(message[5:])
                    print('Set delta time:', dt)
                elif message == END_MESSAGE:
                    print('simulation exiting ...')
                    sys.exit(0)
        
        single_step(taskmanager, dt, position, speed, masse)

        body_array = np.zeros((len(position), 4), dtype=np.float64)
        normalization = -11
        max_rad = max(rad)
        
        for body_index in range(len(position)):
            body_array[body_index][0] = position[body_index][0] / max_size
            body_array[body_index][1] = position[body_index][1] / max_size
            body_array[body_index][2] = position[body_index][2] / max_size
            body_array[body_index][3] = rad[body_index] / max_rad / 10

        sim_pipe.send(body_array)
        
        cnt = (cnt + 1) % 50
        timer_end = datetime.datetime.now()
        if cnt == 1:
            print(timer_end - timer)
        timer = timer_end
