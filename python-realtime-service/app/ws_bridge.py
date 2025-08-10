import asyncio

import websockets
from fastapi import APIRouter, WebSocket

from .config import get_settings

router = APIRouter()


@router.websocket("/socket")
async def websocket_proxy(ws: WebSocket) -> None:
    """Proxy messages between the client WebSocket and backend server."""
    await ws.accept()
    settings = get_settings()

    async with websockets.connect(settings.backend_url) as backend:
        async def client_to_backend() -> None:
            while True:
                data = await ws.receive_text()
                await backend.send(data)

        async def backend_to_client() -> None:
            while True:
                data = await backend.recv()
                await ws.send_text(data)

        await asyncio.gather(client_to_backend(), backend_to_client())
