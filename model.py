from enum import Enum


class ResponseType(Enum):
    OK = "OK"
    ERROR = "ERROR"
    WARNING = "WARNING"
    IGNORE = "IGNORE"


class Response:
    def __init__(self, type, msg) -> None:
        self.type: ResponseType = type
        self.msg: str = msg
        pass
