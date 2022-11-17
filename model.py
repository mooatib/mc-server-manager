from enum import Enum
import asyncio


class ResponseType(Enum):
    OK = "OK"
    ERROR = "ERROR"
    WARNING = "WARNING"
    IGNORE = "IGNORE"


class Response:
    def __init__(self, type, msg, params=[]) -> None:
        self.type: ResponseType = type
        self.msg: str = msg
        self.params: list(str) = params
        pass


class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.create_task(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback
