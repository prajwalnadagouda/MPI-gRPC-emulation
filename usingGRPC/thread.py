import grpc
import barrier_pb2_grpc
import barrier_pb2
from concurrent import futures
import sys



class Barrier(barrier_pb2_grpc.BarrierServicer):
    def wait(self, request, context):
        print("Got request " + str(request))
        return barrier_pb2.BarrierResponse(arrived=True)


def server(portno):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    barrier_pb2_grpc.add_BarrierServicer_to_server(Barrier(), server)
    print('[::]:'+str(portno))
    server.add_insecure_port('[::]:'+str(portno))
    print("gRPC starting")
    server.start()
    server.wait_for_termination()

def main(portno):
    server(portno)


if __name__ == "__main__":
    try:
        portno=int(sys.argv[1])
    except:
        print("Wrong arguments")
        exit()
    main(portno)