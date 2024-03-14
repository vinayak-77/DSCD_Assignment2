import logEntry

NodeList = {}



class Node:
  isLeader = False
  nodeId = -1
  ipAddr = ""
  port = ""
  currentTerm = 0
  votedFor = None
  log = []
  commitLength = 0
  currentRole = "Follower"
  currentLeader = None
  votesReceived = []
  sentLength = 0
  ackedLength = 0
  lastTerm = 0
  leaderId = -1
  
  def __init__(self,nodeId,ip,port):
    self.nodeId = nodeId
    self.ipAddr = ip
    self.port = port
    
  def onCrashRecovery(self):
    self.currentRole = "Follower"
    self.currentLeader = None
    self.votesReceived = []
    self.sentLength = []
    self.ackedLength = []
    
  def onElectionTimeout(self):
    self.currentTerm+=1
    self.currentRole = "Candidate"
    self.votedFor = self.nodeId
    self.votesReceived = [self.nodeId]

    if(len(self.log) > 0):
      self.lastTerm = self.log[len(self.log)-1].term