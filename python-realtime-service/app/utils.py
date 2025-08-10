import time
from typing import Any, Dict

import jwt


def decode_jwt(token: str, secret: str) -> Dict[str, Any]:
    """Decode a JWT token with the given secret."""
    return jwt.decode(token, secret, algorithms=["HS256"])


def now() -> float:
    """Return the current Unix timestamp."""
    return time.time()
