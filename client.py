import grpc

import raft_pb2_grpc

other_nodes = ['localhost:50051', 'localhost:50052']
ind = 0


def run():
    for i in other_nodes:
        with grpc.insecure_channel(i) as channel:
            stub = raft_pb2_grpc.RaftStub(channel)
            req = input("Enter Request:")
            reql = req.split(" ")
            if reql == "GET":
                pass
                # Get req
            else:
                #Set req
                pass


if __name__ == "main":
    run()
