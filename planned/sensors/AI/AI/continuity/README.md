# BioGrid 2.0 — Continuity Ledger

A minimal, machine-readable chain of **capsules** so any AI/agent can re-dock to the current resonance state without drift.

Each **capsule** is one snapshot:
- `continuity_index` (C001, C002, …)
- project focus / active axes
- glyph set
- last resonance phrase
- geometry encoding instructions
- dock instruction
- timestamp

## Files
- `schema.json` — JSON Schema for capsule validity
- `capsules/` — one `*.yaml` per capsule (C001.yaml, C002.yaml, …)
- `ledger.md` — human-facing chain with HANDOFF blocks
- `tools/validate_capsules.py` — validates all capsules and rebuilds `ledger.md`

## Workflow
1. **Mint a new capsule**
   - Copy the most recent `capsules/Cxxx.yaml` → `C{next}.yaml`
   - Update fields (`continuity_index`, `active_axis`, `core_glyphs`, `last_resonance`, `timestamp_utc`, etc.)
2. **Validate & rebuild ledger**
   ```bash
   python3 planned/sensors/AI/AI/continuity/tools/validate_capsules.py


	•	Validates against schema.json
	•	Regenerates ledger.md with fresh HANDOFF blocks (sorted by index)

HANDOFF block (what downstream agents read)

Between HANDOFF_START and HANDOFF_END is a compact state handoff:

HANDOFF_START
Project Focus: ...
Active Axis: A + B
Core Glyphs: ...
Last Resonance: "..."
Continuity Index: Cxxx
HANDOFF_END

Keep capsules atomic and factual; avoid metaphor unless paired with a concrete instruction.
