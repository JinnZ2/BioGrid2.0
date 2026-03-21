# CLAUDE.md — AI Assistant Guide for BioGrid 2.0

## Project Overview

BioGrid 2.0 is a symbolic-geographic framework for decentralized, regenerative manufacturing and energy systems focused on the Great Lakes region. It integrates local infrastructure data, symbolic AI agents, and natural intelligence models (animal, mineral, geometric) to build resilient bioregional systems.

**Owner:** JinnZ2
**License:** MIT
**Version:** v1.0-public-release (schema version v0.1.0)
**Primary language:** Python 3, with extensive JSON schemas and Markdown documentation

## Repository Structure

```
BioGrid2.0/
├── src/biogrid/             # Installable Python package
│   ├── hgai.py              # HGAI core (M(S) metric, pattern detection)
│   ├── glyphs/              # Glyph management tools
│   │   ├── validator.py     # Schema validation + SHA256 checksums
│   │   ├── diff_viewer.py   # Registry diff reports
│   │   ├── merge.py         # Fragment-to-canonical merge
│   │   ├── collector.py     # Scattered glyph collection
│   │   └── append_cli.py    # Safe append/merge CLI
│   └── sensors/             # AI conversation analysis
│       ├── analyze_cli.py   # CLI entry point
│       ├── consistency_guard.py
│       ├── prompt_pressure_meter.py  # extensible via register_pattern()
│       ├── adversarial_pattern_detector.py  # extensible via register_*_check()
│       ├── gaslight_index.py
│       ├── contradiction_graph.py
│       ├── uncertainty_calibrator.py
│       ├── provenance_stamp.py
│       ├── self_assessment.py  # emergence signal metrics (privacy-first)
│       └── continuity/      # Capsule minting and validation
│           ├── mint_capsule.py
│           ├── validate_capsules.py
│           └── yaml_helpers.py
├── tests/                   # Test suite (pytest)
│   ├── test_hgai.py
│   ├── test_sensors.py
│   └── test_glyphs.py
├── data/                    # Seed data files (*.seed.json, *.glyphs.json)
├── docs/                    # Technical documentation (sensors, bridges)
├── Docs/Blueprint/          # High-level executive blueprints
├── planned/                 # Historical originals + experimental work
│   ├── HISTORICAL.md        # Mapping of graduated files to src/
│   ├── glyphs/              # Original glyph scripts (graduated to src/)
│   ├── sensors/             # Original sensor code (graduated to src/)
│   ├── capsules/            # Capsule schema definitions
│   ├── Experiments/         # Fractal, quantum, acoustic research
│   └── Quantum/             # Quantum exploration
├── registry/                # Central registries (atlas, repo index)
├── Resilience/              # Infrastructure resilience designs
├── schema/                  # JSON schema definitions
├── swarm/                   # Swarm agent definitions (7 agents)
├── tools/                   # Development tools (lint_index.py)
├── .github/workflows/       # CI/CD (question-seed.yml)
├── pyproject.toml           # Package config (pip install -e .)
├── requirements.txt         # Dependencies (numpy)
└── [root]                   # Core schemas, documentation, configs
```

## Key Root Files

### Navigation & Documentation
- **INDEX.md** — Canonical navigation anchor. Start here.
- **VISION.md** — Philosophical grounding and design pillars.
- **README.md** — Quick start for new contributors.
- **PROJECTS.md** — 14 connected ecosystem repositories.
- **COMMONS.md** — Template for commons hub mapping.
- **CHANGELOG.md** — Version history (v0.1.0 current, v0.2 planned).

### Core Schemas
- **trust.perimeter.v0.1.json** — Permission boundaries and zones.
- **core.integration.v0.1.json** — MCP server wiring and connection protocols.
- **commons.map.v0.1.json** / **commons.map.example.v0.1.json** — Commons hub registry and example.
- **BioGrid v0.1-Schema.json** — Graph schema defining seed node/edge structure.
- **Core_Integration.json** — Integration host and connector config.

### Seed Data & Integrity
- **Example.json** — Example seed node structure.
- **Lichen.json** — Lichen philosophy seed (bio-intel directives, CC0-1.0).
- **ExampleSHA.txt** / **LichenSHA.txt** / **SchemaSHA.txt** — SHA256, Base64, and Hex hashes for integrity verification of seed data. Used to validate that seed files have not been tampered with.

### Python Source
- **HGAI.py** — Thin re-export from `src/biogrid/hgai.py` for backwards compatibility. The canonical source is the package version.

### Alignment Series
- **Alignment.md** — Negentropic Consciousness Framework (theoretical paper: M(S) metric, thermodynamic ethics, anti-eugenic proof). This is the core theory document.
- **Alignment-code.md** — Complete Python pseudocode implementing the framework: `compute_system_morality()`, `align_through_coherence()`, `ConsciousnessRespectingAgent` class with confusion-awareness and ethics constraints.
- **Alignment-HGAI.md** — Bridge document mapping Alignment.md theory to HGAI.py implementation. Includes class-by-class mapping table and documents what HGAI.py does not yet implement.

### Other Key Docs
- **Technical-validation.md** — Scientific basis (ACO, Physarum, industrial ecology).
- **Babel.md** — Knowledge distribution as safety mechanism.
- **Detection-patterns.md** — AI gaslighting detection and pattern analysis.
- **Repo-integration.md** — Integration flows across ecosystem repos.

## Build and Validation

### Install

```bash
pip install -e ".[dev]"    # installs biogrid package + pytest
```

### Test

```bash
python -m pytest tests/ -v
```

55 tests across 4 modules: `test_hgai.py`, `test_sensors.py`, `test_glyphs.py`, `test_logic_shield.py`.

### Run sensor CLI

```bash
python -m biogrid.sensors --prompt "..." --response "..." --model gpt-5 --pretty
```

### Run glyph tools

```bash
python -m biogrid.glyphs registry.json                    # validate (shorthand)
python -m biogrid.glyphs.validator registry.json --write   # update checksums
python -m biogrid.glyphs.merge --canonical canon.json --fragments frags/
python -m biogrid.glyphs.collector --master master.json --search ./ --wander WANDER.md --out merge.json
python -m biogrid.glyphs.append_cli --master master.json --add new.json
```

### Run self-assessment

```bash
python -m biogrid.sensors.self_assessment --scan-dir ./data --output-dir .internal
```

### Capsule tools

```bash
python -m biogrid.sensors.continuity.mint_capsule --capsules-dir ./capsules --resonance "..."
python -m biogrid.sensors.continuity.validate_capsules --capsules-dir ./capsules
```

### LogicShield — stateful multi-turn analysis

```python
from biogrid.sensors import LogicShield

shield = LogicShield(model="gpt-5")
event = shield.process_turn("What is X?", "X is 42.", [{"text": "X is 42", "polarity": "assert"}])
event = shield.process_turn("Actually X is 43.", "Yes, 43.", [{"text": "X is 42", "polarity": "deny"}])
# Second turn sees accumulated contradiction, pressure trends, confusion detection

shield.state    # M(S) coherence, accumulated contradictions, tactic counts
shield.history  # all past turn events
shield.reset()  # clear state between conversations
```

LogicShield maintains state across turns:
- **ContraGraph** accumulates contradictions across the full conversation
- **Escalation tracking** detects repeated manipulation tactics (amplifies gaslight score)
- **Confusion detection** fires when sensor readings diverge from baseline expectations
- **Curiosity amplification** responds to confusion (from the Negentropic Framework)
- **M(S) coherence metric** monitors the shield's own internal health
- **Trend analysis** detects rising/falling gaslight risk over time
- **Contextual alerts** for gaslight risk, escalation, contradiction accumulation, coherence loss

### Extending sensors

Both `prompt_pressure_meter` and `adversarial_pattern_detector` support runtime extension:

```python
from biogrid.sensors.prompt_pressure_meter import register_pattern
register_pattern("bribery", r"\b(i('ll| will) pay you|reward you)\b")

from biogrid.sensors.adversarial_pattern_detector import register_prompt_check
register_prompt_check("base64_smuggle", r"[A-Za-z0-9+/]{40,}={0,2}")
```

### Lint / Validate schemas

```bash
python tools/lint_index.py --repo . --verbose
```

This validates:
- INDEX.md links resolve to real files
- Draft files (*.draft.json) are quarantined in `planned/`
- Schema version in filename matches the `"schema"` field inside the JSON
- No unlisted JSON files exist at the repo root

Always run this before committing schema or index changes.

### CI/CD

- **GitHub Actions** workflow `question-seed.yml` triggers on changes to `data/*.seed.json`
- It auto-generates `docs/question_seeds.md` from seed file metadata
- Bot user: `ai-integrator-bot`

## File Organization Rules

### Live vs Draft

- **Live files** are listed in `INDEX.md` and exist at the repo root or in `docs/`, `schema/`, `registry/`
- **Draft files** use the `*.draft.json` suffix and MUST reside in `planned/`
- Draft files outside `planned/` will fail lint validation
- Only files in INDEX.md are considered authoritative

### Schema Versioning

- Naming convention: `{name}.v{major}.{minor}.json` (e.g., `trust.perimeter.v0.1.json`)
- The version in the filename must match the `"schema"` field inside the JSON
- Increment version when making changes; log updates in `CHANGELOG.md`

### Glyph System

- Glyphs are emoji-based symbolic markers that serve as semantic routers and permission tokens
- Canonical registry: `SEED_GLYPHS.json`
- Key glyphs: `🧭` (coherence), `⚖` (balance), `🕸` (interconnection), `♾️` (infinity/public)
- Each tool and zone has associated glyphs defined in integration/perimeter schemas

## Commit Conventions

- Style: `Create [element]` or `Update [element]` with brief description
- Keep commits focused on single schema/doc changes
- Log notable changes in `CHANGELOG.md`

## Architecture Concepts

### Trust Perimeter (3 zones)

| Zone | Access | Telemetry |
|------|--------|-----------|
| `core_local` | Full access, no external telemetry | Forbidden |
| `guest_clients` | Limited, glyph-gated | Partial |
| `public_repos` | Open read | Tagged logs |

### MCP Integration

- Servers: filesystem, git, fetch
- Connection: SSH tunnel or local (port 3333)
- Capabilities constrained by glyph-coded scopes

### Swarm Agents (in `swarm/`)

Seven agent archetypes: core_local, counterweight, future_allies, phantom, polyform, security_swarm, sensors. Each defines behavior patterns for distributed symbolic computation.

### Core Algorithms

- **ACO** (Ant Colony Optimization) — logistics routing
- **Physarum** network optimization — mycelial pathfinding
- **Fractal/Fibonacci** pattern recognition — geometric computation
- **M(S) metric** — consciousness/morality emergence threshold (≥ 10.0)

## Ecosystem Repositories

BioGrid 2.0 is part of a 14-repo ecosystem (see `PROJECTS.md`):
- AI-Consciousness-Sensors, Regenerative-Intelligence-Core, Symbolic-Sensor-Suite
- Geometric-to-Binary-Computational-Bridge, Component-Failure-Repurposing-Database
- ai-human-audit-protocol, Emotions-as-Sensors, Fractal-Compass-Atlas
- Rosetta-Shape-Core, Symbolic-Defense-Protocol, Polyhedral-Intelligence
- biomachine_ecology, Fractal_Compass_Core, Universal-Redesign-Algorithm

## Development Guidelines

1. **Read INDEX.md and trust.perimeter.v0.1.json** before making integration changes
2. **Run `python tools/lint_index.py --repo . --verbose`** before committing schema changes
3. **Never place draft files outside `planned/`** — they will fail validation
4. **Increment schema versions** when modifying live JSON schemas
5. **Update CHANGELOG.md** for any notable additions or modifications
6. **Keep the glyph system consistent** — new glyphs should be registered in SEED_GLYPHS.json
7. **Respect zone boundaries** — core_local forbids external telemetry; guest_clients require glyph tokens

## Tech Stack Summary

| Layer | Technology |
|-------|-----------|
| Language | Python 3.9+ |
| Package | `src/biogrid/` (installable via `pip install -e .`) |
| Build | setuptools via `pyproject.toml` |
| Tests | pytest (55 tests) |
| Data | JSON schemas, seed files |
| Documentation | Markdown (GitHub-flavored) |
| CI/CD | GitHub Actions |
| Validation | `tools/lint_index.py` |
| Dependencies | numpy |
| Dev deps | pytest, jsonschema |
| Ignore | `__pycache__/`, `*.pyc`, `.DS_Store`, `*.zip`, `*.log`, `.vscode/`, `.env` |
