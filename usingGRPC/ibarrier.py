import grpc
import barrier_pb2_grpc
import barrier_pb2
import sys

import threading
from time import sleep
import barrier_thread
import os



def run_tasks(process_rank,process_count,task_message):
    with grpc.insecure_channel('localhost:'+str(4000+process_rank+1)) as channel:
        stub = barrier_pb2_grpc.BarrierStub(channel)
        req= barrier_pb2.TaskRequest(rank=process_rank,barrier_count=process_count,message=str(task_message))
        response= stub.task(req)
        # print("Main:task response for rank",process_rank,response.arrived)

def run_barrier(thread_count):
    with grpc.insecure_channel('localhost:'+str(4001)) as channel:
        stub = barrier_pb2_grpc.BarrierStub(channel)
        argument=barrier_pb2.BarrierRequest()
        argument.rank=0
        argument.barrier_count=thread_count
        processlist=[]
        for i in range(thread_count):
            processlist.append(i)
        argument.ranklist.extend(processlist)
        response= stub.wait(argument)
        # print("Main:response for rank-",response.arrived)

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


    #assign task A
    for process_rank in range(thread_count):
        task1=threading.Thread(target=run_tasks,args=([process_rank,thread_count,"TASK A"]) )
        task1.start()

    #Barrier Invoked
    print("Calling Ibarrier")
    waittask=threading.Thread(target=run_barrier,args=([thread_count]) )
    waittask.start()
   

    #Assign computation between task A and B
    for process_rank in range(thread_count):
        task2=threading.Thread(target=run_tasks,args=([process_rank,thread_count,"Task between A&B"]) )
        task2.start()
    
    waittask.join()
    print('-' * term_size.columns)
    print("Ibarrier Wait Enforced Here")
    print('-' * term_size.columns)

    #Assign task B
    for process_rank in range(thread_count):
        task2=threading.Thread(target=run_tasks,args=([process_rank,thread_count,"TASK B"]) )
        task2.start()


    sleep(30)
    print('-' * term_size.columns)
    print("END")
    print('-' * term_size.columns)
    #end connections
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