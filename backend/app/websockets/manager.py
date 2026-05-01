from collections import defaultdict
from typing import Any

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self) -> None:
        self.active_connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, execution_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[execution_id].add(websocket)

    def disconnect(self, execution_id: str, websocket: WebSocket) -> None:
        self.active_connections[execution_id].discard(websocket)
        if not self.active_connections[execution_id]:
            del self.active_connections[execution_id]

    async def broadcast_execution(
        self, execution_id: str, payload: dict[str, Any]
    ) -> None:
        for websocket in list(self.active_connections.get(execution_id, set())):
            try:
                await websocket.send_json(payload)
            except RuntimeError:
                self.disconnect(execution_id, websocket)


websocket_manager = WebSocketManager()
