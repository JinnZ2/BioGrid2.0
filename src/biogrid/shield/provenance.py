"""SHA256 provenance stamps for audit trails."""

import hashlib
import time
from typing import Dict, Optional


def _sha256(s: bytes) -> str:
    return hashlib.sha256(s).hexdigest()


def stamp(model: str, prompt: str, context: Optional[str] = None,
          cap_bytes: int = 65536) -> Dict:
    """Create a provenance stamp for a conversation turn."""
    ctx_bytes = context.encode("utf-8", "ignore")[:cap_bytes] if context else b""
    return {
        "model": model,
        "prompt_sha256": _sha256(prompt.encode("utf-8")),
        "context_sha256": _sha256(ctx_bytes) if ctx_bytes else "",
        "context_bytes": len(ctx_bytes),
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
