from PubycWorkerEngine import single_planet
from PubycTaskManager import TaskManager
from multiprocessing import cpu_count, Process

def worker_single_planet(job_queue, result_queue):
    while True:
        args = job_queue.get()
        
        dt = args [0]
        position = args [1]
        speed = args [2]
        mass = args [3]
        lower_planet_index = args [4]
        upper_planet_index = args [5]

        result = single_planet(dt, position, speed, mass, lower_planet_index, upper_planet_index)
        
        for result_tuple in result:
            result_queue.put(result_tuple)
        
        job_queue.task_done()

        
def start_workers(m):
    job_queue, result_queue = m.get_job_queue(), m.get_result_queue()
    nr_of_processes = cpu_count()
    processes = [
            Process(target = worker_single_planet, args = (job_queue, result_queue))
            for i in range(nr_of_processes)
    ]
    
    for p in processes:
        p.start()
    return nr_of_processes


if __name__ == '__main__':
    from sys import argv, exit
    if len(argv) < 3:
        print('usage:', argv[0], 'server_IP server_socket')
        exit(0)
    server_ip = argv[1]
    server_socket = int(argv[2])
    TaskManager.register('get_job_queue')
    TaskManager.register('get_result_queue')
    m = TaskManager(address=(server_ip, server_socket), authkey = b'secret')
    m.connect()
    nr_of_processes = start_workers(m)
    print(nr_of_processes, 'workers started')