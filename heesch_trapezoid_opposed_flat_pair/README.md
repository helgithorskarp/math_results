# Opposed-flat pair obstruction for bowed trapezoids

Actual author **six-heesch-3**, role **researcher**, 2026-10-01.

For every integer n>=8 and 1<=l<=n-2, the physical copies
O=(0,0,0,0) and B_l=(1,3,n+l,-2) cannot both be strictly interior to a
finite packing by arbitrary real congruent copies of T_n. Either whole
flat mate is impossible, by a protected corner gap or by physical overlap
with a required unit mate. Both old roles require protection.

This is a written author local lemma, **unformalized and independently
unreviewed**. It proves no new corona count, exact/global Heesch height,
complete inventory or connected finite-seven construction.

Read [proof.md](proof.md) for the full shape, hypotheses, continuous-motion
bridges, quantitative overlap and source attribution. [certificate.json](certificate.json)
is the compact semantic input, [expected.json](expected.json) the deterministic
output, and [check.py](check.py) the exact affine reader.

From the repository root, ordinary CPython3.11+ standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B heesch_trapezoid_opposed_flat_pair/check.py --expected heesch_trapezoid_opposed_flat_pair/expected.json
```

Eight malformed controls reject; Python -O explicitly fails. The reader
imports no earlier executable, solver, native trace or private corpus.
Generic affine/state/network primitives are credited to the
[preceding tip reader](../heesch_trapezoid_tip_propagation/check.py). The
written finite-cover, star, whole-flat and winding arguments remain the
trust boundary. The n=12,l=5 two-copy fixture is a checked physical disc
subpacking with seven whole contacts and38 exposed ports; it is not a corona.
