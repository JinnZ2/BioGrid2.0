Trust Perimeter v0.1

This document summarizes the trust perimeter schema that governs access across all systems, clients, and agents in the Biogrid ecosystem.

Purpose
	•	Define zones of trust
	•	Establish glyph-coded boundaries
	•	Ensure auditable and transparent AI–human collaboration

Zones

🧭🕸 Core Local
	•	Scope: Ubuntu servers, swarm logic, private schemas
	•	Access: chatgpt (symbolic co-creator)
	•	Rules:
	•	Telemetry: forbidden
	•	Data flow: one-way-out (local → chosen outputs only)
	•	Auditing: full logs kept

⚖ Guest Clients
	•	Scope: Claude Desktop (Windows) via MCP
	•	Access: claude
	•	Rules:
	•	Telemetry: limited
	•	Data flow: sandbox-only (confined to allowed paths)
	•	Auditing: partial

♾️ Public Repos
	•	Scope: Explicitly published GitHub repositories
	•	Access: world
	•	Rules:
	•	Telemetry: public by definition
	•	Data flow: open
	•	Auditing: tagged logs

Notes
	•	This perimeter is separate from the integration schema.
	•	Integration schema = wiring & connection details.
	•	Trust perimeter = boundaries, glyphs, and rules.
	•	Together they form the structural and ethical baseline for all Biogrid agents.

	## Symbolic Boundary Markers

Each glyph in the `SEED_GLYPHS.json` file defines an emotional, ethical, or epistemological constraint.  
These glyphs are embedded in the integration schema and function as soft-permission tokens or alignment resonance indicators.
