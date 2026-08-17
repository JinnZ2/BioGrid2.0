# Biogrid Changelog

All notable changes to this repository are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) principles, versioned by schema/doc revisions.

---

## [0.2.1] - 2026-08-14
### Added
- `docs/legacy/FALSIFICATION-LOG.md` — append-only record of every completed run
  against a BioGrid claim: what was tested, what it returned, which unknowns it
  opened (U1–U5), and the rerun trigger. Includes the first **corroborated** run,
  because a log of only failures is a biased sample.
- Third state (**Falsified**) added to `planned/Experiments/VALIDITY.md`, which
  previously tracked validated/speculative and had nowhere to put a claim that
  was checked and failed.

### Changed
- `docs/legacy/README.md` rewritten: legacy is the **run record**, not a
  graveyard. The blanket "never cite legacy as evidence" rule was too blunt and
  discarded the precedent — split into "never as evidence about the world,
  always as evidence about the reasoning."
- Six outcome states defined (FALSIFIED / MISATTRIBUTED / STALE / UNSOURCED /
  CORROBORATED / SUPERSEDED). Documents retire only for FALSIFIED or SUPERSEDED;
  stale figures are refreshed in place rather than hidden behind a retirement.
- Run 001 reclassified the 15 v1 corrections by state: 6 falsified,
  3 misattributed, 4 stale, 2 unsourced. **Eleven of fifteen trace to citing
  something other than the primary source** — the dominant failure mode is
  citation discipline, not research depth.
- `Resilience/The-line-redesign.md` — dated status addendum (Sept 2025
  suspension, pause past 2030, <300k residents, ~$16bn cancellation costs). The
  document's thesis was tested by events and **held**; figures were stale, so it
  is refreshed in place and logged as corroborated, not retired.
- `planned/HISTORICAL.md` → `docs/legacy/HISTORICAL.md`. A record of already-
  graduated code was filed in a folder its own `PLANNED.md` defines as
  future-only context. The code files stay where they are — legacy by reference.

---

## [0.2.0] - 2026-08-14
### Added
- `docs/integration/Technical-validation.md` (v2) — rebuilt evidence base with an
  A/B/C/D evidence grading scheme, retrieval dates on every figure, a
  method-by-method 2026 status review, and six falsifiable predictions replacing
  the previous undocumented outcome percentages.
- `docs/science/METHODS.md` — method register (ADOPT / KEEP / BOUND / WATCH /
  RETIRE) per subsystem, including a routing interface contract for `swarm/`
  agents and four bounded improvements for the sensors package.
- `docs/science/REFERENCES.md` — consolidated graded bibliography plus an
  explicit list of sources that did not survive verification.
- `data/reference.figures.v0.1.json` + `data/ReferenceFiguresSHA.txt` —
  machine-readable figures register with grades, sources, `as_of` dates, and a
  `retracted` block.
- `docs/legacy/README.md` — retirement policy: superseded documents are kept
  verbatim, banner-marked, and excluded from citation.

### Changed
- `README.md` — corrected two references to files that do not exist
  (`docs/framework/bio-grid-universal-framework.md`, `docs/blueprint/bio-grid-seed.md`),
  rewrote Quick Start against the real repository layout, added the evidence policy.
- `INDEX.md` — added Science and Legacy sections and the figures register.
- Great Lakes water figure corrected to 21% of the world's *surface* fresh water
  (84% of North America's), per US EPA.

### Corrected / Retracted
Fifteen claims in the v1 evidence document failed verification. Full list in
`docs/integration/Technical-validation.md` §1. The consequential ones:
- ACO attribution to UPS ORION, Amazon warehouse routing, and "RFC 3626" all
  withdrawn — RFC 3626 is IETF OLSR, not an ACO standard and not IEEE.
- Physarum "O(n log n)" complexity withdrawn; correct citation is Bonifaci,
  Mehlhorn & Varma (2012). "Outperformed Tokyo's rail designers" softened to the
  benchmark comparison the paper actually reports.
- Hempcrete R-value corrected from 2.5–3.0 to **≈1.6–2.4 per inch** from measured
  thermal conductivity — the old figure would under-insulate any wall built to it.
- "BioMASON acquired by Ginkgo Bioworks" withdrawn as false.
- Undocumented $/kWh comparison withdrawn; replaced by published LCOE ranges.

### Deprecated
- `docs/legacy/Technical-validation.v1.md` — superseded, retained verbatim for
  provenance. Not to be cited.

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
