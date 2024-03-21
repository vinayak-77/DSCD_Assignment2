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
            if(not res.Success):
                with open("nodes.txt","r") as f:
                    nodes = f.readlines()
                    for node in nodes:
                        
                        if(len(node.split()) >= 2 and node.split()[1] == str(res.LeaderID)):
                            leader_addr = node.split()[0]
                            print(leader_addr)
                            print("Here")
            print(res)


if __name__ == "__main__":
    run()
