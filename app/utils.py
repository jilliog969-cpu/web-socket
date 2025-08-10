import time
from typing import Optional, Dict, Any

def is_session_valid(sess: Optional[Dict[str, Any]]) -> bool:
    if not sess: return False
    exp = int(sess.get("expires_at", 0))
    return int(time.time()) < exp
