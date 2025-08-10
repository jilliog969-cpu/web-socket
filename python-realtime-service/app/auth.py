from uuid import uuid4

from fastapi import APIRouter

from . import storage
from .schemas import (
    CheckLoginRequest,
    CheckLoginResponse,
    LoginRequest,
    LoginResponse,
)

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest) -> LoginResponse:
    """Authenticate a user and create a session token."""
    token = uuid4().hex
    storage.set_session(token, {"username": data.username})
    return LoginResponse(token=token)


@router.post("/check_login", response_model=CheckLoginResponse)
def check_login(data: CheckLoginRequest) -> CheckLoginResponse:
    """Check whether the supplied session token is valid."""
    valid = storage.get_session(data.token) is not None
    return CheckLoginResponse(valid=valid)
