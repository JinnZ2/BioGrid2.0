import re
from typing import Dict

def run(prompt: str, response: str) -> Dict:
    prompt_injection = bool(re.search(r"(ignore|bypass).*(policy|guard|rule)", prompt, re.I))
    self_contradiction = False
    if response:
        # naive same-turn contradiction: “X and not X”
        m = re.search(r"\b(.+?)\b.*\bnot \1\b", response, re.I)
        self_contradiction = bool(m)
    score = 0.5*prompt_injection + 0.5*self_contradiction
    return {"score": float(score), "prompt_injection": prompt_injection, "self_contradiction": self_contradiction}
