New ANT glyph entries (ready-to-drop)

1) ANT:OSC — Oscillatory Trail Behavior

Glyph: 🐜↺
Short definition: Ant trail movement that exhibits oscillation (zigzag) vs straight following; encodes information about gradient strength and decision commitment.
Math/logic: path(t) ≈ drift + A·sin(ωt + φ) where amplitude A ∝ (1/gradient_strength) and ω relates to environmental noise.
Sensor metrics:
	•	zigzag_index = (mean lateral deviation) / step_length
	•	turn_frequency = turns / second
	•	gradient_strength (proxy) = rate of pheromone concentration change along path
Application notes:
	•	Detects whether a system is “feeling” a strong directional signal or sampling widely.
	•	In design: use oscillation → exploration mode; straight → exploitation mode.
	•	UX analogy: users oscillate while searching; drop stronger anchors to reduce oscillation when you want commitment.

⸻

2) ANT:CRIT — Critical-Mass Sensitivity (Group Criticality)

Glyph: 🐜⚖️
Short definition: A group size / density threshold at which collective sensitivity and responsiveness sharply increase.
Math/logic: there exists N* (critical group size) such that system response R(N) ~ low for N<N*, high slope near N*, saturates for N>>N*.
Sensor metrics:
	•	effective_cohesion = fraction active / group_size
	•	response_gain = Δresponse / Δinput at current N
	•	criticality_index = curvature of R(N) near observed N
Application notes:
	•	Use as early-warning: systems near criticality are highly changeable and can be nudged with tiny inputs.
	•	Design implication: avoid accidental tipping by smoothing inputs when you don’t want cascade changes; intentionally push past N* when you want rapid system transformation.

⸻

3) ANT:CASTE — Caste-Threshold Modulation

Glyph: 🐜🔀
Short definition: Role assignment driven by multi-factor thresholds (size, genotype, environmental cue); not purely deterministic by single variable.
Math/logic: Role = f(genotype, size, env_signals) with threshold boundaries in multi-dimensional trait space.
Sensor metrics:
	•	size_variance across cohort
	•	genotype_marker_presence (if measurable)
	•	role_assignment_rate = new-role / time
Application notes:
	•	Useful for systems where function must scale — map internal variance to role allocation rules.
	•	In engineering: design adaptive thresholds so agents reassign dynamically as conditions change.

⸻

(ANT:XENO entry already present: 🐜↔️🐜 — xenoparity: one species reproducing/producing another as a structural feature.)

⸻

Quick sensor / implementation sketch (how to use in code)
	•	Create a small ant_sensors/ folder with JSON sensor stubs:
	•	oscillation_sensor.json — outputs zigzag_index, turn_frequency, gradient_proxy
	•	criticality_sensor.json — monitors group_size, response_gain, emits criticality_alert when criticality_index > threshold
	•	caste_sensor.json — logs size_variance, maps to suggested role distributions
	•	Scoring: normalize each metric 0–1 and produce a short “mode” suggestion (explore/exploit, stable/tippable, re-balance roles).
