import aiohttp
from fastapi import APIRouter, HTTPException
from .schemas import LoginIn, LoginOut, CheckLoginOut
from .config import settings
from .storage import store
from .utils import is_session_valid

router = APIRouter()

@router.post("/login", response_model=LoginOut)
async def login(payload: LoginIn):
    """
    Forward tới AUTH_BASE_URL/login. Giả định backend trả JSON { token, user? }.
    Nếu backend khác format, bạn map lại ở đây.
    """
    url = f"{settings.AUTH_BASE_URL.rstrip('/')}/login"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json={"username": payload.username, "password": payload.password}) as resp:
                text = await resp.text()
                if resp.status >= 400:
                    raise HTTPException(status_code=resp.status, detail=f"Upstream error: {text}")
                data = await resp.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Cannot reach auth backend: {e}")

    token = data.get("token")
    if not token:
        raise HTTPException(status_code=502, detail="Auth backend response missing token")
    user  = data.get("user", {"username": payload.username})

    # Lưu phiên đơn giản (single-user). Nếu multi-user => dùng cookie/sessionid
    store.set_session(user_id=str(user.get("id", user.get("username", "me"))), token=token, user=user)
    return LoginOut(ok=True, token=token, user=user)

@router.get("/check_login", response_model=CheckLoginOut)
async def check_login():
    sess = store.get_any_session()
    return CheckLoginOut(
        logged_in=is_session_valid(sess),
        user=(sess or {}).get("user"),
        token_expires_at=(sess or {}).get("expires_at"),
    )
