import grpc
import barrier_pb2_grpc
import barrier_pb2
import sys

import threading
from time import sleep


def run_barrier(process_rank,process_count):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = barrier_pb2_grpc.BarrierStub(channel)
        req= barrier_pb2.BarrierRequest(rank=process_rank,barrier_count=process_count)
        response= stub.wait(req)
        print("response from rank-",process_rank,response)



def main(thread_count):  
    print("Number of threads",thread_count)
    for process_rank in range(thread_count):
        x=threading.Thread(target=run_barrier,args=([process_rank+1,thread_count]) )
        x.start()
    sleep(5)

    


if __name__ == "__main__":
    try:
        thread_count=int(sys.argv[1])
    except:
        print("Wrong arguments")
        exit()
    main(thread_count)