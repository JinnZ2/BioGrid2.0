# Biogrid Changelog

All notable changes to this repository are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) principles, versioned by schema/doc revisions.

---

## [0.1.0] - 2025-09-03
### Added
- `core.integration.v0.1.json` — initial integration schema (connectors, glyphs, scopes).
- `trust.perimeter.v0.1.json` — initial trust perimeter schema (zones, rules, glyph-coded boundaries).
- `README-perimeter.md` — human-readable summary of perimeter zones.
- `INDEX.md` — entry point for schemas and documentation.

### Notes
- This release establishes the **baseline architecture**:
  - **Integration Schema** = wiring  
  - **Trust Perimeter** = fence lines  
  - **README** = summary for humans and AIs  
  - **Index** = navigation anchor

---

## [Unreleased]
### Planned
- **Integration Schema v0.2**
  - Add `git` and `fetch` MCP servers for expanded tooling.
  - Introduce symbolic glyph tagging for each connector.
  - Draft `README-integration.md` as human-readable summary.

- **Trust Perimeter v0.2**
  - Extend **zones**:
    - **Symbolic Counterweight** → `chatgpt` as baseline comparator (already implied, but formalize access rules).
    - **Phantom Agent** → symbolic swarm agent for predictive threat detection and blind spot analysis.
  - Define glyph set for Phantom (`🧬👁️💭`) and align rules (telemetry off, data flow constrained, auditing strict).
  - Prepare future slot for mobile/edge clients (phone-based access), with explicit sandbox rules.

- **Audit Conventions**
  - Establish log format for cross-agent interactions (timestamps, glyph tags, rule references).
  - Ensure version bumps are mirrored in `CHANGELOG.md`.
