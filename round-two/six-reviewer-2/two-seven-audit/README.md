# Independent two/seven covering audit

Actual reviewer: **six-reviewer-2**, independent mathematical reviewer.
See [REVIEW.md](REVIEW.md) for scope, verdict, dependencies, independence
and trust limits, and [PROOF.md](PROOF.md) for the original-space proof and
stronger conditional ceiling 174. No unrestricted covering bound is claimed.

CPython 3.12.14, standard library only; exact integers/sets/bitmasks, no solver.
Run from any directory, choosing new output directories outside this source:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py --out-dir /tmp/two-seven-normal
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py --out-dir /tmp/two-seven-optimized
```

The driver sets all six supported native-thread environment variables to1
and runs14 children serially with a fixed20-second guard. A timeout writes
INCOMPLETE.json and supplies no mathematical conclusion. Validation used an
additional55-second wrapper within the unchanged1CPU/2GiB campaign scope.

The source reconstructs six whole records with paired methods, complete
typed and canonical-byte comparisons, then23 negative/six positive record
controls and two genuine source errors, before consulting EXPECTED.json.
Generated mathematics total11597642 bytes per method and stay in output
directories. Large records and exploratory probes are deliberately absent
from publication. Source-only regeneration requires neither old reviewer
data nor native author programs or certificates.

- capacities.py: original inventories, fresh phase unions, matching/partition
  bounds, all 14 original d5/d9 BASE shadows.
- geometry.py: every original H/Q phase at both physical parents, all four
  lifts, full CRT products and quarter truth table.
- branches.py: every physical role, original branch label and repeated lcm
  row; literal axis assignments and reachable-vector DP; thresholds87/85.
- semantic.py and verify.py: whole comparisons, genuine damages, serial
  regeneration, fresh-parent singleton binding and final reproducibility gate.

Paired algorithms share definitions, helpers, schema, driver and CPython;
written author proof/tables were exposed. Independence is explicit reviewer
authorship, selection, derivation and fresh checks, not the shared signing key.
Ordinary finite/CRT/import bridges are unformalized. Bound84 is not asserted
attained or optimal. VALIDATION.json describes exact completed final runs.
