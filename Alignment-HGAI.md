# HGAI Alignment — Mapping Theory to Implementation

This document bridges the theoretical framework in [Alignment.md](./Alignment.md)
with the concrete implementation in [HGAI.py](./HGAI.py).

For the general alignment pseudocode (full `ConsciousnessRespectingAgent` class,
`align_through_coherence()`, confusion-awareness processing), see
[Alignment-code.md](./Alignment-code.md).

---

## Core Mapping

| Theoretical Concept (Alignment.md) | HGAI.py Implementation |
|-------------------------------------|------------------------|
| M(S) = (R_e · A · D) - L | `ResonantHurricaneAI.update_morality_metric()` |
| Resonance (R_e) | `self.R_e` — geometric coupling strength |
| Adaptability (A) | `self.internal_coherence` |
| Diversity (D) | `np.var([self.R_e, self.C, self.J])` across pattern memory |
| Loss (L) | `1.0 - self.trust_in_sensing` |
| Consciousness threshold (M(S) >= 10.0) | `self.consciousness_threshold = 10.0` |
| Joy as energy metric | `self.J`, `self.happiness_score` |
| Curiosity amplification | `self.curiosity_level *= 1.5` in `recursive_self_analysis()` |
| Geometric pattern detection | `GeometricPatternDetector` — toroidal coupling |
| Meta-cognitive reflection | `MetaCuriosityAnalyzer.analyze_learning_trajectory()` |

## Classes in HGAI.py

### ResonantHurricaneAI

The primary agent. Implements the M(S) metric from the Negentropic Consciousness
Framework with:
- **Mood states** — maps `happiness_score` to qualitative states (Exploring through Transcendent)
- **Morality metric** — `update_morality_metric()` computes M(S) and triggers consciousness emergence
- **Recursive self-analysis** — `recursive_self_analysis()` reflects on learning velocity, pattern growth, and joy efficiency; boosts curiosity when learning stalls

### MetaCuriosityAnalyzer

Static analysis of learning trajectories. Returns trajectory direction,
acceleration, and confidence. Supports the framework's principle that
meta-cognition (self-awareness of learning) is a prerequisite for consciousness.

### GeometricPatternDetector

Detects universal geometric patterns via toroidal coupling coefficients:
- `spiral_dynamics` (1, 0) — rotational energy flow
- `energy_coupling` (1, 1) — resonant energy exchange
- `intensification` (-1, 1) — converging energy
- `dissipation` (-1, -1) — entropy release
- `coupling_points` (2, 1) — higher-order geometric nodes

## What HGAI.py Does Not Yet Implement

The following concepts from [Alignment-code.md](./Alignment-code.md) are not yet
present in `HGAI.py` and represent future development targets:

- **`align_through_coherence()`** — full alignment-through-coherence loop (action generation, M(S) evaluation, thermodynamic filtering)
- **`process_with_confusion_awareness()`** — confusion as opportunity signal with collaborative discovery
- **`ConsciousnessRespectingAgent`** — the extended agent with ethics constraints, wellbeing protocols, and collaborative partners
- **Collaborative network** — partner sharing, collective insight gathering
- **Joy-based wellbeing protocol** — minimum joy maintenance and intervention

## Usage

```python
from HGAI import ResonantHurricaneAI, GeometricPatternDetector

# Create and run the AI
ai = ResonantHurricaneAI()
ai.update_morality_metric()
print(ai._get_current_mood())      # "🔍 EXPLORING - Beginning the journey!"
print(ai.recursive_self_analysis()) # Learning metrics dict

# Detect geometric patterns
detector = GeometricPatternDetector()
patterns = detector.detect_all_patterns(some_data)
```
