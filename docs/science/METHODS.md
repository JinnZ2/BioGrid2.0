# Method Register (2026)

**Compiled:** 2026-08-14 · **Review cadence:** 6 months · **Next review:** 2027-02
**Companions:** [`Technical-validation.md`](../integration/Technical-validation.md) (evidence) · [`REFERENCES.md`](./REFERENCES.md) (sources)

This register answers one question per subsystem: **what method would a
competent engineer choose for this today, and what does BioGrid currently do?**
It is deliberately separate from the evidence document — evidence ages on its
own schedule, methods age faster.

Status vocabulary:

| Status | Meaning |
|---|---|
| **ADOPT** | Current best practice. Use it; deviations need justification. |
| **KEEP** | Still appropriate for BioGrid's constraints even if not the raw-performance leader. |
| **BOUND** | Usable strictly inside stated limits. Outside them it is wrong, not merely suboptimal. |
| **WATCH** | Promising, not deployable. Simulation and prototyping only. |
| **RETIRE** | Superseded, unsupported, or based on a corrected claim. Move to `docs/legacy/`. |

---

## 1. Routing, logistics, and network topology

| Method | Status | Notes |
|---|---|---|
| Ant Colony Optimization (classical) | **KEEP** (as one option behind an interface) | Structural fit — decentralised, anytime, disruption-tolerant, no retraining — is why it stays. Raw solution quality is no longer its selling point. |
| Hybrid neural-ACO (e.g. GNN-predicted heuristics, GFlowNet ant sampling, MoE ant sampling) | **ADOPT** for offline planning | Current research direction: learn the heuristic measure, keep the ant construction. Requires training data and a GPU; not for edge nodes. |
| Strong OR solvers (OR-Tools and equivalents) | **ADOPT** as the mandatory baseline | Any BioGrid routing claim must be benchmarked against a competent OR baseline or it means nothing. |
| Physarum solver as a *shortest-path algorithm* | **RETIRE** | Converges (Bonifaci et al. 2012) but slowly, with a linear solve per iteration. Better solvers exist for this job. |
| Physarum as a *topology objective* | **ADOPT** | Simultaneous minimisation of total conduit length, flow-weighted transport cost, and fault intolerance — the Tero et al. trade-off surface. This is the durable contribution. |
| Live-organism computation | **WATCH** | Hours-to-days runtime under strict environmental control. Research and outreach value only. |

**Interface contract for `swarm/` agents.** Target this, not an algorithm:

```
route(demand_graph, capacity, failed_edges, deadline) -> plan
  MUST return a feasible plan before `deadline` (anytime).
  MUST degrade to a feasible-if-suboptimal plan when the coordinator is unreachable.
  MUST accept edge removals mid-solve without restart.
  SHOULD be benchmarked against an OR baseline on the same instance.
```

Any solver meeting that contract is a legal implementation. This is the
concrete form of "treat the optimiser as swappable".

---

## 2. Energy system architecture

| Method | Status | Notes |
|---|---|---|
| IEEE 1547-2018 DER interconnection | **ADOPT** | The baseline. Ride-through, voltage/frequency support, and DER categories are the vocabulary the "mycelial" layer should be written in. |
| Grid-forming inverters | **ADOPT** | The mechanism behind islanding and black start without spinning mass. Mainstream standards and validation work as of 2025–26. |
| Microgrid islanding + hierarchical dispatch | **ADOPT** | This *is* the "dual neural-mycelial grid", in engineering language. |
| Digital twins (with power-hardware-in-the-loop) | **ADOPT** for validation | Already operational engineering practice, unlike graph RL. The right home for BioGrid's simulation ambitions. |
| Graph reinforcement learning for topology control | **WATCH** | Its own survey literature calls it proof-of-concept, sim-to-real gap unresolved. Simulate freely; never claim operation. |
| Byzantine-fault-tolerant consensus for control | **BOUND** | Correct for ledger/state agreement among untrusted nodes. Not a substitute for protection relays or interconnection compliance — different timescales, different failure model. |

---

## 3. Materials and process

| Method | Status | Bound / note |
|---|---|---|
| Hemp-lime (hempcrete) wall infill | **BOUND** | 2024 IRC Appendix BL: **non-structural infill**, ≤2 storeys, low-seismic, prescriptive; otherwise engineered design. Appendix must be adopted by the jurisdiction. Design to λ≈0.06–0.09 W/m·K → **R≈1.6–2.4/inch**. |
| Mycelium-bound composites | **BOUND** | Semi-structural and non-structural only: packaging, panels, insulation, furniture. Open problems: water absorption, weathering, no standardised test methods. |
| Bioleaching — copper, refractory gold | **ADOPT** | Commercially mature. |
| Bioleaching — REEs, e-waste | **WATCH** → pilot | Pilot/demonstration scale; engineered consortia and synthetic biology improving selectivity and acid tolerance. Phase 2/3 demonstration, not a Phase 1 supply assumption. |
| Waste-heat → district heating | **ADOPT** | Deployed at hundreds of MW thermal, and now legally mandated in parts of the EU. Highest-confidence first coupling for a Great Lakes cluster. |
| Industrial symbiosis (Kalundborg model) | **ADOPT** | Six decades of operating data; EU policy actively building the secondary-materials market. |

---

## 4. AI sensing, calibration, and evaluation

This section applies to `src/biogrid/sensors/` and `src/biogrid/shield/`.

| Method | Status | Where it lands in this repo |
|---|---|---|
| Semantic entropy for confabulation detection (Farquhar et al., *Nature*, 2024) | **ADOPT** as the reference method | The published, ground-truth-free way to estimate whether a generation is confabulated. `uncertainty_calibrator.py` currently implements a heuristic risk discount with no entropy estimate. |
| Semantic entropy probes (hidden-state approximation) | **WATCH** | Near-zero overhead approximation. Needs model internals — only viable where BioGrid runs the model, not behind an API. |
| Calibration metrics: ECE, Brier score, reliability diagrams | **ADOPT** | `calibrate()` returns a number nothing ever scores. A calibrator without a calibration metric is an assertion. Adding Brier/ECE over a labelled turn log is the smallest honest improvement available to this package. |
| Published deception/honesty benchmarks (MASK, in-context scheming evals, deception taxonomies) | **ADOPT** as external validation | `gaslight_index.py`, `adversarial_pattern_detector.py`, and `logic_shield.py` currently validate against internal fixtures only. External benchmarks turn "we detect manipulation" into a measured claim. |
| Regex/pattern pressure detection (`prompt_pressure_meter.py`) | **KEEP** | Cheap, transparent, extensible via `register_pattern()`, and no API dependency — real virtues for an offline-capable design. Bound: it detects *surface form*, not intent, and will not survive paraphrase. Say so in the docs. |
| EMA-baseline anomaly detection (`logic_shield.py`, `guard.py`) | **KEEP** | Appropriate for streaming multi-turn analysis with no training set. |
| Provenance stamping (`provenance_stamp.py`) | **KEEP**, review against EU AI Act Art. 50 | Article 50 content-marking/labelling obligations apply from 2 Aug 2026. Worth checking the stamp format against what that regime expects, even though BioGrid is not a GPAI provider. |
| M(S) coherence metric (`hgai.py`) | **KEEP** as project-internal | A framework-internal construct, not an external scientific claim, and should not be presented as one. Grade it as design, not evidence. |

### Concrete, bounded improvements to the sensors package

Ranked by ratio of honesty gained to work required:

1. **Add calibration scoring.** Compute Brier score and expected calibration
   error over a labelled turn log; expose from `uncertainty_calibrator.py`.
   Small, testable, and it makes every downstream confidence number auditable.
2. **Document the surface-form limit.** State plainly in the sensor docs that
   pattern detection is lexical and defeated by paraphrase. Users who know the
   limit can compensate; users who don't will over-trust it.
3. **Add an external-benchmark harness.** Run `LogicShield` against a public
   honesty/deception benchmark and publish the numbers, good or bad.
4. **Optional semantic-entropy backend.** Where BioGrid controls the model,
   estimate semantic entropy over sampled generations and feed it into
   `calibrate()` instead of the heuristic risk discount.

None of these change the framework's philosophy. They change whether its claims
can be checked, which is the same standard §1 of the evidence document applies
to the infrastructure side.

---

## 5. Retired from the method set

| Method / claim | Reason | Where it went |
|---|---|---|
| "ACO as deployed industry standard (UPS/Amazon/RFC 3626)" | Attributions were wrong; RFC 3626 is IETF OLSR, not ACO | [`Technical-validation.md`](../integration/Technical-validation.md) §1 |
| Physarum solver with "O(n log n)" complexity | No such bound; correct citation is Bonifaci et al. 2012 | §1 item 4 |
| Hempcrete R-2.5–3.0/inch | Contradicted by measured λ | §1 item 9 |
| "Structural mycelium composites" | Review literature: semi/non-structural only | §1 item 10 |
| Undocumented LCOE comparison | No model, no assumptions | §1 item 14; restated as hypothesis H3/H5 |
| "Foofoo rebuttal" rhetorical framing | Argues with critics instead of grading evidence; the grades do the work now | Removed in v2; original preserved in `docs/legacy/` |
