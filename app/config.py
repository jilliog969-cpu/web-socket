import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # URL backend thật mà các file JS đang nói chuyện:
    # ví dụ: AUTH_BASE_URL=https://api.example.com
    AUTH_BASE_URL: str = Field(..., description="Base URL cho auth backend (có /login)")
    REALTIME_WS_URL: str = Field(..., description="WS URL của hệ thống realtime, ví dụ wss://rt.example.com/ws")

    # Tên header mang token khi đi backend (nếu cần)
    UPSTREAM_AUTH_HEADER: str = Field("Authorization", description="Header auth gửi lên backend realtime")

    # Secret cục bộ để ký/verify session (nếu bạn muốn tự quản)
    LOCAL_SESSION_SECRET: str = Field("dev-local-secret", description="Local secret cho HMAC/JWT nhẹ")

    # File lưu session (simple JSON). Có thể thay bằng Redis/DB sau
    SESSION_STORE_PATH: str = Field("./sessions.json")

    # Thời hạn session cục bộ (nếu backend không cung cấp refresh logic)
    SESSION_TTL_SECONDS: int = Field(86400)

    class Config:
        env_file = ".env"

settings = Settings()
