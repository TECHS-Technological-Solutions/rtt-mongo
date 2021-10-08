import uuid
import logging
from typing import List, Callable
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import CollectionChangeStream
from starlette.applications import Starlette
from starlette.websockets import WebSocketDisconnect, WebSocket
from starlette.routing import WebSocketRoute
from rttmongo import stream

client = MongoClient(
    host='localhost',
    port=27017,
    username='rtt-mongo',
    password='1234abcd!'
)



@stream.listen(stream.RegisterStream(label=None,
                                     database='rtt-mongo',
                                     collection='users',
                                     operation_type='insert'), client)
async def websocket_endpoint(change: stream.Change, websocket: WebSocket):
    print('received: ', change)
    await websocket.send_json(change.dict())


def startup():
    print("websocket server ready")


routes = [
    WebSocketRoute('/users', websocket_endpoint)
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])
