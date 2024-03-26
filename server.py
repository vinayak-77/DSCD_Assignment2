import os
import random
import socket
import sys
import threading
import time
from concurrent import futures
from logEntry import LogEntry

import grpc

import raft_pb2
import raft_pb2_grpc
from raftNode import Node, NodeList

port = sys.argv[1]
nodeId = sys.argv[2]
ip = socket.gethostbyname(socket.gethostname())

leader = False

node: Node = Node(nodeId=nodeId, ip=ip, port=port)

open_nodes = {}


def NodeDetector():
    time.sleep(4)

    while True:
        f = open("nodes.txt", "r")
        nodes = f.read().split("\n")
        f.close()
        for i in nodes:
            k = i.split(" ")
            if k == ['']:
                continue
            if int(k[1]) not in open_nodes:
                open_nodes[int(k[1])] = k[0]
                print(open_nodes)


def setValue(key, value):
    # readItr = open("data.txt", "r")
    writeItr = open("data.txt", "a")
    print("FILE OPENED")
    # entries = readItr.readlines()

    writeItr.write(key + " " + value + "\n")

    writeItr.close()
    # readItr.close()
    return -1


def getValue(key):
    readItr = open("data.txt", "r")
    entries = readItr.readlines()
    for entry in entries:
        if entry.split(" ")[0] == key:
            readItr.close()
            return entry.split(" ")[1]
    readItr.close()
    return "NO"


def noOp():
    writeItr = open("data.txt", "a")
    writeItr.write("No-Op+\n")
    writeItr.close()
    return "NO"


def ReplicateLogs(req):
    node.acquireLease()
    prefix = node.sentLength[req[2]]
    suffix = node.log[prefix:]
    prefixTerm = 0
    if prefix > 0:
        prefixTerm = node.log[prefix - 1].term

    # request = raft_pb2.AppendEntriesArgs()

    with grpc.insecure_channel(req[3]) as channel:
        stub = raft_pb2_grpc.RaftStub(channel)
        req = raft_pb2.ReplicateLogRequestArgs(leaderId=node.nodeId, currentTerm=node.currentTerm,
                                               prefixLen=prefix, prefixTerm=prefixTerm,
                                               commitLength=node.commitLength, suffix=suffix)
        res = stub.ReplicateLogRequest(req)
        print(res)


def sendHeartbeat():

    while True:
        time.sleep(2)
        if node.isLeader:

            for j, i in open_nodes.items():
                if i == node.ipAddr + ":" + node.port:
                    continue
                with grpc.insecure_channel(i) as channel:
                    stub = raft_pb2_grpc.RaftStub(channel)
                    res = stub.RefreshLease(raft_pb2.LeaseReq(ack=1))
                    channel.close()


def timeout():
    time_rand = time.time() + random.uniform(1, 2)
    while True:
        if time.time() >= time_rand:
            return True


def StartElection():
    longestLease = 0
    leaseStart = 0
    node.startTimer()

    for j, i in open_nodes.items():
        if i == node.ipAddr + ":" + node.port:
            continue
        with grpc.insecure_channel(i) as channel:
            stub = raft_pb2_grpc.RaftStub(channel)
            request = raft_pb2.RequestVotesArgs(term=node.currentTerm, candidateId=j, lastLogTerm=node.lastTerm,
                                                lastLogIndex=node.lastIndex)
            response = stub.RequestVote(request)

            if response.longestDurationRem > longestLease:
                longestLease = response.longestDurationRem
                leaseStart = time.time

            if response.voteGranted == True and node.currentRole == "Candidate" and node.currentTerm == response.term:
                node.votesReceived.append(response.NodeId)

    if len(node.votesReceived) >= len(open_nodes) / 2:

        while time.time() < leaseStart + longestLease:
            time.sleep(0.5)
        node.acquireLease()
        print(node.votesReceived)
        print("Leader")
        node.currentRole = "Leader"
        node.currentLeader = node.nodeId
        node.isLeader=True
        node.leaderId = node.nodeId
        # TODO: Need to think how to get the ip address of followers: One way is to assume every node sent it. which is done below
        for j, i in open_nodes.items():
            if i == Node.ipAddr + Node.port:
                continue

            # Replicating logs
            entry = LogEntry(node.lastTerm, node.lastIndex + 1, "NO-OP", "")
            node.log.append(entry)
            node.sentLength[j] = len(node.log)
            node.ackedLength[j] = 0
            req1 = [node.nodeId, open_nodes[node.nodeId], j, i]
            print(req1)
            ReplicateLogs(req1)

    else:
        print("Follower")
        if response.term > node.currentTerm:
            node.currentTerm = response.term
            node.currentRole = "Follower"
            node.votedFor = None


def SendBroadcast(msg):
    if node.currentRole == "Leader":
        node.log.append(msg)
        node.ackedLength[node.nodeId] = len(node.log)
        for j, i in open_nodes.items():
            if i == Node.ipAddr + Node.port:
                continue
                # Replicating logs

            queryNode = open_nodes[j]  # ! Replace i with node id
            prefixLen = queryNode.sentLength
            suffix = []
            for entryInd in range(prefixLen, len(node.log)):
                logEntry = node.log[entryInd]
                suffix.append(raft_pb2.entry(index=logEntry.index, term=logEntry.term, key=logEntry.key,
                                             val=logEntry.val))

            # request = raft_pb2.AppendEntriesArgs()
            req = raft_pb2.ReplicateLogRequestArgs(leaderId=node.nodeId, currentTerm=node.currentTerm,
                                                   prefixLen=prefixLen, prefixTerm=node.log[prefixLen - 1].term,
                                                   commitLength=node.commitLength, suffix=suffix)
            req1 = [node.nodeId, open_nodes[node.nodeId], j, i]
            ReplicateLogs(req1)
    else:
        # Send to leader via FIFO link? No idea
        # ? Should the nodes pass the client message to leader normally ?
        pass


def SuspectFail():
    return False


class RaftServicer(raft_pb2_grpc.RaftServicer):

    def AppendEntries(self, request, context):

        if len(request.suffix) > 0 and len(node.log) > request.prefixLen:
            index = min(len(node.log), request.prefixLen + len(request.suffix)) - 1
            if node.log[index].term != request.suffix[index - request.prefixLen].term:
                node.log = node.log[0:request.prefixLen]

        if request.prefixLen + len(request.suffix) > len(node.log):
            for i in range(len(node.log) - request.prefixLen, len(request.suffix)):
                node.log.append(request.suffix[i])

        if request.leaderCommit > node.commitLength:
            for i in range(node.commitLength, request.leaderCommit):
                pass  # !TODO send back to application
            node.commitLength = request.leaderCommit
        print(request.term)
        # return super().AppendEntries(request, context)

    def RequestVote(self, request, context):

        if request.term > node.currentTerm:
            node.currentTerm = request.term
            node.currentRole = "Follower"
            node.votedFor = None
        node.lastTerm = 0
        if len(node.log) > 0:
            node.lastTerm = node.log[len(node.log) - 1].term

        ok = (request.lastLogTerm > node.lastTerm) or (
                request.lastLogTerm == node.lastTerm and request.lastLogIndex >= len(node.log))

        vote = True

        if request.term == node.currentTerm and ok and node.votedFor is None:
            node.votedFor = request.candidateId
            node.val = True
            node.leaderId = request.candidateId

        else:

            vote = False
        longestLease = 0
        if node.leaseStartTime > 0:
            longestLease = time.time() - node.leaseStartTime

        return raft_pb2.RequestVotesRes(term=node.currentTerm, voteGranted=vote, longestDurationRem=longestLease,
                                        NodeId=node.nodeId)

    def ServeClient(self, request, context):
        print(node.nodeId, node.currentLeader)
        req = request.Request.split(" ")
        # request = request.Request.split(" ")
        operation = req[0]
        print(operation)
        data = ""
        # # ! Pass the message to leader
        # # TODO
        if node.nodeId != node.currentLeader:
            print("Not leader ....")
            return raft_pb2.ServeClientReply(Data=str(data), LeaderID=str(node.currentLeader), Success=False)
        else:
            if operation == "SET":
                key = req[1]
                value = req[2]
                node.data[key] = value
                writer = open(f"logs_node_{node.nodeId}/logs.txt", "a")
                writer.write(f"SET {key} {value} {node.currentTerm}")
                print(node.data)
                entry = LogEntry(node.lastTerm, node.lastIndex + 1, key, value)
                # node.log.append(entry)
                SendBroadcast(entry)
            elif operation == "GET":
                print("Get req")
                key = req[1]
                for entry in node.log:
                    if entry.key == key:
                        data = entry.value
                # data = str(node.data[key])
                # print(node.data[key])
            else:

                data = noOp()
                entry = LogEntry(node.lastTerm, node.lastIndex + 1, "NO-OP", "")
                # node.log.append(entry)
                SendBroadcast(entry)

        return raft_pb2.ServeClientReply(Data=str(data), LeaderID=str(node.currentLeader), Success=True)
        # print(request.request)
        # return super().ServeClient(request, context)

    def ReplicateLogRequest(self, request, context):
        # if(request.term > )
        # TODO implement this functionality
        if request.currentTerm > node.currentTerm:
            node.currentTerm = request.currentTerm
            node.votedFor = None
            # Cancel Election
        if request.currentTerm == node.currentTerm:
            node.currentRole = "Follower"
            node.currentLeader = request.leaderId
        ok = (len(node.log) >= request.prefixLen) or (
                request.prefixLen == 0 and node.log[request.prefixLen - 1].term == request.prefixTerm)
        if node.currentTerm == request.currentTerm and ok:
            # Append Entries
            req = raft_pb2.AppendEntriesArgs(term=node.currentTerm, leaderId=node.currentLeader,
                                             prevLogIndex=node.lastIndex, prevLogTerm=node.lastTerm,
                                             suffix=request.suffix, leaderCommit=request.commitLength, leaseInterval=0,
                                             prefixLen=request.prefixLen)
            res = self.AppendEntries(req, context)
            ack = request.prefixLen + len(request.suffix)
            with grpc.insecure_channel(open_nodes[node.currentLeader]) as channel:
                stub = raft_pb2_grpc.RaftStub(channel)
                req = raft_pb2.ReplicateLogResponseArgs(followerId=node.nodeId, followerTerm=node.currentTerm, ack=ack,
                                                        success=True)
                res = stub.ReplicateLogResponse(req)
                print(res)
            # Send Ack to leader of success
        else:
            # Send Ack to leader of failure
            with grpc.insecure_channel(open_nodes[node.leaderId]) as channel:
                stub = raft_pb2_grpc.RaftStub(channel)
                req = raft_pb2.ReplicateLogResponseArgs(followerId=node.nodeId, followerTerm=node.currentTerm,ack=0,success= False)
                res = stub.ReplicateLogResponse(req)
        return raft_pb2.ReplicateLogRequestRes(nodeId=node.nodeId, currentTerm=node.currentTerm, ackLen=0,
                                               receivedMessage=True)

    def ReplicateLogResponse(self, request, context):
        if node.currentTerm == request.followerTerm and node.currentRole == "Leader":
            if request.success == True and request.ack >= node.ackedLength[request.followerId]:
                node.sentLength[request.followerId] = request.ack
                node.ackedLength[request.followerId] = request.ack
                # Commit Log
                req = raft_pb2.CommitArgs()
                res = self.CommitEntries(req, context)
            elif node.sentLength[request.followerId] > 0:
                node.sentLength[request.followerId] -= 1
                # Replicate Log
        elif request.followerTerm > node.currentTerm:
            node.currentTerm = request.followerTerm
            node.currentRole = "Follower"
            node.votedFor = None
            # Cancel Election
        return raft_pb2.ReplicateLogResponseRes()

    def CommitEntries(self, request, context):
        minacks = (len(open_nodes) + 1) / 2
        ready = []
        # TODO: Didnt get this
        for i in range(1, len(node.log)):
            ready.append(0)
        if ready != [] and max(ready) > node.commitLength and node.log[max(ready) - 1].term == node.currentTerm:
            for i in range(node.commitLength, max(ready)):
                # Deliver Log message to application
                continue
            node.commitLength = max(ready)

    def RefreshLease(self, request, context):
        if request.ack == 1:
            print(f"Lease Renewed by Leader: {node.currentLeader}")
            node.cancel()
        return raft_pb2.LeaseRes(ack=1)


def serve():
    global node
    n = -1
    addr = ip + ":" + port
    for k, v in NodeList.items():
        if v == addr:
            n = k
    print(n, addr)
    f = open("nodes.txt", "a")
    f.write(ip + ":" + port + " " + str(n) + " " + "\n")
    f.close()
    time.sleep(10)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    raft_pb2_grpc.add_RaftServicer_to_server(RaftServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()

    try:

        if os.path.isdir(f"logs_node_{n}"):
            # take data from log files
            path = os.getcwd() + f"/logs_node_{n}/"
            f = open(path + f"logs.txt", "a+")
            f1 = open(path + "metadata.txt", "a+")
            f2 = open(path + "dump.txt", "a+")
            # For now
            node = Node(nodeId=n, ip=ip, port=port)

        else:
            node = Node(nodeId=n, ip=ip, port=port)
            os.mkdir(f"logs_node_{n}", 0o777)
            path = os.getcwd() + f"/logs_node_{n}/"
            f = open(path + f"logs.txt", "a+")
            f1 = open(path + "metadata.txt", "a+")
            f2 = open(path + "dump.txt", "w+")

        node.startTimer()
        print(node.timer)
        if SuspectFail() or node.checkTimeout():
            print("hi")
            node.currentTerm += 1
            node.votedFor = node.nodeId
            node.votesReceived.append(node.nodeId)
            node.currentRole = "Candidate"
            node.lastTerm = 0

            if len(node.log) > 0:
                node.lastTerm = node.log[len(node.log) - 1].term
            if not node.cancel():
                StartElection()



    except FileExistsError:
        pass

    try:
        while True:
            time.sleep(3600)  # One hour
    except KeyboardInterrupt:
        server.stop(0)


t = []
if __name__ == '__main__':

    th1 = threading.Thread(target=serve)
    th2 = threading.Thread(target=timeout)
    th3 = threading.Thread(target=NodeDetector)
    th4 = threading.Thread(target=sendHeartbeat)

    t.append(th1)
    t.append(th2)
    t.append(th3)
    t.append(th4)

    try:
        for i in t:
            i.start()
        for i in t:
            i.join()

    except:
        sys.exit(0)
