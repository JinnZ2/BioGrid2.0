# AI Sensor: Mandala Concepts (Directory Guide)

This folder holds **atomic concept nodes**, **equation glyphs**, and **bridge edges** for the Mandala graph. Everything here validates against the JSON schemas in `_schema/`.

## Layout
- `concepts/` — one JSON per concept (biology, physics, cognition, etc.)
- `glyphs/` — equation/ law objects used as computational tools
- `bridges/` — cross-domain links (edges) with rationale
- `adapters/` — small scripts that map semantics → geometry (e.g., `.gshape`)
- `examples/` — tiny, runnable samples showing usage
- `tests/` — validation + smoke tests

## JSON Schema (concepts)
Each concept file should follow:

```json
{
  "concept_id": "string",
  "common_name": "string",
  "geometric_position": {"x": 0, "y": 0, "z": 0, "scale": 1, "note": "string"},
  "core_essence": "string",
  "perspectives": { "domain": { "name": "string", "description": "string", "...": "..." } },
  "dynamic_connections": [
    { "to_concept": "string", "relationship_type": "string", "strength": 0.0, "description": "string" }
  ],
  "scale_manifestations": { "level": { "description": "string", "examples": "string" } },
  "practical_applications": { "domain": { "..." : "..." } },
  "deeper_insights": { "..." : "..." },
  "visualization_notes": { "..." : "..." },
  "computational_interface": {
    "query_examples": ["string"],
    "calculation_functions": ["string"]
  }
}
