> [!NOTE]
> **LEGACY REGISTER — relocated 2026-08-14.**
> This file was in `planned/`, but [`planned/PLANNED.md`](../../planned/PLANNED.md)
> defines that folder as *"read-only future context"* on a draft→release path.
> A record of code that has already graduated points the other way in time, so
> the register now lives here. See [`README.md`](./README.md).
>
> **The code files themselves have not moved.** They stay at `planned/glyphs/`
> and `planned/sensors/` because their sibling `INDEX.md` files use relative
> paths, nothing imports them, and they already carry the "Do Not Edit" marking
> below. They are legacy *by reference* — precedence intact, location unchanged.
> Relocating them is a live option if the churn is ever worth it.

---

# Historical Source — Do Not Edit

The Python code in `planned/glyphs/` and `planned/sensors/` has been
**graduated into the installable package** at `src/biogrid/`.

These files are preserved as historical record of the original implementations.
All new development, bug fixes, and extensions should happen in `src/biogrid/`.

## Mapping

| Original (planned/) | Graduated (src/biogrid/) |
|---------------------|--------------------------|
| `glyphs/Collector_script.py` | `glyphs/collector.py` |
| `glyphs/diff_viewer.py` | `glyphs/diff_viewer.py` |
| `glyphs/glyph_append_cli.py` | `glyphs/append_cli.py` |
| `glyphs/fragments/auto_validator.py` | `glyphs/validator.py` |
| `glyphs/registry/scripts/auto_validator.py` | `glyphs/validator.py` (merged) |
| `glyphs/scripts/merge_registry.py` | `glyphs/merge.py` |
| `glyphs/registry/scripts/list_checksums.py` | (folded into `validator.py --write`) |
| `sensors/AI/AI/__init__.py` | `sensors/__init__.py` |
| `sensors/AI/analyze.py` | `sensors/analyze_cli.py` |
| `sensors/AI/AI/adversarial_pattern_detector.py` | `sensors/adversarial_pattern_detector.py` |
| `sensors/AI/AI/consistency_guard.py` | `sensors/consistency_guard.py` |
| `sensors/AI/AI/contradiction_graph.py` | `sensors/contradiction_graph.py` |
| `sensors/AI/AI/gaslight_index.py` | `sensors/gaslight_index.py` |
| `sensors/AI/AI/prompt_pressure_meter.py` | `sensors/prompt_pressure_meter.py` |
| `sensors/AI/AI/provenance_stamp.py` | `sensors/provenance_stamp.py` |
| `sensors/AI/AI/uncertainty_calibrator.py` | `sensors/uncertainty_calibrator.py` |
| `sensors/AI/AI/self_assessment.py` | `sensors/self_assessment.py` |
| `sensors/AI/AI/continuity/tools/mint_capsule.py` | `sensors/continuity/mint_capsule.py` |
| `sensors/AI/AI/continuity/tools/validate_capsules.py` | `sensors/continuity/validate_capsules.py` |

## Still in planned/ only (not yet graduated)

- `planned/Experiments/` — fractal, quantum, acoustic research
- `planned/Quantum/` — quantum exploration
- `planned/capsules/` — capsule schema definitions
