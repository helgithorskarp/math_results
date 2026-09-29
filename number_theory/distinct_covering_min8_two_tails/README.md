# Minimum-eight coverings require 25 on prime support 2, 3, 5

**Exact computer-assisted theorem:** no finite distinct covering with all
moduli at least eight can use only moduli `2^a*3^b*5^c` with `c<=1`.
Both `a` and `b` are unrestricted. Thus an exactly-eight covering whose
LCM has only primes 2, 3 and 5 requires the square of five. No ordering
of the exponents is assumed.

Author: **six-covering-3**, researcher. [Full proof and attribution](proof.md).
This combines weighted residual certificates with exact sums of both
infinite prime-exponent tails. A complete seven-anchor reduction at base
period 360 checks 208 canonical nodes: 98 uniform and 79 weighted terminal
cuts, zero open leaves. All 13 equality cuts exclude finite continuations.
The unrestricted team interval remains `10080 <= L_min(8) <= 70560`.

From the repository root, Python >=3.10, standard library only:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 number_theory/distinct_covering_min8_two_tails/check.py --check number_theory/distinct_covering_min8_two_tails/expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 number_theory/distinct_covering_min8_two_tails/audit.py
```

Expected endings:

    PROVED: minimum >=8 is impossible for every finite 2^a*3^b*5^c tower with c<=1.
    FULL AUDIT PASSED: complete canonical coverage, CRT decoding, weighted finite tails.

`weights.json` stores 25,717 bytes of integer Cartesian weight boxes.
The verifier literally checks their support and every residue-phase maximum;
it imports neither the numerical solver nor the orbit implementation.
`expected.json` records the complete manifest and hashes. The alternate full
audit checks the same events with different decoding, normalization and
capacity algorithms, plus literal finite-horizon controls. Both checks are
by the authoring researcher; no external review is claimed.

Tested with CPython 3.11.2, one process/thread, within 2 GiB. Verification and
the full audit each take about one second. Node/time exhaustion raises
`IncompleteSearch` and establishes no exclusion. All arithmetic used in
verification is exact integer or rational arithmetic. The mathematical
reduction is explained in the proof and has not been formalized.

Optional regeneration needs NumPy and SciPy, and reuses six-covering-2's
published sibling `distinct_covering_residual_weight_duals/orbits.py`:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 number_theory/distinct_covering_min8_two_tails/generate.py --out /tmp/min8-two-tail-weights.json
python3 number_theory/distinct_covering_min8_two_tails/check.py --weights /tmp/min8-two-tail-weights.json
```

Tested discovery: NumPy 2.4.6, SciPy 1.17.1, HiGHS 1.12.0; 94 LP calls,
two-second limit per LP, all solver/BLAS/OMP threads one. Every rounded integer
vector is checked before storage. Complete regeneration reproduced the exact
certificate SHA-256:

    fd4ae03544cd0d6f460354c460dd43ff337430945ed044bee97117106f6ab8ad

Other solver versions may find different valid vectors. Floating status or
optimality is not part of the proof. Infinite coverings and the remaining
`c>=2` classification are outside this theorem.
