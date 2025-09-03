# Opinion-as-Vector (4D over P01–P12)

**Why**: Opinions drift in text. As vectors, they become positions in a 4D lattice:
- Invariance (P01–P03): form, quantity, frame
- Transformation (P04–P06): direction, innovation, dissipation
- Connectivity (P07–P09): content, exchange, structure
- Evolution (P10–P12): fit, continuity, resonance

**Files**
- `opinion_vector.schema.json` — validation schema (0–1 weights)
- `opinion_vector_example.json` — example stance encoding

**Conventions**
- Weights in `[0,1]`. Soft rule: each axis’ three weights sum ≤ 1.
- Add `meta.statement` (plain-English) and `interpretation` (generated).
- Use `provenance_sha256` if derived from raw notes.
- Commit message: `opinion(vX): short label (sha:XXXX)`

**Quick glyphs**
- ⚖ Invariance | 🔄 Transformation | 🕸 Connectivity | 🔮 Coherence/Evolution

**Compare opinions**
- Cosine similarity or L2 distance across the 12 weights.
- Axis summaries: sum or max per axis to see emphasis.
