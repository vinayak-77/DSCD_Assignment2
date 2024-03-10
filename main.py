from concurrent import futures

import grpc
import os

def run():
    n=int(input("Enter Node ID : "))
    try:
        os.mkdir(f"{n}", 0o777)
        path = os.getcwd()+f"/{n}/"
        f = open(path+"logs.txt","w")
        f.write("Hello")
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