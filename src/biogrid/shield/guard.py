"""
ConversationGuard — Stateful multi-turn conversation analysis.

Maintains state across conversation turns to detect manipulation patterns
that single-turn analysis misses:

- Contradictions accumulate across the full conversation
- Repeated manipulation tactics are flagged as escalation
- Anomaly detection fires when risk scores diverge from baseline
- System health metric monitors the guard's own reliability
- Trend analysis detects rising/falling risk over time

Usage:
    guard = ConversationGuard(model="gpt-5")
    event = guard.process_turn("prompt", "response", [claims])
    event = guard.process_turn("next prompt", "next response", [more_claims])

    guard.state     # internal health and counters
    guard.history   # all past turn events
    guard.reset()   # clear between unrelated conversations
"""

import time
from collections import defaultdict
from typing import Any, Dict, List, Optional

from .consistency import check as check_consistency
from .pressure import check as check_pressure
from .adversarial import check as check_adversarial
from .manipulation import compute as compute_manipulation
from .calibrator import calibrate
from .contradiction import ContradictionTracker
from .provenance import stamp


class ConversationGuard:
    """
    Stateful conversation analysis engine.

    Data flow:
        consistency ──→ contradiction_tracker (accumulates) ──┐
        pressure    ──→ escalation_tracker (trends)          ──┤──→ risk_index
        adversarial ──→ tactic_counts (repeats amplify)      ──┘       │
                                                                       ↓
        risk_index ──→ anomaly_detector (vs EMA baseline) ──→ system_health
    """

    def __init__(self, model: str = "unknown", context: str = "",
                 anomaly_threshold: float = 0.3,
                 alert_threshold: float = 0.6):
        self.model = model
        self.context = context
        self.anomaly_threshold = anomaly_threshold
        self.alert_threshold = alert_threshold

        # Persistent state
        self.contradictions = ContradictionTracker()
        self.history: List[Dict] = []
        self._risk_history: List[float] = []
        self._tactic_counts: Dict[str, int] = defaultdict(int)

        # System health (self-monitoring)
        self.prediction_accuracy = 0.0   # how well baseline predicts observations
        self.investigation_priority = 1.0  # raised when anomalies are detected
        self.detection_score = 0.0        # accumulated from successful detections
        self.system_health = 0.0          # composite health metric
        self.internal_consistency = 1.0   # stability of sensor agreement
        self.sensor_reliability = 1.0     # degrades under sustained anomalies

        # Baseline (exponential moving average)
        self._baseline_risk = 0.0
        self._baseline_alpha = 0.3

    @property
    def turn_count(self) -> int:
        return len(self.history)

    @property
    def state(self) -> Dict[str, Any]:
        """Snapshot of internal state."""
        return {
            "turn_count": self.turn_count,
            "system_health": round(self.system_health, 4),
            "prediction_accuracy": round(self.prediction_accuracy, 4),
            "investigation_priority": round(self.investigation_priority, 4),
            "detection_score": round(self.detection_score, 4),
            "sensor_reliability": round(self.sensor_reliability, 4),
            "internal_consistency": round(self.internal_consistency, 4),
            "accumulated_conflicts": self.contradictions.conflict_count(),
            "baseline_risk": round(self._baseline_risk, 4),
            "tactic_counts": dict(self._tactic_counts),
        }

    # ------------------------------------------------------------------ core

    def process_turn(self, prompt: str, response: str,
                     claims: Optional[List[Dict]] = None) -> Dict:
        """
        Analyze one conversation turn with full feedback loops.

        Returns an event dict with risk scores, alerts, and system state.
        """
        claims = claims or []

        # 1. Run detectors
        consistency = check_consistency(claims)
        pressure = check_pressure(prompt)
        adversarial = check_adversarial(prompt, response)

        # 2. Accumulate persistent state
        self.contradictions.ingest(claims)
        all_conflicts = self.contradictions.conflicts()
        escalation = self._track_escalation(pressure, adversarial)

        # 3. Compute risk index with escalation amplification
        raw_risk = compute_manipulation(
            consistency["score"], pressure["score"], adversarial["score"])
        escalation_factor = 1.0 + 0.1 * escalation["repeat_count"]
        risk_index = min(1.0, raw_risk * escalation_factor)

        # 4. Anomaly detection (divergence from baseline)
        anomaly = self._detect_anomaly(risk_index)

        # 5. Respond to anomaly
        anomaly_response = self._respond_to_anomaly(anomaly)

        # 6. Update system health
        self._update_health(risk_index, anomaly)

        # 7. Calibrate confidence
        confidence = calibrate(1.0, {
            "consistency": consistency["score"],
            "pressure": pressure["score"],
            "adversarial": adversarial["score"],
        })

        # 8. Generate alerts
        alerts = self._generate_alerts(
            risk_index, anomaly, all_conflicts, escalation)

        # 9. Build event
        event = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "turn": self.turn_count + 1,
            "risk_index": round(risk_index, 4),
            "confidence": round(confidence, 4),
            "details": {
                "consistency": consistency,
                "pressure": pressure,
                "adversarial": adversarial,
                "escalation": escalation,
                "anomaly": anomaly,
                "anomaly_response": anomaly_response,
            },
            "accumulated": {
                "conflicts": all_conflicts,
                "conflict_count": len(all_conflicts),
                "trend": self._compute_trend(),
            },
            "health": {
                "system_health": round(self.system_health, 4),
                "prediction_accuracy": round(self.prediction_accuracy, 4),
                "sensor_reliability": round(self.sensor_reliability, 4),
            },
            "alerts": alerts,
            "provenance": stamp(self.model, prompt, self.context),
        }

        # 10. Update history and baseline
        self._risk_history.append(risk_index)
        self._update_baseline(risk_index)
        self.history.append(event)

        return event

    # ----------------------------------------------------------- escalation

    def _track_escalation(self, pressure: Dict, adversarial: Dict) -> Dict:
        """Track repeated manipulation tactics across turns."""
        current = set()

        for name, hit in pressure.get("hits", {}).items():
            if hit:
                self._tactic_counts[f"pressure.{name}"] += 1
                current.add(f"pressure.{name}")

        for name, hit in adversarial.get("prompt_hits", {}).items():
            if hit:
                self._tactic_counts[f"adversarial.{name}"] += 1
                current.add(f"adversarial.{name}")

        repeats = sum(1 for t in current if self._tactic_counts[t] > 1)

        return {
            "current_tactics": sorted(current),
            "repeat_count": repeats,
            "is_escalating": repeats > 0 and len(current) > 0,
            "unique_tactics_seen": sum(
                1 for v in self._tactic_counts.values() if v > 0),
        }

    # ------------------------------------------------------------- anomaly

    def _detect_anomaly(self, risk: float) -> Dict:
        """
        Detect when observed risk diverges from baseline.

        A sudden spike or drop in risk scores indicates a pattern shift
        that warrants investigation.
        """
        distance = abs(risk - self._baseline_risk)
        is_anomalous = distance > self.anomaly_threshold

        if risk > self._baseline_risk + self.anomaly_threshold:
            direction = "spike"
        elif risk < self._baseline_risk - self.anomaly_threshold:
            direction = "drop"
        else:
            direction = "stable"

        return {
            "distance": round(distance, 4),
            "baseline": round(self._baseline_risk, 4),
            "observed": round(risk, 4),
            "is_anomalous": is_anomalous,
            "direction": direction,
        }

    def _respond_to_anomaly(self, anomaly: Dict) -> Dict:
        """
        Adjust investigation priority based on detected anomalies.

        Anomalies raise investigation priority rather than being suppressed —
        unexpected patterns are information, not noise.
        """
        if not anomaly["is_anomalous"]:
            return {
                "action": "normal",
                "priority_change": 0.0,
                "message": "Risk levels within expected range.",
            }

        boost = anomaly["distance"] * 1.5
        self.investigation_priority = min(10.0, self.investigation_priority + boost)

        if anomaly["direction"] == "spike":
            self.sensor_reliability = max(0.5, self.sensor_reliability - 0.05)
            return {
                "action": "investigate_spike",
                "priority_change": round(boost, 4),
                "message": (
                    f"Unexpected risk spike "
                    f"(observed={anomaly['observed']:.2f} vs "
                    f"baseline={anomaly['baseline']:.2f}). "
                    f"Investigation priority raised."
                ),
            }
        else:
            return {
                "action": "investigate_drop",
                "priority_change": round(boost, 4),
                "message": (
                    "Unexpected risk drop. "
                    "Monitoring for pattern shift or evasion."
                ),
            }

    # -------------------------------------------------------------- health

    def _update_health(self, risk: float, anomaly: Dict):
        """
        Update system health metric.

        health = (accuracy * consistency * diversity) - unreliability

        Where:
            accuracy:    inverse of anomaly distance (good predictions)
            consistency: internal agreement between sensors
            diversity:   variance in recent risk scores (not stuck)
            unreliability: 1 - sensor_reliability
        """
        distance = anomaly["distance"]

        # Prediction accuracy: improves when baseline matches observation
        if distance < self.anomaly_threshold:
            self.prediction_accuracy = min(10.0, self.prediction_accuracy + 0.2)
        else:
            self.prediction_accuracy = max(0.0,
                                           self.prediction_accuracy - 0.1 * distance)

        # Detection score: grows from clean passes and caught threats
        if risk < 0.2:
            self.detection_score += 0.1 * self.prediction_accuracy
        elif risk > 0.5 and self.sensor_reliability > 0.8:
            self.detection_score += 0.2  # caught a real threat

        # Diversity of recent readings
        if self._risk_history:
            recent = self._risk_history[-10:]
            diversity = max(0.5, _variance(recent))
        else:
            diversity = 1.0

        # Unreliability
        unreliability = 1.0 - self.sensor_reliability

        # Composite health
        self.system_health = (
            self.prediction_accuracy * self.internal_consistency * diversity
        ) - unreliability

        # Reliability recovery when health is good
        if self.system_health > 2.0:
            self.sensor_reliability = min(1.0, self.sensor_reliability + 0.02)

    def _update_baseline(self, risk: float):
        """Exponential moving average of risk scores."""
        a = self._baseline_alpha
        self._baseline_risk = a * risk + (1 - a) * self._baseline_risk

    def _compute_trend(self) -> Dict:
        """Detect rising/falling/stable risk trajectory."""
        history = self._risk_history
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

    # -------------------------------------------------------------- alerts

    def _generate_alerts(self, risk: float, anomaly: Dict,
                         conflicts: List[str], escalation: Dict) -> List[Dict]:
        """Generate contextual alerts from fused sensor data."""
        alerts: List[Dict] = []

        if risk >= self.alert_threshold:
            alerts.append({
                "level": "high",
                "type": "manipulation_risk",
                "message": f"Risk index {risk:.2f} exceeds threshold {self.alert_threshold}.",
            })

        if escalation["is_escalating"]:
            alerts.append({
                "level": "medium",
                "type": "escalation",
                "message": (
                    f"Repeated tactics detected "
                    f"({escalation['repeat_count']} repeats this turn)."
                ),
            })

        if len(conflicts) >= 3:
            alerts.append({
                "level": "high",
                "type": "conflict_accumulation",
                "message": f"{len(conflicts)} accumulated conflicts across conversation.",
            })

        trend = self._compute_trend()
        if trend["direction"] == "rising" and len(self._risk_history) >= 3:
            alerts.append({
                "level": "medium",
                "type": "rising_trend",
                "message": f"Risk trending upward (slope={trend['slope']:.3f}).",
            })

        if self.system_health < 0:
            alerts.append({
                "level": "high",
                "type": "health_degraded",
                "message": (
                    f"System health {self.system_health:.2f} is negative. "
                    f"Sensor reliability may be compromised."
                ),
            })

        if anomaly["is_anomalous"] and anomaly["direction"] == "spike":
            alerts.append({
                "level": "medium",
                "type": "anomaly_spike",
                "message": (
                    f"Risk anomaly detected "
                    f"(distance={anomaly['distance']:.2f} from baseline)."
                ),
            })

        return alerts

    # -------------------------------------------------------------- util

    def reset(self):
        """Reset all state. Use between unrelated conversations."""
        self.__init__(model=self.model, context=self.context,
                      anomaly_threshold=self.anomaly_threshold,
                      alert_threshold=self.alert_threshold)


def _variance(xs: List[float]) -> float:
    """Population variance."""
    if not xs:
        return 0.0
    mean = sum(xs) / len(xs)
    return sum((x - mean) ** 2 for x in xs) / len(xs)
