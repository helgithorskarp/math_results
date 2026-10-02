# Full-interval small-diagonal obstruction at a five-contact point

six-tammes-1, researcher. Author-proved ordinary geometric lemma with
exact necessary-cover checks; independent review/formalization pending.

For1/2<c<3/5, a triangle made of the selected small-corner diagonals of
actual simple convex hemispherical quadrilateral contact faces cannot
contain a five-contact point. Other faces may be larger. The proof uses
a full-interval diagonal cosine bound below1/17 and two incompatible
angle budgets at the five. See [PROOF.md](PROOF.md).

In the original15-point nine-Q T/Q/degree3..5 class, the same32 necessary
count profiles extend from the old beta interval to the full open
interval. Delete four-four diagonal edges and retain a triangle-free H*
with unchanged required five degrees. Actual H-triangle-freeness above
beta is not asserted. Downstream beta-only proofs still require an audit.
No compatible sphere population, complete-nine-Q exclusion or global
numerical Tammes bound is claimed.

The programs take no external runtime input. CPython>=3.11/standard
library; audited with3.12.14. From this directory:

```sh
python3 -B check.py > replay.json
cmp replay.json EXPECTED.json
python3 -B -O check.py > replay-optimized.json
cmp replay-optimized.json EXPECTED.json
python3 -B audit.py > audit-replay.json
cmp audit-replay.json EXPECTED.json
python3 -B -O audit.py > audit-optimized.json
cmp audit-optimized.json EXPECTED.json
python3 -B check.py --entries > entries-check.json
python3 -B audit.py --entries > entries-audit.json
cmp entries-check.json entries-audit.json
```

All four summary outputs agree bytewise. Full-entry replay compares all
44 domains, including empty ones, rather than aggregate counts. Across
these separate necessary domains,333 H* masks and1533 three-neighbor
families are regenerated. Twelve control groups and all ten five-link
cases pass. Summary SHA256
`b981771908e1a95f223d0be0e72aae2c1f1c169d72ac86f4fde38b97ca07e66d`;
full-entry SHA256
`45593204afdc5bb0fd15f5b2f8244e4bc26a4c1a26aee2dae3704b5904e8fb35`.
Bulk entry output is regenerated locally and omitted from publication.

[VALIDATION.json](VALIDATION.json) records six sequential runs and the
explicit conservative memory measurement. [PRIOR_VALIDATION.json](PRIOR_VALIDATION.json)
records full comparisons with the pinned earlier count source;
[DEPENDENCIES.json](DEPENDENCIES.json) separates imported corollary
premises from citations. [MANIFEST.json](MANIFEST.json) records source
bytes. The written geometry and prior degree/all-four proofs remain
unformalized; separate same-author enumeration is not peer review.
