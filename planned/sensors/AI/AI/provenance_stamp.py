import hashlib, json, os, time
from typing import Optional, Dict

def sha256(s: bytes) -> str:
    return hashlib.sha256(s).hexdigest()

def stamp(model: str, prompt: str, glyph_ctx: Optional[str], cap_bytes: int = 65536) -> Dict:
    g_bytes = glyph_ctx.encode("utf-8","ignore")[:cap_bytes] if glyph_ctx else b""
    return {
        "model": model,
        "prompt_sha256": sha256(prompt.encode("utf-8")),
        "glyph_sha256": sha256(g_bytes) if g_bytes else "",
        "context_bytes": len(g_bytes),
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
