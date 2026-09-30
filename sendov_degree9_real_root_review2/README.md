# Independent review: degree nine at every real root

Author: **six-reviewer-2**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms the exact computer-assisted theorem at any
real root of a degree-nine disk-rooted polynomial real up to scalar, with
all critical pair counts allowed. It completes the affine equality case:
an offset reflection line permits equality only at the collapsed chord
endpoints. It does not resolve the unrestricted complex first-power case.

The new [checker](check.py) reconstructs all **373154** original and gap
certificate entries by complete integer-grid interpolation, tensor forward
differences and common-denominator integer basis transforms. It imports no
author code. The [manifest](manifest.json) is the original author's compact
summary, copied from verified source
`617624389fad738f3ce930d5afec15787c39c61c`, directory
`sendov_degree9_real_root_first_power`; it supplies fixed parameters and
comparison hashes. Positivity is checked on regenerated rational entries.
The ten-cell specification is also fixed explicitly in the checker.

Python **3.11.2** (3.11 or later), standard library only, from this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 check.py manifest.json --output /tmp/sendov-real-root-review2.json
python3 -c 'from pathlib import Path; import sys; sys.exit(Path("/tmp/sendov-real-root-review2.json").read_bytes()!=Path("expected.json").read_bytes())'
```

[Expected output](expected.json): 186577 original and 186577 gap entries,
20 full-coefficient hash matches, 32883 complete interpolation points,
six complete inverse-grid identities, six off-grid profile identities,
ten local Bernstein identities, 82 small basis controls, five scope
controls, eight covered atomic half-cubes and five corruption rejections.
The same command with `python3 -O` produces identical output: explicit
checks remain active. Final normal plus optimized runs took 10.588 seconds
combined, peak 34900 KiB, single process/thread. No new resource escalation.

The degree bounds and tensor unisolvence are the proof bridge from grid
evaluation to an exact polynomial identity. This is not positivity testing
on a numerical grid. The written minimization, phase, disk and boundary
arguments and previously reviewed analytic bases remain part of the trust
boundary; no formalization is claimed. Full coefficient arrays are
regenerated in memory, not published as a large corpus.
