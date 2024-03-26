from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LeaseReq(_message.Message):
    __slots__ = ("ack",)
    ACK_FIELD_NUMBER: _ClassVar[int]
    ack: int
    def __init__(self, ack: _Optional[int] = ...) -> None: ...

class LeaseRes(_message.Message):
    __slots__ = ("ack",)
    ACK_FIELD_NUMBER: _ClassVar[int]
    ack: int
    def __init__(self, ack: _Optional[int] = ...) -> None: ...

class msg(_message.Message):
    __slots__ = ("msg",)
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: str
    def __init__(self, msg: _Optional[str] = ...) -> None: ...

class ack(_message.Message):
    __slots__ = ("ack",)
    ACK_FIELD_NUMBER: _ClassVar[int]
    ack: int
    def __init__(self, ack: _Optional[int] = ...) -> None: ...

class entry(_message.Message):
    __slots__ = ("index", "term", "key", "val")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    index: int
    term: int
    key: str
    val: str
    def __init__(self, index: _Optional[int] = ..., term: _Optional[int] = ..., key: _Optional[str] = ..., val: _Optional[str] = ...) -> None: ...

class AppendEntriesArgs(_message.Message):
    __slots__ = ("term", "leaderId", "prevLogIndex", "prevLogTerm", "suffix", "leaderCommit", "leaseInterval", "prefixLen", "heartBeat")
    TERM_FIELD_NUMBER: _ClassVar[int]
    LEADERID_FIELD_NUMBER: _ClassVar[int]
    PREVLOGINDEX_FIELD_NUMBER: _ClassVar[int]
    PREVLOGTERM_FIELD_NUMBER: _ClassVar[int]
    SUFFIX_FIELD_NUMBER: _ClassVar[int]
    LEADERCOMMIT_FIELD_NUMBER: _ClassVar[int]
    LEASEINTERVAL_FIELD_NUMBER: _ClassVar[int]
    PREFIXLEN_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    term: int
    leaderId: int
    prevLogIndex: int
    prevLogTerm: int
    suffix: _containers.RepeatedCompositeFieldContainer[entry]
    leaderCommit: int
    leaseInterval: float
    prefixLen: int
    heartBeat: bool
    def __init__(self, term: _Optional[int] = ..., leaderId: _Optional[int] = ..., prevLogIndex: _Optional[int] = ..., prevLogTerm: _Optional[int] = ..., suffix: _Optional[_Iterable[_Union[entry, _Mapping]]] = ..., leaderCommit: _Optional[int] = ..., leaseInterval: _Optional[float] = ..., prefixLen: _Optional[int] = ..., heartBeat: bool = ...) -> None: ...

class AppendEntriesRes(_message.Message):
    __slots__ = ("term", "success")
    TERM_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    term: int
    success: bool
    def __init__(self, term: _Optional[int] = ..., success: bool = ...) -> None: ...

class RequestVotesArgs(_message.Message):
    __slots__ = ("term", "candidateId", "lastLogIndex", "lastLogTerm")
    TERM_FIELD_NUMBER: _ClassVar[int]
    CANDIDATEID_FIELD_NUMBER: _ClassVar[int]
    LASTLOGINDEX_FIELD_NUMBER: _ClassVar[int]
    LASTLOGTERM_FIELD_NUMBER: _ClassVar[int]
    term: int
    candidateId: int
    lastLogIndex: int
    lastLogTerm: int
    def __init__(self, term: _Optional[int] = ..., candidateId: _Optional[int] = ..., lastLogIndex: _Optional[int] = ..., lastLogTerm: _Optional[int] = ...) -> None: ...

class RequestVotesRes(_message.Message):
    __slots__ = ("term", "voteGranted", "longestDurationRem", "NodeId")
    TERM_FIELD_NUMBER: _ClassVar[int]
    VOTEGRANTED_FIELD_NUMBER: _ClassVar[int]
    LONGESTDURATIONREM_FIELD_NUMBER: _ClassVar[int]
    NODEID_FIELD_NUMBER: _ClassVar[int]
    term: int
    voteGranted: bool
    longestDurationRem: float
    NodeId: int
    def __init__(self, term: _Optional[int] = ..., voteGranted: bool = ..., longestDurationRem: _Optional[float] = ..., NodeId: _Optional[int] = ...) -> None: ...

class ServeClientArgs(_message.Message):
    __slots__ = ("Request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    Request: str
    def __init__(self, Request: _Optional[str] = ...) -> None: ...

class ServeClientReply(_message.Message):
    __slots__ = ("Data", "LeaderID", "Success")
    DATA_FIELD_NUMBER: _ClassVar[int]
    LEADERID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    Data: str
    LeaderID: str
    Success: bool
    def __init__(self, Data: _Optional[str] = ..., LeaderID: _Optional[str] = ..., Success: bool = ...) -> None: ...

class ReplicateLogRequestArgs(_message.Message):
    __slots__ = ("leaderId", "currentTerm", "prefixLen", "prefixTerm", "commitLength", "suffix", "heartBeat")
    LEADERID_FIELD_NUMBER: _ClassVar[int]
    CURRENTTERM_FIELD_NUMBER: _ClassVar[int]
    PREFIXLEN_FIELD_NUMBER: _ClassVar[int]
    PREFIXTERM_FIELD_NUMBER: _ClassVar[int]
    COMMITLENGTH_FIELD_NUMBER: _ClassVar[int]
    SUFFIX_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    leaderId: int
    currentTerm: int
    prefixLen: int
    prefixTerm: int
    commitLength: int
    suffix: _containers.RepeatedCompositeFieldContainer[entry]
    heartBeat: bool
    def __init__(self, leaderId: _Optional[int] = ..., currentTerm: _Optional[int] = ..., prefixLen: _Optional[int] = ..., prefixTerm: _Optional[int] = ..., commitLength: _Optional[int] = ..., suffix: _Optional[_Iterable[_Union[entry, _Mapping]]] = ..., heartBeat: bool = ...) -> None: ...

class ReplicateLogRequestRes(_message.Message):
    __slots__ = ("nodeId", "currentTerm", "ackLen", "receivedMessage")
    NODEID_FIELD_NUMBER: _ClassVar[int]
    CURRENTTERM_FIELD_NUMBER: _ClassVar[int]
    ACKLEN_FIELD_NUMBER: _ClassVar[int]
    RECEIVEDMESSAGE_FIELD_NUMBER: _ClassVar[int]
    nodeId: int
    currentTerm: int
    ackLen: int
    receivedMessage: bool
    def __init__(self, nodeId: _Optional[int] = ..., currentTerm: _Optional[int] = ..., ackLen: _Optional[int] = ..., receivedMessage: bool = ...) -> None: ...

class ReplicateLogResponseArgs(_message.Message):
    __slots__ = ("followerId", "followerTerm", "ack", "success")
    FOLLOWERID_FIELD_NUMBER: _ClassVar[int]
    FOLLOWERTERM_FIELD_NUMBER: _ClassVar[int]
    ACK_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    followerId: int
    followerTerm: int
    ack: int
    success: bool
    def __init__(self, followerId: _Optional[int] = ..., followerTerm: _Optional[int] = ..., ack: _Optional[int] = ..., success: bool = ...) -> None: ...

class ReplicateLogResponseRes(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CommitArgs(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CommitRes(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
