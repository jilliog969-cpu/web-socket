from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str


class CheckLoginRequest(BaseModel):
    token: str


class CheckLoginResponse(BaseModel):
    valid: bool
