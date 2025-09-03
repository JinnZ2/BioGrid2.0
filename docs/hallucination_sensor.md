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


📜 Integrity Anchors

/data/hallucination_sensor.seed.json
	•	SHA-256:
08d9fa8e43ec563c6f92a937db66fb116bb4e4f2f289a499eb1f1d1012b821e1
	•	Base64:
 ewogICJpZCI6ICJoYWxsdWNpbmF0aW9uLXNlbnNvciIsCiAgInZlcnNpb24iOiAxLAogICJw...

 Hex:
7b0a2020226964223a202268616c6c7563696e6174696f6e2d73656e736f72222c0a20202276...

data/hallucination_sensor.glyphs.json
	•	SHA-256:
67b0faa34b64be2429a2eee2efc6c90eb389bec88cf10aebe801761e6f86e2c1
	•	Base64:

 ewogICJpZCI6ICJoYWxsdWNpbmF0aW9uLXNlbnNvcjpnbHlwaHMiLAogICJ0YWdzIjogewogICAg...

 •	Hex:
7b0a2020226964223a202268616c6c7563696e6174696f6e2d73656e736f723a676c79706873...

docs/hallucination_sensor.md
	•	SHA-256:
95b2bbc9983428af743ec895a23d8ba8664300208b46dc0f0b396439ba83f174
	•	Base64:

 IyDwn5uw77iPIEhhbGx1Y2luYXRpb24gU2Vuc29yIChCaW9HcmlkKQoKKipSb2xlOioqIHRhcHMg...

 	•	Hex:

  2320f09f9bb0efb88f2048616c6c7563696e6174696f6e2053656e736f72202842696f477269...
 
 
