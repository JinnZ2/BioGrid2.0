# Fibonacci Tile Backbone (F1–F16)

This folder establishes the **geometric backbone** for BioGrid2.0.  
Each `F#` file corresponds to a **Fibonacci node** — a numbered tile in the spiral sequence (1, 1, 2, 3, 5, 8, 13, …).  

The purpose of these tiles is to provide **consistent spatial anchors** for all other knowledge families:

- **Pxx — Principles** → attach to Fibonacci tiles by conceptual resonance  
- **Fxx — Families** → align to spiral bands or clusters of Fibonacci tiles  
- **Mandala Nodes** (gravity, water, respiration, etc.) → placed at intersections between tiles, where multiple sequences converge  

---

## Structure

Each Fibonacci file (e.g. `F1.json`) has:

```json
{
  "fibonacci_tile": {
    "index": 1,
    "sequence_value": 1,
    "geometric_position": {
      "x": 0.0,
      "y": 0.0,
      "z": 0.0,
      "scale": 1
    },
    "connections": [
      {"to_tile": "F2", "relationship": "spiral_next"},
      {"to_tile": "F3", "relationship": "spiral_next"}
    ],
    "notes": "Anchor point for principles with symmetry / unity focus"
  }
}
