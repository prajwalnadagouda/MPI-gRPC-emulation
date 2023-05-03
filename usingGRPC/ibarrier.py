import grpc
import barrier_pb2_grpc
import barrier_pb2
import sys

import threading
from time import sleep
import barrier_thread
import os



def run_tasks(process_rank,process_count):
    with grpc.insecure_channel('localhost:'+str(4000+process_rank)) as channel:
        stub = barrier_pb2_grpc.BarrierStub(channel)
        req= barrier_pb2.BarrierRequest(rank=process_rank,barrier_count=process_count)
        response= stub.wait(req)
        print("response for rank",process_rank,response.arrived)

def run_barrier():
    pass

def main(thread_count):
    term_size = os.get_terminal_size()
    print("Number of threads",thread_count)
    #start 
    process_init_list=[]
    for process_rank in range(thread_count):
        process_init=threading.Thread(target=barrier_thread.main,args=([4000+process_rank+1]) )
        process_init.start()
        process_init_list.append(process_init)
    sleep(1)
    print('-' * term_size.columns)


    #assign task1
    for process_rank in range(thread_count):
        task1=threading.Thread(target=run_tasks,args=([process_rank+1,thread_count]) )
        task1.start()

    #Barrier Invoked
    run_barrier()

    #Assign task2
    for process_rank in range(thread_count):
        task2=threading.Thread(target=run_tasks,args=([process_rank+1,thread_count]) )
        task2.start()


    #end connections
    sleep(2)
    print('-' * term_size.columns)
    for process_rank in range(thread_count):
        x=threading.Thread(target=barrier_thread.close,args=() )
        x.start()


    


if __name__ == "__main__":
    try:
        thread_count=int(sys.argv[1])
    except:
        print("Wrong arguments")
        exit()
    main(thread_count)