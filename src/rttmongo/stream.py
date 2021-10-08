import asyncio
from enum import Enum
from typing import Union, Callable, Dict, Any
from functools import wraps
from pydantic import BaseModel
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.collection import CollectionChangeStream
from starlette.websockets import WebSocketDisconnect, WebSocket


class ObjectIdDataType(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')
        return str(v)


class OperationType(str, Enum):
    insert = "insert"
    update = "update"
    delete = "delete"


class RegisterStream(BaseModel):
    label: Union[str, None]
    database: str
    collection: str
    operation_type: str


class Change(BaseModel):
    operationType: OperationType
    fullDocument: Dict[str, Union[ObjectIdDataType, Any]]


class ConnectionManager:
    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    def disconnect(self, websocket: WebSocket):
        pass


manager = ConnectionManager()


async def connect(websocket: WebSocket, s: Callable):
    await manager.connect(websocket)
    try:
        await s()

    except WebSocketDisconnect:
        manager.disconnect(websocket)


def listen(register: RegisterStream, client: MongoClient):
    cursor = client[register.database][register.collection].watch(
        pipeline=[{"$match": {"operationType": register.operation_type}}], **{})

    def decorate(fn):
        @wraps(fn)
        async def wrapper(websocket: WebSocket):
            await connect(websocket, lambda: stream(cursor, websocket, fn))

        return wrapper

    return decorate


async def stream(cursor: CollectionChangeStream, w: WebSocket, l: listen, timeout=1):
    with cursor:
        while cursor.alive:
            change = cursor.try_next()
            if change is not None:
                doc = Change(fullDocument=change['fullDocument'], operationType=change['operationType'])
                await l(doc, w)
            await asyncio.sleep(timeout)
