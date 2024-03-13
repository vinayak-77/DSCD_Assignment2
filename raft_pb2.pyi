from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class entry(_message.Message):
    __slots__ = ("index", "key", "val")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    index: int
    key: int
    val: int
    def __init__(self, index: _Optional[int] = ..., key: _Optional[int] = ..., val: _Optional[int] = ...) -> None: ...

class AppendEntriesArgs(_message.Message):
    __slots__ = ("term", "leaderId", "prevLogIndex", "prevLogTerm", "entries", "leaderCommit", "leaseInterval")
    TERM_FIELD_NUMBER: _ClassVar[int]
    LEADERID_FIELD_NUMBER: _ClassVar[int]
    PREVLOGINDEX_FIELD_NUMBER: _ClassVar[int]
    PREVLOGTERM_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    LEADERCOMMIT_FIELD_NUMBER: _ClassVar[int]
    LEASEINTERVAL_FIELD_NUMBER: _ClassVar[int]
    term: int
    leaderId: int
    prevLogIndex: int
    prevLogTerm: int
    entries: _containers.RepeatedCompositeFieldContainer[entry]
    leaderCommit: int
    leaseInterval: int
    def __init__(self, term: _Optional[int] = ..., leaderId: _Optional[int] = ..., prevLogIndex: _Optional[int] = ..., prevLogTerm: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[entry, _Mapping]]] = ..., leaderCommit: _Optional[int] = ..., leaseInterval: _Optional[int] = ...) -> None: ...

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
    longestDurationRem: int
    NodeId: int
    def __init__(self, term: _Optional[int] = ..., voteGranted: bool = ..., longestDurationRem: _Optional[int] = ..., NodeId: _Optional[int] = ...) -> None: ...

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
