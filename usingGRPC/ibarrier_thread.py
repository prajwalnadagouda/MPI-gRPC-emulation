import grpc
import barrier_pb2_grpc
import barrier_pb2
from concurrent import futures
import sys

import time
import threading 
from random import randrange
from sys import stdout
LOCK=1

from termcolor import colored

class Barrier(barrier_pb2_grpc.BarrierServicer):
    def __init__(self,portno) -> None:
        self.id=portno
    

    def task(self, request, context):
        global LOCK
        LOCK=1
        printstatement="TASK:GOT task-"+request.message+" on "+str(request.rank)+"\n"
        print(colored(printstatement,"green"))
        time.sleep(randrange(4,10)) #assign random runtime
        printstatement="TASK:DONE task-"+request.message+" on "+str(request.rank)+"\n"
        print(colored(printstatement,"blue"))
        time.sleep(2)
        LOCK=0
        return barrier_pb2.TaskResponse(arrived=False)


    def inside_wait(ranklist):
        length=len(ranklist)
        if(length==1):
            return True
        
        index=highestPowerof2(length)
        if(index==length):
            index=int(index/2)

        with grpc.insecure_channel('localhost:'+str(4001+ranklist[index])) as channel:
            stub = barrier_pb2_grpc.BarrierStub(channel)
            argument=barrier_pb2.BarrierRequest()
            argument.rank=index
            argument.barrier_count=length-index
            processlist=ranklist[index:]
            argument.ranklist.extend(processlist)
            response= stub.wait(argument)
        Barrier.inside_wait(ranklist[:index]) 


    def wait(self, request, context):
        global LOCK
        while LOCK:
            time.sleep(2)
            pass
        printstatement="BARRIER:GOT sync "+" on "+str(request.ranklist[0])+"\n"
        print(colored(printstatement,"red"))
        length=len(request.ranklist)
        if(length==1):
            return barrier_pb2.BarrierResponse(arrived=True)
        
        Barrier.inside_wait(request.ranklist)
        LOCK=1
        return barrier_pb2.BarrierResponse(arrived=True)

def server(portno):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    barrier_pb2_grpc.add_BarrierServicer_to_server(Barrier(portno), server)
    server.add_insecure_port('[::]:'+str(portno))
    print("gRPC starting-",portno)
    server.start()
    server.wait_for_termination()

def close():
    print("Closing process")
    exit()

def highestPowerof2(n):
    res = 0
    for i in range(n, 0, -1):
        # If i is a power of 2
        if ((i & (i - 1)) == 0):
            res = i
            break
    return res
def main(portno):
    
    server(portno)


if __name__ == "__main__":
    try:
        portno=int(sys.argv[1])
    except:
        print("Wrong arguments")
        exit()
    main(portno)