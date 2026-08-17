# Falsification Log

**Opened:** 2026-08-14 · **Cadence:** every 6 months, plus event triggers
**Policy:** [`README.md`](./README.md) · **Current claims:** [`Technical-validation.md`](../integration/Technical-validation.md)

Every completed run against a BioGrid claim, with what it returned. This is the
loop record: *hypothesize → run → result → edit the claim → search unknowns →
rerun.* Entries are never deleted, only continued.

Outcome states are defined in [`README.md`](./README.md#outcome-states):
**FALSIFIED** · **MISATTRIBUTED** · **STALE** · **UNSOURCED** · **CORROBORATED** · **SUPERSEDED**

---

## Run 001 — v1 evidence audit (2026-08-14)

**Hypothesis under test:** the claims in `Technical-validation.md` v1 are
supported by the sources it cites.

**Method:** every citation and figure re-checked against a primary source or a
first-party operator/regulator; 2024–2026 literature searched for each method.

**Result:** 15 of the document's load-bearing claims failed. Breakdown by state:

| # | Claim | State | Replacement |
|---|---|---|---|
| 1 | UPS ORION uses ACO | MISATTRIBUTED | ORION's public lineage is OR/genetic heuristics; the ~100M mi/yr saving is real, the ACO link is not sourced |
| 2 | "RFC 3626 — IEEE standard for ACO routing" | **FALSIFIED** | RFC 3626 is IETF OLSR, a link-state protocol. Correct ACO routing citations: AntNet, AntHocNet |
| 3 | Amazon warehouse routing uses ACO | UNSOURCED | No public source |
| 4 | Physarum shortest path is O(n log n) | **FALSIFIED** | No such bound. Bonifaci, Mehlhorn & Varma (2012) prove convergence; each step is a Laplacian solve |
| 5 | Slime mould outperformed Tokyo's rail designers | **FALSIFIED** | Tero et al. report *comparable* trade-offs on a benchmark layout, against a different objective |
| 6 | BioMASON acquired by Ginkgo Bioworks | **FALSIFIED** | Biomason is independent (~$132M raised, Series C Dec 2024) |
| 7 | Ecovative $100M+ valuation | UNSOURCED | Valuation not public; report funding (~$156M since 2019) |
| 8 | Solugen $2B valuation | STALE | $357M Series D at a reported ~$1.8B |
| 9 | Hempcrete R-2.5–3.0 per inch | **FALSIFIED** | λ≈0.06–0.09 W/m·K → **R≈1.6–2.4/inch** |
| 10 | Mycelium composites in commercial use by IKEA/Dell/Ford | STALE | 2011–2016 packaging pilots; 2025 reviews bound the material to non-structural use |
| 11 | Great Lakes = 20% of world's freshwater | **FALSIFIED** | 21% of world **surface** fresh water; wrong denominator |
| 12 | Internet: 5 billion users | STALE | ~6.0bn (ITU 2025) |
| 13 | Biomimicry has a $425B market | MISATTRIBUTED | A 2013 projection of US GDP *by 2030*, in 2013 dollars — not a measured market |
| 14 | $0.12/kWh vs $0.06–0.08/kWh | UNSOURCED | No model or assumptions. Restated as hypotheses H3/H5 |
| 15 | Kalundborg: 6+ facilities, €12M+ savings | STALE | ~17 partners; operator-reported ~586,000 t CO₂/yr (range 275k–635k) |

**Tally:** 6 FALSIFIED · 3 MISATTRIBUTED · 4 STALE · 2 UNSOURCED.

### What the pattern says

This is the most useful output of the run, and it is not any individual
correction.

**Eleven of fifteen failures trace to citing something other than the primary
source** — a press release, a summary article, a conference gloss. Only the
stale figures (4) are ordinary ageing. The rest are provenance failures that
were checkable on the day they were written.

Two consequences follow, and they are actionable:

1. **The dominant failure mode is citation discipline, not research depth.**
   More reading would not have prevented these; *reading the thing being cited*
   would have. Hence the `source` + `as_of` requirement on every row of
   `data/reference.figures.v0.1.json`, and grade C explicitly meaning "trade
   press — never load-bearing."
2. **Every error ran in the same direction** — toward the framework being
   righter than the evidence supported. A random error process would scatter.
   Directional error means the filter was motivated, not noisy, which is why
   the corrections are kept visible rather than absorbed silently.

### Consequence ranking

Most errors were rhetorical. One was physical:

- **#9 (hempcrete R-value)** is the only failure that would have damaged
  something real. A wall built to R-3.0/inch using a material that delivers
  ~R-2.0 under-insulates by roughly a third, in a heating climate, in
  buildings meant to last decades. Everything else cost credibility.
- **#2, #4** would have misled an implementer into choosing the wrong algorithm
  or expecting a performance bound that does not exist.
- **#1, #3, #5, #6, #13** cost credibility only — the kind of error a hostile
  reader finds first.

### Unknowns opened

Each retraction left a question behind. These are live:

| U# | Unknown | From | Status |
|---|---|---|---|
| U1 | What *is* the right decentralised routing method for a disruption-heavy bioregional network, benchmarked honestly against OR-Tools? | #1, #2, #3 | Open — see `METHODS.md` §1 interface contract, and H6 |
| U2 | At measured R≈2.0/inch, does hemp-lime still win on total wall cost at equal U-value once thickness rises? | #9 | Open — H3 |
| U3 | Which Kalundborg CO₂ methodology fits a Great Lakes cluster's system boundary? | #15 | Open — the 275k–635k spread is a boundary-definition problem, not a measurement error |
| U4 | Is there any documented case of the *full* BioGrid combination (symbiosis + islanded DER + local bio-materials + decentralised logistics) in one bioregion? | whole-document | Open — none found in this run. This is the framework's central untested claim |
| U5 | What structural role, if any, can mycelium composites take with standardised test methods once those exist? | #10 | Watch — blocked on standards work |

**U4 is the important one.** Each leg has evidence; the integration has never
been built. That is the actual hypothesis BioGrid is making.

### Rerun triggers

- **Scheduled:** 2027-02 — re-verify every figure in `Technical-validation.md` §4.
- **Event:** a cited standard, regulation, or price series is superseded
  (2024 IRC adoption by a target jurisdiction; Lazard LCOE+ annual release;
  EU Circular Economy Act publication; NREL ATB release; EU AI Act Art. 50
  enforcement).
- **Failure condition:** any figure that cannot be re-verified at review drops
  to grade D and leaves the register. Silent survival is not permitted.

---

## Run 002 — The Line failure analysis (2026-08-14)

**Hypothesis under test:** `Resilience/The-line-redesign.md` (dated Nov 2024)
asserts that The Line fails because it accelerates continuously against natural
process rates and physical constraints, and predicts continued schedule and
scope collapse.

**Method:** re-checked project status against 2026 reporting.

**Result: CORROBORATED, figures STALE.**

The directional prediction held. What moved were the numbers:

| Claim as written (Nov 2024) | Status 2026-08 |
|---|---|
| "Mostly halted, scaled back to 2.4km" | Construction suspended Sept 2025 after ~2.4km of foundation; major work paused until after 2030 |
| "Timeline pushed to 2070s–2080s" | 2045 now cited as a possible full-completion date; NEOM restructured around industrial, energy, and AI uses |
| "9 million residents" (original vision) | Fewer than 300,000 expected by end of decade |
| Cost escalation | ~$16bn in reported termination and cancellation costs on suspended contracts |

**Disposition:** the document **stays live**. Its premise was tested by events
and survived; only its figures aged, which per the policy is a refresh, not a
retirement. A dated status addendum was added rather than a rewrite, so the
original prediction and its outcome are both readable.

**Why this entry matters:** a falsification log that only records failures is
itself a biased sample. A framework that logs its errors but not its survived
predictions cannot show whether it is improving. This is the first corroborated
run.

**Rerun trigger:** any NEOM restructuring announcement, or 2030.

---

## Pending runs

Predictions with test methods, awaiting execution. Full statements in
[`Technical-validation.md`](../integration/Technical-validation.md) §6.

| ID | Prediction | Blocked on |
|---|---|---|
| H1 | Biomass CHP + on-site load cuts purchased energy ≥50% | A pilot site and a metered baseline year |
| H2 | Bioregional sourcing cuts inbound tonne-km ≥70% | Procurement records |
| H3 | Hemp-lime modular ≥30% cheaper at equal thermal performance | Bid-level costing at matched U-value — **carries U2** |
| H4 | 3–5 facility cluster holds 90% uptime through regional disruption | Cluster existing |
| H5 | Data-centre waste-heat coupling delivers heat at competitive cost | Comparable against the Finnish/Danish reference projects |
| H6 | Decentralised routing degrades more gracefully than centralised OR under progressive link loss | **Runnable now in simulation — carries U1, no field site needed** |

**H6 is the cheapest open run in the repository.** It needs a simulation
harness and an OR baseline, not a building. It is the obvious next experiment.

---

## Log format

```markdown
## Run NNN — <what was tested> (YYYY-MM-DD)
**Hypothesis under test:** the claim, stated so it could fail
**Method:** how it was checked
**Result:** state + what changed
**Unknowns opened:** what the result made newly answerable-but-unanswered
**Rerun trigger:** scheduled date, or the event that invalidates the result
```

Entries are appended, never edited. A correction to a run is a new run citing
the old one.
