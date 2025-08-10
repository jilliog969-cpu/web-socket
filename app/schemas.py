from pydantic import BaseModel
from typing import Optional, Any, Dict


class LoginIn(BaseModel):
    username: str
    password: str


class LoginOut(BaseModel):
    ok: bool
    token: str
    user: Optional[Dict[str, Any]] = None


class CheckLoginOut(BaseModel):
    logged_in: bool
    user: Optional[Dict[str, Any]] = None
    token_expires_at: Optional[int] = None  # epoch seconds


class ErrorOut(BaseModel):
    ok: bool = False
    error: str
