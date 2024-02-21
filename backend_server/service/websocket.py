from fastapi import WebSocket

import backend_server.schemas.user_scent as user_scent_schema


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(
        self,
        message: user_scent_schema.WebSocketMessage,
        websocket: WebSocket,
    ):
        await websocket.send_text(message.model_dump_json())

    async def broadcast(
        self,
        message: user_scent_schema.WebSocketMessage,
    ):
        for connection in self.active_connections:
            try:
                await connection.send_text(message.model_dump_json())
            except RuntimeError:
                self.active_connections.remove(connection)


manager = ConnectionManager()


def get_ws_manager():
    return manager
