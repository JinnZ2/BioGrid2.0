# Legacy — The Run Record

**Legacy is not a graveyard. It is the experimental record, and precedence carries.**

A claim that was tested and found wrong is not worthless — it is a *completed
run*. It tells you what was believed, what was checked, what the check returned,
and what changed as a result. Delete it and you lose the only proof that the
work was ever tested at all. A framework with no falsification record is
indistinguishable from a framework that was never checked.

So this folder holds the runs. The banner on each file says what replaced it;
the [falsification log](./FALSIFICATION-LOG.md) says why.

## The cycle

```
   hypothesize ──▶ run ──▶ result
        ▲                    │
        │                    ▼
     rerun ◀── search    falsified?
        ▲     unknowns       │
        │         ▲          ▼
        └─────────┴──── edit the claim
```

Each stage has a home in this repository:

| Stage | Where it lives |
|---|---|
| **Hypothesize** | `docs/`, `planned/` — a claim, stated so it could be wrong |
| **Run** | `tests/`, `tools/lint_index.py`, source retrieval, field measurement |
| **Result** | `data/reference.figures.v0.1.json` — value, grade, source, `as_of` |
| **Falsified** | [`FALSIFICATION-LOG.md`](./FALSIFICATION-LOG.md) — what broke and how it was found |
| **Edit the claim** | `Technical-validation.md` §1 corrections; `retracted` block in the figures register |
| **Search unknowns** | `Technical-validation.md` §6 open questions; `planned/Experiments/VALIDITY.md` |
| **Rerun** | 6-month review cadence, plus event triggers when a source is superseded |
| **The old run** | `docs/legacy/` — kept verbatim, this folder |

The loop is the point. A retraction that doesn't open a new question is a
half-finished run.

## What "don't cite legacy" actually means

The earlier version of this policy said legacy files must never be cited as
evidence. That was too blunt, and it threw away the precedent. The real rule
has two halves:

- **Never cite a legacy file as evidence about the world.** Its figures are
  stale or wrong by definition — that is why it is here.
- **Always cite it as evidence about the reasoning.** "This was believed until
  2026-08, tested, and found wrong" is a load-bearing fact about how much to
  trust the current claims. Anyone auditing this project should read the
  falsification log first, because a project that logs its own errors is making
  a checkable claim about its own reliability.

Put concretely: you may not build a wall to a legacy R-value. You *should* cite
the legacy R-value when explaining why the current one is trustworthy.

## Outcome states

Not everything that ages is falsified. Distinguishing these matters, because
treating a stale number like a broken hypothesis discards work that actually
held up.

| State | Meaning | Where it goes |
|---|---|---|
| **FALSIFIED** | Claim was tested against evidence and is wrong | Legacy + log |
| **MISATTRIBUTED** | Claim may be true, but the cited source doesn't support it | Log; claim returns only if a real source is found |
| **STALE** | Was accurate, the world moved | Figure updated in place, `as_of` bumped; no retirement |
| **UNSOURCED** | Never had support in the first place | Log; restated as a hypothesis with a test method |
| **CORROBORATED** | Tested and held | Stays live, logged as a survived prediction |
| **SUPERSEDED** | Replaced by a better version of the same document | Legacy + banner |

A document only moves to this folder for **FALSIFIED** or **SUPERSEDED**. Stale
figures get refreshed where they live — moving them here would be hiding
maintenance behind a retirement.

## Register

| File | Retired | State | Superseded by | Reason |
|---|---|---|---|---|
| [`Technical-validation.v1.md`](./Technical-validation.v1.md) | 2026-08-14 | SUPERSEDED | [`docs/integration/Technical-validation.md`](../integration/Technical-validation.md) | 15 claims failed verification; no evidence grading, no retrieval dates |
| [`HISTORICAL.md`](./HISTORICAL.md) | 2026-08-14 | SUPERSEDED (register only) | [`src/biogrid/`](../../src/biogrid/) | Graduated-code manifest. Was filed in `planned/`, which its own `PLANNED.md` defines as future-only context — wrong direction in time. The code files themselves stay put; see the note in that file. |

## Retiring a document

```bash
git mv docs/<area>/<Name>.md docs/legacy/<Name>.v<N>.md
# 1. prepend the LEGACY banner naming its successor and the date
# 2. add a row to the register above
# 3. add the run to FALSIFICATION-LOG.md — including the unknowns it opened
# 4. write the successor, with its corrections section
# 5. update INDEX.md and CHANGELOG.md
python tools/lint_index.py --repo . --verbose
```

The body stays byte-for-byte identical apart from the banner, so the archive can
be diffed against its replacement. That diff is the result of the run.
