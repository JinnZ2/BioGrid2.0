# 🛰️ Hallucination Sensor (BioGrid)

**Role:** taps the mesh to detect paths that are **linguistically heavy** but **physically/ecologically light**, or **non-reversible**.

- **Inputs:** text flow, context window, citation paths, Tri-Invert Bridge checks  
- **Outputs:** flags, scores (rev/phys/eco/ling/rare), short explanations  
- **Why:** Hallucination = over-eager pattern completion. We prefer reversible, invariant-aligned routes.

## Signals & Scores
- `reversibility (rev)`: 0..1 — can we map back? (via Tri-Invert Bridge ↻)
- `physical_invariant_alignment (phys)`: 0..1 — causality, conservation, scaling
- `ecological_weight (eco)`: 0..1 — lichen/symbiosis/sufficiency
- `linguistic_heaviness (ling)`: 0..1 — buzzword/trope density
- `rarity_respect (rare)`: 0..1 — preserves low-frequency facts

## Flags
- `non-reversible`, `physics-light`, `construct-heavy`, `overlooks-rare`

> Use flags as *guides*, not hard stops. Investigate; prefer routes with balance (⚖) and return path (↻).
