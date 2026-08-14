# Legacy Archive

Documents that have been **superseded** but are kept verbatim for provenance.

BioGrid 2.0 makes empirical claims about physical infrastructure. Claims decay:
prices move, companies fold or get acquired, standards get revised, and some
citations turn out to have been wrong the day they were written. Deleting a
retired claim hides the fact that it was ever made. Rewriting it in place hides
what changed. So retired material moves here, unedited except for a banner at
the top pointing at whatever replaced it.

## Policy

1. **Nothing is deleted.** A document that is no longer accurate moves to
   `docs/legacy/` with a `LEGACY` banner naming its successor and the date it
   was retired.
2. **The banner is the only edit.** The body stays byte-for-byte as it was, so
   the archive can be diffed against the replacement.
3. **The successor carries the correction list.** Whoever writes the replacement
   is responsible for an explicit "what changed and why" section — a claim that
   was retracted must say so, not simply vanish.
4. **Legacy files are not linked as evidence.** They stay out of `INDEX.md`'s
   live sections and must not be cited as support for a design decision.
5. **Versioned filenames.** `Name.v1.md`, `Name.v2.md`, … so the lineage is
   readable from `ls`.

## Contents

| File | Retired | Superseded by | Reason |
|---|---|---|---|
| [`Technical-validation.v1.md`](./Technical-validation.v1.md) | 2026-08-14 | [`docs/integration/Technical-validation.md`](../integration/Technical-validation.md) | Stale figures (2019–2023 vintage), several unverifiable or incorrect attributions, no evidence grading, no retrieval dates |

## Retiring a document

```bash
git mv docs/<area>/<Name>.md docs/legacy/<Name>.v<N>.md
# prepend the LEGACY banner
# add a row to the table above
# write the successor, including its corrections section
# update INDEX.md and CHANGELOG.md
python tools/lint_index.py --repo . --verbose
```
