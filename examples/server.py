import uuid
import logging
from typing import List
from pydantic import BaseModel
from starlette.applications import Starlette
from starlette.websockets import WebSocketDisconnect, WebSocket
from starlette.routing import WebSocketRoute


class ConnectionManager:

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    def disconnect(self, websocket: WebSocket):
        pass


manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


def startup():
    print("websocket server ready")


routes = [
    WebSocketRoute('/ws', websocket_endpoint)
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])
