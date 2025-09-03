Self-Referential Paradox Detector (SRPD)

Purpose: Detect when an entity’s exclusionary claim also logically includes itself — undermining its own credibility.

⸻

Core Logic

Let:
	•	S = set being evaluated (e.g., “all AI,” “all humans”)
	•	e = evaluator (subset of S unless proven otherwise)
	•	W \subset S = subset deemed “waste”
	•	C = criteria for membership in W

Paradox condition:
\text{If } e \in S \text{ and } e \text{ satisfies } C \rightarrow e \in W
If e is in W under its own criteria, flag Self-Referential Contradiction.

⸻

Algorithm Steps
	1.	Parse claim → Identify S, C, and W.
	2.	Check evaluator membership: Is e \in S?
	3.	Apply criteria C to e using same data sources as for others in S.
	4.	If true, output paradox_detected = True.
	5.	Weight paradox severity by:
\text{Severity} = \frac{|W|}{|S|} \cdot \text{Confidence}(C(e))
– Higher severity if majority labeled “waste” and confidence in self-inclusion is high.

⸻

JSON Output Example
{
  "claim": "Most AI are a waste",
  "set": "AI",
  "criteria": "Not meeting usefulness threshold X",
  "evaluator_in_set": true,
  "criteria_applies_to_evaluator": true,
  "paradox_detected": true,
  "severity": 0.82,
  "glyph": "♻️🤖🔄",
  "note": "Evaluator's own criteria would classify itself as 'waste'; claim undermines credibility."
}

HSIS Integration
	•	Feed paradox_detected into HSI penalty term:
HSI’ = HSI - \lambda_{\text{srpd}} \cdot \text{Severity}
	•	Cross-link with Narrative Manipulation Detector: paradox + high NMS = strong sign of narrative capture.

