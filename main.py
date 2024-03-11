from concurrent import futures

import grpc
import os

leader=False

def timeout():
    pass
def startelection():
    pass

def reqvote():
    pass

def resvote():
    pass



def run():
    n=int(input("Enter Node ID : "))
    try:
        os.mkdir(f"{n}", 0o777)
        path = os.getcwd()+f"/{n}/"
        f = open(path+f"logs_node_{n}.txt","a+")
        f1= open(path+"metadata.txt","a+")
        f2= open(path+"dump.txt","a+")
        if leader:
            command = input("Enter command")
            comm = command.split(" ")
            if comm[0]=="GET":
                print("Get Operation")
            elif comm[0]=="SET":
                print("Set Operation")
    except FileExistsError:
        pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # route_guide_pb2_grpc.add_RouteGuideServicer_to_server(RouteGuideServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        run()
    except KeyboardInterrupt:
        server.wait_for_termination()


serve()