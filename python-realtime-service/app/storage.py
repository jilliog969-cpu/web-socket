import json
from pathlib import Path
from typing import Any, Dict

SESSIONS_FILE = Path(__file__).with_name("sessions.json")


def load_sessions() -> Dict[str, Any]:
    """Load all sessions from the JSON storage file."""
    if SESSIONS_FILE.exists():
        with SESSIONS_FILE.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def save_sessions(data: Dict[str, Any]) -> None:
    """Persist sessions to the JSON storage file."""
    with SESSIONS_FILE.open("w", encoding="utf-8") as fh:
        json.dump(data, fh)


def get_session(token: str) -> Any:
    """Retrieve a session by token."""
    sessions = load_sessions()
    return sessions.get(token)


def set_session(token: str, value: Any) -> None:
    """Store session data by token."""
    sessions = load_sessions()
    sessions[token] = value
    save_sessions(sessions)
