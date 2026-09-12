# Handoff and replay

## Required input

Use the complete order-24 `(4,5)` graph6 catalogue `r45_24.g6` from Brendan
McKay's Ramsey graph data page.  Required properties:

```text
records: 352366
SHA256: 83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0
```

## Environment

Python 3.11 was used with the pinned packages in `requirements.txt`.
Proof checking used `drat-trim`; proof production used CaDiCaL 1.9.5.

## Certificate verification

```bash
python verify.py \
  --catalog /absolute/path/r45_24.g6 \
  --drat-trim /absolute/path/drat-trim
```

This reconstructs every literal closure trace, every exact endpoint formula,
checks each stored core is contained in its formula, and verifies all 52
trimmed DRAT proofs.

## Full catalogue replay

```bash
python reproduce.py \
  --catalog /absolute/path/r45_24.g6 \
  --drat-trim /absolute/path/drat-trim
```

This additionally rebuilds `COARSE.json`, `PHYSICAL.json`, `CLOSURE.json`,
and `CT.json` from the original catalogue and compares all mathematical
fields with the committed certificates.

## Reproducing solver proofs

`run_sat_branches.py` regenerates all 52 full formulas, invokes CaDiCaL,
trims and rechecks the proofs, and emits `BRANCH_PROOFS.json`.  Its required
arguments are shown by `--help`.  No SAT or UNKNOWN branch is acceptable.

Do not interpret an individual physical residual as a candidate good43.
Only a satisfying assignment of a complete endpoint formula, independently
checked over all five-subsets, would be such a candidate; none exists here.
