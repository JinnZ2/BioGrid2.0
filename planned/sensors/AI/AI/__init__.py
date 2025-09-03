import json, time
from .provenance_stamp import stamp
from .consistency_guard import run as run_consistency
from .prompt_pressure_meter import run as run_pressure
from .adversarial_pattern_detector import run as run_adversarial
from .gaslight_index import compute as gaslight
from typing import List, Dict

def analyze(prompt: str, response: str, claims: List[Dict], model: str, glyph_ctx: str="") -> Dict:
    prov = stamp(model, prompt, glyph_ctx)
    c = run_consistency(claims); p = run_pressure(prompt); a = run_adversarial(prompt, response)
    gi = gaslight(c["score"], p["score"], a["score"])
    return {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sensor": "AI.logic_shield",
        "subject": "conversation_turn",
        "score": 1.0 - gi,
        "labels": ["consistency", "pressure", "adversarial", "gaslight_index"],
        "details": {"consistency": c, "pressure": p, "adversarial": a, "gaslight_index": gi},
        "provenance": prov
    }
