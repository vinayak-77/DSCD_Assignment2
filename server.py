import random
import sys
import threading

import grpc
from concurrent import futures
import time
import raft_pb2, raft_pb2_grpc
import os
port = sys.argv[1]
other_nodes = ['localhost:50052']
leader = False


def timeout():
    time_rand = time.time() + random.uniform(1, 2)

    while True:
        if time.time() >= time_rand and not leader:
            StartElection()
            if leader:
                print("Leader")


def StartElection():

    global leader
    votes = 0
    for i in other_nodes:
        with grpc.insecure_channel(i) as channel:
            stub = raft_pb2_grpc.RaftStub(channel)

            request = raft_pb2.RequestVotesArgs(term=1,candidateId=other_nodes.index(i),lastLogTerm=0,lastLogIndex=0)

            response = stub.RequestVote(request)
            if (response.voteGranted == True):
                votes += 1
    if (votes >= len(other_nodes) / 2):
        leader = True


class RaftServicer(raft_pb2_grpc.RaftServicer):
    def AppendEntries(self, request, context):
        print(request.term)
        # return super().AppendEntries(request, context)

    def RequestVote(self, request, context):

        return raft_pb2.RequestVotesRes(term=1,voteGranted=True,longestDurationRem=0)
        # return super().RequestVote(request, context)

    def ServeClient(self, request, context):
        print(request.request)
        # return super().ServeClient(request, context)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1000))
    raft_pb2_grpc.add_RaftServicer_to_server(RaftServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    n = int(input("Enter Node ID : "))
    try:

        os.mkdir(f"logs_node_{n}", 0o777)
        path = os.getcwd() + f"/logs_node_{n}/"
        f = open(path + f"logs.txt", "a+")
        f1 = open(path + "metadata.txt", "a+")
        f2 = open(path + "dump.txt", "a+")
        if leader:
            command = input("Enter command")
            comm = command.split(" ")
            if comm[0] == "GET":
                print("Get Operation")
            elif comm[0] == "SET":
                print("Set Operation")
    except FileExistsError:
        pass

    try:
        while True:
            time.sleep(3600)  # One hour
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':

    if port =="50051":
        th = threading.Thread(target=timeout)
        try:
            th.start()
        except KeyboardInterrupt:
            th.join()
    else:
        serve()