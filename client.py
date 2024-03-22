import grpc

import raft_pb2
import raft_pb2_grpc



def run():
    leader_addr = "127.0.0.1:50052"
    while True:
        print(leader_addr)
        with grpc.insecure_channel(leader_addr) as channel:
            stub = raft_pb2_grpc.RaftStub(channel)
            req = input("Enter Request: ")
            print(req.split())
            res = stub.ServeClient(raft_pb2.ServeClientArgs(Request=req))
            print(res)

if __name__ == "__main__":
    run()
