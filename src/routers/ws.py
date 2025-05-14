from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException
from typing import Set

router = APIRouter()

class ConnectionManager:
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        print("server: client connected")
        await websocket.accept()
        self.active_connections.add(websocket)
        try:
            while True:
                # Keep connection alive
                await websocket.receive_text()
        except WebSocketDisconnect:
            print(f"Connection disconnected")
        except WebSocketException:
            print(f"Unexpected error: {WebSocketException}")
        finally:
            self.active_connections.remove(websocket)

    async def send(self, message: str):
        for conn in self.active_connections:
            await conn.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('connecting...')
    await manager.connect(websocket)

   

