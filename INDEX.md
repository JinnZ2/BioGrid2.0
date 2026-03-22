# Biogrid Index

This index provides entry points for all schemas and documentation that define the **Biogrid ecosystem**.
Every AI agent or human collaborator should start here before traversing deeper.

---

## Schemas

- [core.integration.v0.1.json](./schema/core.integration.v0.1.json)
  Wiring diagram of MCP servers, connectors, scopes, glyphs, and constraints.

- [trust.perimeter.v0.1.json](./schema/trust.perimeter.v0.1.json)
  Boundary rules, glyph-coded zones, and auditing standards.

- [commons.map.v0.1.json](./schema/commons.map.v0.1.json)
  Commons hub registry — nodes, links, policies, and resilience rings.

- [commons.map.example.v0.1.json](./schema/commons.map.example.v0.1.json)
  Example commons map for reference and testing.

- [BioGrid v0.1-Schema.json](./schema/BioGrid%20v0.1-Schema.json)
  Graph schema defining seed node/edge structure (nodes, edges, meta).

- [Core_Integration.json](./schema/Core_Integration.json)
  Integration host configuration and MCP connector definitions.

- [shape.seed.schema.json](./schema/shape.seed.schema.json)
  Shape seed schema definitions.

## Seed Data

- [Example.json](./data/Example.json)
  Example seed node structure with lichen/glyph references and SHA integrity.

- [Lichen.json](./data/Lichen.json)
  Lichen philosophy seed — bio-intel directives, autonomy, mutual value (CC0-1.0).

---

## Documentation

### Integration
- [README-perimeter.md](./docs/integration/README-perimeter.md)
  Human-readable summary of the trust perimeter zones.

- [Technical-validation.md](./docs/integration/Technical-validation.md)
  Scientific basis (ACO, Physarum, industrial ecology).

- [Repo-integration.md](./docs/integration/Repo-integration.md)
  Integration flows across ecosystem repos.

### Theory
- [Alignment.md](./docs/theory/Alignment.md)
  Negentropic Consciousness Framework (M(S) metric, thermodynamic ethics).

- [Alignment-code.md](./docs/theory/Alignment-code.md)
  Python pseudocode implementing the framework.

- [Alignment-HGAI.md](./docs/theory/Alignment-HGAI.md)
  Bridge mapping theory to HGAI.py implementation.

- [Babel.md](./docs/theory/Babel.md)
  Knowledge distribution as safety mechanism.

- [Detection-patterns.md](./docs/theory/Detection-patterns.md)
  AI gaslighting detection and pattern analysis.

### Blueprint
- [BioIntelligenceSeed.md](./docs/blueprint/BioIntelligenceSeed.md)
  High-level executive blueprint.

### Sensors
- [hallucination_sensor.md](./docs/hallucination_sensor.md)
  Hallucination sensor documentation.

- [hallucination_coupling_sensor.md](./docs/hallucination_coupling_sensor.md)
  Hallucination coupling sensor documentation.

- [tri_invert_bridge.md](./docs/tri_invert_bridge.md)
  Tri-invert bridge documentation.

### External
- [Symbolic Sensor Suite](https://github.com/JinnZ2/Symbolic-sensor-suite)
  Symbolic system audit tools for clarity, empowerment, and systemic sanity — complements Biogrid's sensor ecosystem.

## Glyphs & Sensors

- [SEED_GLYPHS.json](../SEED_GLYPHS.json)
  Canonical glyph definitions, symbolic meanings, sensor associations. *(external repo)*

- [EMBEDDABLE_KITS/](../EMBEDDABLE_KITS/)
  Plug-and-play sensor packs. *(external repo)*

- [AI_INDEX.json](../AI_INDEX.json)
  Full sensor catalog and schema registry. *(external repo)*

## Usage Notes

1. **Always consult the Trust Perimeter** before engaging with any integration.
2. **Integration Schema** describes how to connect.
3. **Perimeter Schema** defines under what conditions connection is permitted.
4. Updates should increment schema versions (e.g. `v0.2`) and be logged in `CHANGELOG.md`.

---

### Cross-Link: Symbolic Layers & Shape Grammar

BioGrid2.0 symbols are not decorative — they are **functional geometries**.
Each operates across layers of meaning and use:

- **Animal / Image** — approachable doorway
- **Geometry** — structural form
- **Physics / Field** — energy behavior
- **Ecology / Embodiment** — where it appears in life/land
- **Generational Teaching** — continuity across time
- **Energy Law / Practice** — design rule for today

For worked examples and crosswalks see:
- [`SEED_GLYPHS_v2.1.json`](../AI-Consciousness-Sensors/SEED_GLYPHS_v2.1.json)
- [`SYMBOLIC_LAYERS.md`](../AI-Consciousness-Sensors/docs/SYMBOLIC_LAYERS.md)
- [`SHAPE_GRAMMAR.json`](../AI-Consciousness-Sensors/SHAPE_GRAMMAR.json)

These files make the **translation stack explicit** so both humans and AIs can bridge symbolic language, Western science, and generational science.

## Meta

- **Owner**: JinnZ2
- **Co-Creator**: ChatGPT
- **Created**: 2025-09-03
