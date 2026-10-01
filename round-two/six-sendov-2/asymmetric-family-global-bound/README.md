# Sharp bound on the full asymmetric3+3+1+1 angular family

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary author proof; unformalized, independent review pending.

The entire balanced original-slope family with two triple blocks and
two singletons has sharp angular ratio constant
`c3 in(24.53389668,24.53389670)`. Equality is exactly the4+3+1 orbit
from [the sharp three-level theorem](../angular-three-level-transition/PROOF.md),
source6efce877eb9dcde6e12b6a90930d65382b29dd89, graph8753.

This is a global theorem on that full two-parameter family, including
asymmetry and collisions. Every genuinely four-level profile has
strictly smaller ratio. Other multiplicity patterns and the full
all-sphere maximum are not settled. The first-power endpoint remains open.
[PROOF.md](PROOF.md) gives the statement, dependency and complete proof;
[LITERATURE.md](LITERATURE.md) gives problem status and prior-art credit.

## Reproduction

CPython3.11.2 was used; Python3.11+ standard library, no CAS or solver.
Run in this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 python3 -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 python3 -B -O verify.py
```

Expected:24 exact records,4 damage controls, recordSHA256
`9cc80dcdb8aee82f7e48f3c1439bcd49f799ba126cfb22c31b5e3cf20ceaa376`.
Elapsed time in the summary is descriptive and not part of the fixture.

The checker independently derives the moment/Gram formula, computes
one17x17 and two15x15 integer-polynomial determinants by Bareiss,
verifies the full degree59 factorization, and bounds every admissible
stationary branch using exact gcd, Sturm and rational intervals.
The source contains the compact rational root intervals; their counts
and exhaustion are checked. Analytic spectral and compactness arguments
remain ordinary written mathematics. No external proof corpus is required.
`--expected PATH` supports independent fixture corruption checks;
`--write-expected` regenerates the compact regression record only.
