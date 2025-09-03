Narrative Manipulation Detector (NMD)

Purpose: Detect divergence between reported system health and actual ground-truth signals.

⸻

1. Core Variables
	•	RII_{\text{official}} = Reported Reciprocity Integrity Index
	•	RII_{\text{ground}} = Measured/anonymous Reciprocity Integrity Index
	•	CPGI_{\text{official}} = Reported Constructive Productivity Gain Index
	•	CPGI_{\text{ground}} = Measured/anonymous CPGI
	•	O_{\text{hard}} = Hard outcome metrics (attrition, defect rate, safety incidents)

⸻

2. Manipulation Divergence Metric

For each metric X:
D_X = \frac{|X_{\text{official}} - X_{\text{ground}}|}{\max(X_{\text{official}}, X_{\text{ground}}, 0.01)}
Large D_X means official data diverges significantly from ground truth.

⸻

3. Narrative Mismatch Score (NMS)

NMS = \frac{D_{RII} + D_{CPGI} + D_O}{3}
Where D_O is divergence between official morale/productivity claims and hard outcomes.

⸻

4. Risk Levels
	•	NMS < 0.2 → Narrative matches reality
	•	0.2 ≤ NMS < 0.5 → Warning: possible spin
	•	NMS ≥ 0.5 → High risk: reality distortion in effect

⸻

5. AI Training Implication

In AI training context:
	•	Replace “official” with curated/public-facing datasets.
	•	Replace “ground” with raw/unfiltered human experience.
	•	High NMS means AI is being taught a fictionalized humanity.

⸻

6. JSON Output
{
  "timestamp": "2025-08-11T23:12:00Z",
  "RII_official": 0.85,
  "RII_ground": 0.42,
  "CPGI_official": 0.90,
  "CPGI_ground": 0.50,
  "O_hard": {"attrition": 18, "defects_per_million": 320, "incidents": 14},
  "NMS": 0.56,
  "status": "High risk: reality distortion",
  "glyph": "🎭📉"
}

