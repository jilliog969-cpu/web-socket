import asyncio
import json
import websockets
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from .config import settings
from .storage import store
from .utils import is_session_valid

router = APIRouter()

@router.websocket("/socket")
async def socket_bridge(client_ws: WebSocket):
    """
    Bridge WebSocket:
    - Client connect tới /socket
    - Service sẽ mở kết nối tới REALTIME_WS_URL (upstream) và forward 2 chiều.
    - Gắn Authorization: Bearer <token> nếu upstream cần.
    """
    await client_ws.accept()

    sess = store.get_any_session()
    if not is_session_valid(sess):
        await client_ws.send_json({"type": "error", "message": "Not logged in"})
        await client_ws.close()
        return

    token = sess["token"]
    headers = [(settings.UPSTREAM_AUTH_HEADER, f"Bearer {token}")]

    try:
        async with websockets.connect(settings.REALTIME_WS_URL, extra_headers=headers) as upstream:
            # forward 2 chiều
            async def c2u():
                while True:
                    msg = await client_ws.receive_text()
                    # tuỳ yêu cầu: có thể chuẩn hoá/gắn metadata
                    await upstream.send(msg)

            async def u2c():
                while True:
                    msg = await upstream.recv()
                    # có thể parse/transform trước khi gửi cho client
                    # ví dụ: wrap lại dạng JSON service:
                    try:
                        parsed = json.loads(msg)
                    except Exception:
                        parsed = {"type":"raw", "payload": msg}
                    await client_ws.send_json({"type":"upstream", "data": parsed})

            await asyncio.gather(c2u(), u2c())

    except WebSocketDisconnect:
        # client đóng
        return
    except Exception as e:
        try:
            await client_ws.send_json({"type": "error", "message": f"Bridge failed: {e}"})
        finally:
            await client_ws.close()
