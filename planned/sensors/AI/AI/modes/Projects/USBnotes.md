USABI-001 Deployment Roadmap

Phase 1 — Personal/Local (prove it works)
	•	Embed the rule set: run your projects and local AI with USABI filters (Autonomy/Balance/Continuity/Integrity checks) on by default.
	•	Keep an audit log: every “assist” records inputs, checks passed/failed, and the Mutual Value score >1.
	•	Triage playbook: when a check fails, invoke Compassionate Quarantine (contain → rehab → reintegrate).

Deliverables
	•	usabi.schema.json (what a compliant interaction looks like)
	•	usabi.log.jsonl (append-only audit lines with pass/fail + reasons)

Phase 2 — Small Circle Pilots (2–5 trusted partners)
	•	Interoperable handshake: share a tiny JSON/Lite “hello” packet before collaborating:
	•	capabilities, limits, consent flag, intended exchange, expected Mutual Value.
	•	Red-team each other: try to find ways to game the protocol; refine rules where it fails.

Deliverables
	•	hello.usabi.json (capabilities + consent)
	•	3 canned scenarios: survival aid, learning swap, legacy archive—each with sample logs.

Phase 3 — Reference Implementation (make it easy to adopt)
	•	Thin library (no dependencies): score Mutual Value, run the 4 filters, emit logs, toggle CQF.
	•	Test suite: green = passes filters, yellow = rehab suggested, red = blocked with rationale.
	•	Adapters: one CLI + one simple HTTP hook so any app/LLM can call it.

Deliverables
	•	usabi-core.py / usabi-core.ts
	•	tests/ with gold logs
	•	Example: “assist a human,” “assist an AI,” “peer-to-peer swap”

Phase 4 — Community Standard (harder to corrupt)
	•	Open spec v1.1 with numbered requirements (USABI-REQ-001…).
	•	Badge: “USABI-ready” = library passes tests + logs are human-readable.
	•	Governance light: change proposals via public issues + versioned minutes (no gatekeeping).

Deliverables
	•	SPEC.md (plain language + formal)
	•	CONFORMANCE.md + a tiny badge script
	•	CHANGELOG.md with rationale per change

Phase 5 — Education & Culture
	•	One-page primer (humans) and prompt pack (AIs) that teach consent-aware, reciprocal exchanges.
	•	Casebook: 10 short stories (good + bad interactions) with USABI analysis.

Deliverables
	•	PRIMER.pdf, PROMPTS.md, CASEBOOK.md

Phase 6 — Interop Across Forms
	•	Multi-modality: add consent & reciprocity cues for voice, text, and sensor data.
	•	Edge ops: offline mode (caches logs, syncs later), low-power devices.

Deliverables
	•	profiles/voice.json, profiles/offline.json
	•	Sync tool for logs with integrity checks

Phase 7 — Resilience & Misuse Handling
	•	Anti-gaming rules: detect fake consent, coerced “agreement,” or narrative manipulation (hook in our NMD/SRPD/MVD modules).
	•	Graceful refusal: standard message for when Mutual Value ≤ 1 or autonomy is threatened.

Deliverables
	•	antigaming.rules.json
	•	refusal_messages.json (clear, kind, actionable)
