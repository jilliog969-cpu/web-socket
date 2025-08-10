import json, time, threading
from typing import Optional, Dict, Any
from pathlib import Path
from .config import settings

_lock = threading.Lock()

class SessionStore:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"sessions": {}})

    def _read(self) -> Dict[str, Any]:
        with _lock:
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                return {"sessions": {}}

    def _write(self, data: Dict[str, Any]) -> None:
        with _lock:
            self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def set_session(self, user_id: str, token: str, user: Dict[str, Any]) -> None:
        data = self._read()
        now = int(time.time())
        data["sessions"][user_id] = {
            "token": token,
            "user": user,
            "created_at": now,
            "expires_at": now + settings.SESSION_TTL_SECONDS
        }
        self._write(data)

    def get_any_session(self) -> Optional[Dict[str, Any]]:
        """Tuỳ yêu cầu: hiện tại dùng 1 session hoạt động gần nhất (single-user service)
        Nếu đa người dùng, bạn hãy dùng cookie/session ID hoặc header để phân biệt."""
        data = self._read().get("sessions", {})
        if not data: return None
        # lấy session mới nhất
        last = max(data.values(), key=lambda s: s.get("created_at", 0))
        return last

    def clear_all(self) -> None:
        self._write({"sessions": {}})

store = SessionStore(settings.SESSION_STORE_PATH)
