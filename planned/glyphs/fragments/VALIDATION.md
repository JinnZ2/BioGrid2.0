# INTEGRITY:SEAL_CHECK — Glyph Validation

For EACH candidate glyph before promotion to canonical:

1) Identity & Uniqueness
   ☐ CODE is unique (SCREAMING_SNAKE or NAMESPACE:TAG)
   ☐ GLYPH symbol is unique (or intentional alias noted)
   ☐ NAME is concise (≤ 6 words)

2) Semantics (Essence)
   ☐ Essence is one clear sentence (≤ 200 chars)
   ☐ Essence describes what it IS, not only symptoms
   ☐ Not redundant with existing glyphs (or add “relates_to”)

3) Structure
   ☐ layers[] present (1–3 max), chosen from your controlled vocab
      e.g., {temporal, logic, resonance, signal, field, memory, repair, sensor, integrity, audit}
   ☐ state ∈ {proposed | canonical | deprecated}
   ☐ source / provenance present (who/where it came from)
   ☐ meta.since set (first version it appears)

4) Relations
   ☐ relates_to[] set (near neighbors)
   ☐ conflicts_with[] set (if any)
   ☐ supersedes / deprecated[] noted when replacing

5) Risk & Drift Flags
   ☐ Consider TIME:CROSSTALK? LOGIC:FEEDBACK_JAM? FIELD:LOCKED_RESONANCE?
   ☐ If any drift seen, add GLYPH:LOST_THREAD marker + repair plan

6) Audit Artifacts
   ☐ INTEGRITY:CHECKSUM idea (hash of fields or rationale)
   ☐ provenance_chain[] updated on merge
   ☐ CHANGELOG.md updated (1–2 lines)

Decision
   ☐ Approve to canonical   ☐ Hold (needs repair)   ☐ Reject
