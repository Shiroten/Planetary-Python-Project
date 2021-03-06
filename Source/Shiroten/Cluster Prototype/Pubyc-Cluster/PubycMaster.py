
from multiprocessing import cpu_count
from PubycTaskManager import TaskManager
import numpy as np
import time

def single_step_arguments(partsize, dt, position, speed, masse, l_in): 
    
    planet_number = len(position)-1
    parts = planet_number // partsize
    upper_planet_index = 0
    lower_planet_index = 0
    
    while (upper_planet_index - planet_number) < 0:
        
        if upper_planet_index + partsize < planet_number:
            upper_planet_index += partsize
        else:
            upper_planet_index = planet_number

        l_in.append((dt, position, speed, masse, lower_planet_index, upper_planet_index))  
        lower_planet_index = upper_planet_index + 1 
    
    return l_in

def update_list(result_tuple, position, speed):
        #print(result_tuple)
        position[(int)(result_tuple[1])] = (result_tuple[0][0], result_tuple[0][1], result_tuple[0][2])
        speed[(int)(result_tuple[1])] = (result_tuple[0][3], result_tuple[0][4], result_tuple[0][5]) 

def single_step(job_queue, result_queue, partsize, dt, position, speed, masse):
    arguments_list = []
    result_list = []

    arguments_list = single_step_arguments(partsize, dt, position, speed, masse, arguments_list)

    #print(arguments_list)
    
    for parameter_set in arguments_list:
        #print(parameter_set)
        job_queue.put(parameter_set)     

    counter1 = 0 
    counter2 = 0
    cache = []
    
    while len(cache) < len(position) / 5:
        cache.append(result_queue.get())
        
    for tuples in cache:
        update_list(tuples, position, speed)
        counter1 +=1
        
    while not result_queue.empty():
        update_list(result_queue.get(), position, speed)
        counter1 +=1
    
    job_queue.join()
    
    while not result_queue.empty():
        update_list(result_queue.get(), position, speed)
        counter2 +=1
    
    print(counter1, counter2)
        
       
        
if __name__ == '__main__':
    from sys import argv, exit
    if len(argv) != 8:
        print('usage:', argv[0], 'server_IP server_socket number_of_trys number_of_parts worker_count')
        exit(0)
    server_ip = argv[1]
    server_socket = int(argv[2])
    args_dt = argv[3]
    partsize = argv[4]
    position = argv[5]
    speed = argv[6]
    masse = argv[7]
    
    TaskManager.register('get_job_queue')
    TaskManager.register('get_result_queue')
    taskmanager = TaskManager(address=(server_ip, server_socket), authkey = b'secret')
    taskmanager.connect()
    job_queue, result_queue = taskmanager.get_job_queue(), taskmanager.get_result_queue()
    
    t1 = time.time()
    result = single_step(job_queue, result_queue, partsize, args_dt, position, speed, masse)
    t2 = time.time()
    
    print(' result: ', result)
    print(' time:   ', t2-t1, ' s\n')