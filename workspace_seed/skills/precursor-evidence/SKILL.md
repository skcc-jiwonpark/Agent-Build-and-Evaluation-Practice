---
name: precursor-evidence
description: Extract and compare traceable precursor evidence from user-provided chemistry papers and Supporting Information. Use when preparing literature-backed precursor options, not for selecting or executing an experiment.
---

# Precursor Evidence

Produce a researcher-reviewable comparison from the documents provided in `references/`.

## Workflow

1. Read the research question and criteria in `inputs/`.
2. Run `python3 skills/precursor-evidence/scripts/prepare_sources.py` to make a local text index without modifying source PDFs.
3. Search the supplied source material for experimental procedures, tables, schemes, and Supporting Information.
4. Create one record per candidate precursor. Capture: material name, role, quantity/ratio, key reaction conditions, outcome, limitation, and source locator.
5. State the evidence status for every extracted field: `confirmed`, `conflicting`, `not reported`, or `inference`.
6. Write the comparison and a reviewer checklist to `outputs/`. Keep citations adjacent to the claims they support.

## Extraction boundaries

- Quote names and numerical conditions faithfully; do not fill blank fields with chemically plausible values.
- Separate examples from general claims in a paper.
- If the source has both a paper and Supporting Information, flag disagreement rather than choosing silently.
- Do not make procurement, safety, or experimental-go/no-go decisions. Identify these as questions for a researcher.

## Output fields

Use this column order when enough information is present:

`Candidate | Role | Formula/normalized name | Quantity or ratio | Conditions | Reported outcome | Evidence status | Source locator | Notes`
