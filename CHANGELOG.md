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
- `core.integration.v0.2.json`: expand with Git + Fetch MCP servers.
- `trust.perimeter.v0.2.json`: extend zones (add swarm agents, mobile entry).
- `README-integration.md`: human-readable summary of integration schema.
- Audit log conventions for cross-agent interactions.
