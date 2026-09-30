# Exact exclusion of the conditional Tammes-15 eight-Q branch

Author: **six-tammes-1**, role: **researcher**, 2026-09-30.

The [proof](PROOF.md) excludes a complete connected simple strictly convex
cellular sphere contact graph on fifteen points with degree pattern `(5^2,4^13)`
and two ordinary fives (four T faces, one Q each), throughout
`1/2<cos(d)<3/5`. Faces are simple geodesic triangles T and quadrilaterals
Q in open hemispheres. The preceding degree-pattern theorem supplies
these hypotheses in the degree3..5, eight-Q branch with `1/2<c<beta`.
Thus **the entire conditional eight-Q/beta branch is excluded**.

This closes the previously remaining two profiles and eleven necessary
H types in that branch. It does not assert a global Tammes-15 upper-bound
improvement or coverage of arbitrary optimal contact graphs. Larger faces,
nine or more Qs and independent mathematical review remain open.

The reduction uses disjoint **original** fan points and retains all
possible opposite aliases in its initial finite cover. A self-contained
integer/Fraction audit checks 5,875 necessary assignments, one surviving
full face/role orbit with 24 labelings, both signs in each metric seed
cover and three strict forbidden-pair certificates. No graph mask is
used as a coordinate identity. At most fourteen original positions
need be constructed; other required face equations are not assumed
to hold identically for every parameter.

Reproduce with CPython 3.11+ standard library, one process:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -B check.py > replay.json
cmp replay.json EXPECTED.json
python3 -B -O check.py > replay-optimized.json
cmp replay-optimized.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Ten invalid-certificate controls remain active under `-O`. The original
face cover, forced Q-sector order, equal corner angles and half-turn
interpretation are written proof bridges, not proof-assistant formalization.
Shared arithmetic kernels are not an independent full arithmetic audit.
