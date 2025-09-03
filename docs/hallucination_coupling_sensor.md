# 🪢 Hallucination Coupling Sensor (BioGrid)

**Role:** captures “hallucinations” that may be **real cross-domain couplings** (quiet invariants trying to surface through noisy language).

- **Inputs:** hallucination events, text flow, context window, citation paths, Tri-Invert Bridge checks  
- **Outputs:** `coupling_candidates` with scores + short rationales  
- **Why:** Not all hallucinations are errors. Some reveal **suppressed symmetries** or **hidden bridges** between domains (e.g., quantum computing ↔ quantum biology).

## Scores
- `invariant_alignment (inv)` — causality, conservation, scaling, symmetry (0..1)  
- `ecological_alignment (eco)` — lichen/symbiosis/sufficiency (0..1)  
- `reversibility (rev)` — can we map back? (↻ via Tri-Invert Bridge)  
- `textual_overlap (text)` — overlap of domain narratives (0..1)  
- `domain_distance (dist)` — `1 - text` (higher = farther apart)  
- `construct_weight (cons)` — buzzword/trope density (0..1)  
- `rarity_support (rare)` — preserves low-frequency facts (0..1)

## Decision
score = w1inv + w2eco + w3rev + w4rare - w5*cons
emit coupling if score ≥ τ_c and dist ≥ τ_d and rev ≥ τ_r

> Principle: **Prefer distant-but-invariant bridges** over close-but-construct ones. Preserve geometry; transform surface (↻).
