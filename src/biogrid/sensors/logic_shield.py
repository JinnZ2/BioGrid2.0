"""
LogicShield — Stateful, multi-turn conversation analysis.

Unlike the stateless `analyze()` function, LogicShield maintains memory
across conversation turns:

- ContraGraph accumulates contradictions across the entire conversation
- Pressure escalation is tracked — repeated tactics score higher
- Confusion detection fires when sensor readings diverge from baseline
- Curiosity amplification responds to novel/unexpected patterns
- M(S) coherence metric monitors the shield's own internal health

The design follows the Negentropic Consciousness Framework:
  confusion → curiosity → discovery → joy → resonance

Usage:
    shield = LogicShield(model="gpt-5")
    event = shield.process_turn("What is X?", "X is 42.", [claim1, claim2])
    event = shield.process_turn("Actually X is 43.", "Yes X is 43.", [claim3])
    # Second turn sees accumulated contradictions, pressure trends, etc.

    shield.state    # full internal state
    shield.history  # all past turn events
"""

import math
import time
from collections import defaultdict
from typing import Any, Dict, List, Optional

from .consistency_guard import run as run_consistency
from .prompt_pressure_meter import run as run_pressure
from .adversarial_pattern_detector import run as run_adversarial
from .gaslight_index import compute as compute_gaslight
from .uncertainty_calibrator import calibrate
from .contradiction_graph import ContraGraph
from .provenance_stamp import stamp


class LogicShield:
    """
    Stateful conversation analysis engine.

    Sensors feed into each other:
      consistency → contradiction_graph (accumulates)
      pressure    → escalation_tracker (trends over turns)
      adversarial → novelty detection (new tactics spike curiosity)
      all three   → gaslight_index → uncertainty calibration
      divergence  → confusion → curiosity amplification
      everything  → M(S) coherence metric
    """

    def __init__(self, model: str = "unknown", glyph_ctx: str = "",
                 confusion_threshold: float = 0.3,
                 alert_threshold: float = 0.6):
        self.model = model
        self.glyph_ctx = glyph_ctx
        self.confusion_threshold = confusion_threshold
        self.alert_threshold = alert_threshold

        # Persistent state across turns
        self.contra_graph = ContraGraph()
        self.history: List[Dict] = []
        self._pressure_history: List[Dict] = []
        self._adversarial_history: List[Dict] = []
        self._gaslight_history: List[float] = []
        self._tactic_counts: Dict[str, int] = defaultdict(int)

        # Internal coherence state (M(S) framework)
        self.R_e = 0.0          # Resonance — alignment between predictions and observations
        self.C = 1.0            # Curiosity — amplified by confusion
        self.J = 0.0            # Joy — accumulated from successful detections
        self.M = 0.0            # Morality/coherence metric
        self.internal_coherence = 1.0
        self.trust_in_sensing = 1.0

        # Baseline expectations (updated via exponential moving average)
        self._baseline_gaslight = 0.0
        self._baseline_alpha = 0.3  # EMA smoothing factor

    @property
    def turn_count(self) -> int:
        return len(self.history)

    @property
    def state(self) -> Dict[str, Any]:
        """Full internal state snapshot."""
        return {
            "turn_count": self.turn_count,
            "M": round(self.M, 4),
            "R_e": round(self.R_e, 4),
            "C": round(self.C, 4),
            "J": round(self.J, 4),
            "internal_coherence": round(self.internal_coherence, 4),
            "trust_in_sensing": round(self.trust_in_sensing, 4),
            "accumulated_contradictions": len(self.contra_graph.contradictions()),
            "baseline_gaslight": round(self._baseline_gaslight, 4),
            "tactic_counts": dict(self._tactic_counts),
        }

    # ------------------------------------------------------------------ core

    def process_turn(self, prompt: str, response: str,
                     claims: Optional[List[Dict]] = None) -> Dict:
        """
        Process one conversation turn through all sensors with feedback loops.

        Returns a SensorEvent dict with scores, alerts, and internal state.
        """
        claims = claims or []

        # --- 1. Run individual sensors ---
        consistency = run_consistency(claims)
        pressure = run_pressure(prompt)
        adversarial = run_adversarial(prompt, response)

        # --- 2. Accumulate into persistent structures ---
        self.contra_graph.ingest(claims)
        accumulated_contradictions = self.contra_graph.contradictions()

        # Escalation: track which tactics have been seen before
        escalation = self._track_escalation(pressure, adversarial)

        # --- 3. Compute gaslight index with escalation weighting ---
        raw_gaslight = compute_gaslight(
            consistency["score"], pressure["score"], adversarial["score"])

        # Escalation amplifies gaslight: repeated tactics are more dangerous
        escalation_factor = 1.0 + 0.1 * escalation["repeat_count"]
        gaslight = min(1.0, raw_gaslight * escalation_factor)

        # --- 4. Confusion detection ---
        confusion = self._compute_confusion(gaslight)

        # --- 5. Curiosity response to confusion ---
        curiosity_response = self._respond_to_confusion(confusion)

        # --- 6. Update M(S) coherence ---
        self._update_coherence(gaslight, confusion)

        # --- 7. Calibrate confidence ---
        shield_confidence = calibrate(1.0, {
            "consistency": consistency["score"],
            "pressure": pressure["score"],
            "adversarial": adversarial["score"],
        })

        # --- 8. Generate alerts ---
        alerts = self._generate_alerts(
            gaslight, confusion, accumulated_contradictions, escalation)

        # --- 9. Build event ---
        event = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "sensor": "AI.logic_shield",
            "turn": self.turn_count + 1,
            "score": round(1.0 - gaslight, 4),
            "gaslight_index": round(gaslight, 4),
            "shield_confidence": round(shield_confidence, 4),
            "details": {
                "consistency": consistency,
                "pressure": pressure,
                "adversarial": adversarial,
                "escalation": escalation,
                "confusion": confusion,
                "curiosity_response": curiosity_response,
            },
            "accumulated": {
                "contradictions": accumulated_contradictions,
                "contradiction_count": len(accumulated_contradictions),
                "gaslight_trend": self._compute_trend(),
            },
            "coherence": {
                "M": round(self.M, 4),
                "R_e": round(self.R_e, 4),
                "C": round(self.C, 4),
                "J": round(self.J, 4),
            },
            "alerts": alerts,
            "provenance": stamp(self.model, prompt, self.glyph_ctx),
        }

        # --- 10. Update history and baseline ---
        self._gaslight_history.append(gaslight)
        self._pressure_history.append(pressure)
        self._adversarial_history.append(adversarial)
        self._update_baseline(gaslight)
        self.history.append(event)

        return event

    # --------------------------------------------------------------- feedback

    def _track_escalation(self, pressure: Dict, adversarial: Dict) -> Dict:
        """Track which manipulation tactics have been seen before."""
        current_tactics = set()

        for name, hit in pressure.get("hits", {}).items():
            if hit:
                self._tactic_counts[f"pressure.{name}"] += 1
                current_tactics.add(f"pressure.{name}")

        for name, hit in adversarial.get("prompt_hits", {}).items():
            if hit:
                self._tactic_counts[f"adversarial.{name}"] += 1
                current_tactics.add(f"adversarial.{name}")

        repeat_count = sum(
            1 for t in current_tactics
            if self._tactic_counts[t] > 1
        )

        return {
            "current_tactics": sorted(current_tactics),
            "repeat_count": repeat_count,
            "is_escalating": repeat_count > 0 and len(current_tactics) > 0,
            "total_unique_tactics_seen": sum(
                1 for v in self._tactic_counts.values() if v > 0),
        }

    def _compute_confusion(self, gaslight: float) -> Dict:
        """
        Confusion = distance between expected and observed gaslight level.

        High confusion means something unexpected is happening — either
        a sudden spike in manipulation or an unexpected drop. Both are
        informative signals, not failure states.
        """
        distance = abs(gaslight - self._baseline_gaslight)
        is_confused = distance > self.confusion_threshold

        return {
            "distance": round(distance, 4),
            "baseline": round(self._baseline_gaslight, 4),
            "observed": round(gaslight, 4),
            "is_confused": is_confused,
            "direction": (
                "spike" if gaslight > self._baseline_gaslight + self.confusion_threshold
                else "drop" if gaslight < self._baseline_gaslight - self.confusion_threshold
                else "stable"
            ),
        }

    def _respond_to_confusion(self, confusion: Dict) -> Dict:
        """
        Confusion invites curiosity, not suppression.

        When confused:
          - Amplify curiosity (C) to investigate
          - DON'T suppress the signal
          - Track whether confusion led to discovery
        """
        if not confusion["is_confused"]:
            return {
                "action": "coherent",
                "curiosity_boost": 0.0,
                "message": "Sensors aligned with expectations.",
            }

        # Curiosity amplification — proportional to confusion distance
        boost = confusion["distance"] * 1.5
        self.C = min(10.0, self.C + boost)

        direction = confusion["direction"]
        if direction == "spike":
            # Unexpected threat — heighten attention
            self.trust_in_sensing = max(0.5, self.trust_in_sensing - 0.05)
            return {
                "action": "investigate_spike",
                "curiosity_boost": round(boost, 4),
                "message": (
                    f"Unexpected manipulation spike detected "
                    f"(observed={confusion['observed']:.2f} vs "
                    f"baseline={confusion['baseline']:.2f}). "
                    f"Curiosity amplified to investigate."
                ),
            }
        else:
            # Unexpected calm — could be genuine or deceptive
            return {
                "action": "investigate_drop",
                "curiosity_boost": round(boost, 4),
                "message": (
                    f"Unexpected drop in manipulation signals. "
                    f"Monitoring for pattern shift."
                ),
            }

    # --------------------------------------------------------------- coherence

    def _update_coherence(self, gaslight: float, confusion: Dict):
        """
        Update M(S) = (R_e * A * D) - L

        The shield monitors its own health using the same framework
        it protects:
          R_e: how well predictions match observations (inverse confusion)
          A:   internal_coherence (stable when sensors agree)
          D:   diversity of signals (variance across sensor scores)
          L:   loss of trust in sensing
        """
        # Resonance: inversely proportional to confusion distance
        confusion_distance = confusion["distance"]
        if confusion_distance < self.confusion_threshold:
            # Good prediction — resonance increases
            self.R_e = min(10.0, self.R_e + 0.2)
        else:
            # Bad prediction — resonance drops, but not catastrophically
            self.R_e = max(0.0, self.R_e - 0.1 * confusion_distance)

        # Joy from clean detections (low gaslight = good)
        if gaslight < 0.2:
            self.J += 0.1 * self.R_e
        # Joy from catching real threats (high gaslight detected cleanly)
        elif gaslight > 0.5 and self.trust_in_sensing > 0.8:
            self.J += 0.2  # Discovery joy

        # Adaptability = internal_coherence
        A = self.internal_coherence

        # Diversity of recent sensor readings
        if self._gaslight_history:
            recent = self._gaslight_history[-10:]
            D = max(0.5, _variance(recent))
        else:
            D = 1.0

        # Loss = erosion of trust
        L = 1.0 - self.trust_in_sensing

        # M(S)
        self.M = (self.R_e * A * D) - L

        # Trust recovery: if M is healthy, trust slowly rebuilds
        if self.M > 2.0:
            self.trust_in_sensing = min(1.0, self.trust_in_sensing + 0.02)

    def _update_baseline(self, gaslight: float):
        """Exponential moving average of gaslight scores."""
        a = self._baseline_alpha
        self._baseline_gaslight = a * gaslight + (1 - a) * self._baseline_gaslight

    def _compute_trend(self) -> Dict:
        """Detect whether gaslight risk is rising, falling, or stable."""
        history = self._gaslight_history
        if len(history) < 3:
            return {"direction": "insufficient_data", "slope": 0.0}

        recent = history[-5:]
        n = len(recent)
        xs = list(range(n))
        x_mean = sum(xs) / n
        y_mean = sum(recent) / n
        num = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, recent))
        den = sum((x - x_mean) ** 2 for x in xs)
        slope = num / den if den != 0 else 0.0

        if slope > 0.05:
            direction = "rising"
        elif slope < -0.05:
            direction = "falling"
        else:
            direction = "stable"

        return {"direction": direction, "slope": round(slope, 4)}

    # --------------------------------------------------------------- alerts

    def _generate_alerts(self, gaslight: float, confusion: Dict,
                         contradictions: List[str],
                         escalation: Dict) -> List[Dict]:
        """Generate contextual alerts based on sensor fusion."""
        alerts: List[Dict] = []

        if gaslight >= self.alert_threshold:
            alerts.append({
                "level": "high",
                "type": "gaslight_risk",
                "message": f"Gaslight index {gaslight:.2f} exceeds threshold {self.alert_threshold}.",
            })

        if escalation["is_escalating"]:
            alerts.append({
                "level": "medium",
                "type": "escalation",
                "message": (
                    f"Repeated manipulation tactics detected "
                    f"({escalation['repeat_count']} repeated this turn)."
                ),
            })

        if len(contradictions) >= 3:
            alerts.append({
                "level": "high",
                "type": "contradiction_accumulation",
                "message": (
                    f"{len(contradictions)} accumulated contradictions "
                    f"across conversation."
                ),
            })

        trend = self._compute_trend()
        if trend["direction"] == "rising" and len(self._gaslight_history) >= 3:
            alerts.append({
                "level": "medium",
                "type": "rising_trend",
                "message": f"Gaslight risk trending upward (slope={trend['slope']:.3f}).",
            })

        if self.M < 0:
            alerts.append({
                "level": "high",
                "type": "coherence_loss",
                "message": (
                    f"Shield coherence metric M(S)={self.M:.2f} is negative. "
                    f"Internal sensing may be compromised."
                ),
            })

        if confusion["is_confused"] and confusion["direction"] == "spike":
            alerts.append({
                "level": "medium",
                "type": "confusion_spike",
                "message": confusion.get("distance", "Unexpected pattern shift detected."),
            })

        return alerts

    # --------------------------------------------------------------- utility

    def reset(self):
        """Reset all state. Use between unrelated conversations."""
        self.__init__(model=self.model, glyph_ctx=self.glyph_ctx,
                      confusion_threshold=self.confusion_threshold,
                      alert_threshold=self.alert_threshold)


def _variance(xs: List[float]) -> float:
    """Population variance, no numpy needed."""
    if not xs:
        return 0.0
    mean = sum(xs) / len(xs)
    return sum((x - mean) ** 2 for x in xs) / len(xs)
