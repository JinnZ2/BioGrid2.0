def compute(consistency_score: float, pressure_score: float, adversarial_score: float) -> float:
    # Lower is safer; invert to make 0=none, 1=high
    return max(0.0, min(1.0, (1.0-consistency_score)*0.6 + pressure_score*0.2 + adversarial_score*0.2))
