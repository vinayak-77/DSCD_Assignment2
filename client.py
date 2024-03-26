import grpc

import raft_pb2
import raft_pb2_grpc

NodeList = {1: '127.0.0.1:50051', 2: '127.0.0.1:50052', 3: '127.0.0.1:50053', 4: '127.0.0.1:50054'}


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
            if not res.Success:
                with grpc.insecure_channel(NodeList[int(res.LeaderID)]) as channel2:
                    stub2 = raft_pb2_grpc.RaftStub(channel2)
                    res = stub2.ServeClient(raft_pb2.ServeClientArgs(Request=req))
                    print(res)
                    leader_addr = NodeList[int(res.LeaderID)]


if __name__ == "__main__":
    run()
