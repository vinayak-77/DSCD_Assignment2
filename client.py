import grpc

import raft_pb2_grpc
import raft_pb2

other_nodes = ['localhost:50051', 'localhost:50052']
leader_node = {0:'localhost:50051'}
leader_ip = 'localhost:50051'
ind = 0




def run():
    
    while(True):
        with grpc.insecure_channel(leader_ip) as channel:
            stub = raft_pb2_grpc.RaftStub(channel)
            req = input("Enter Request:")
            
            request = raft_pb2.ServeClientArgs(Request=req)
            res = stub.ServeClient(request)
            
            if(not res.Success):
                leader_ip = res.LeaderIp
            else:
                break


if __name__ == "main":
    run()
