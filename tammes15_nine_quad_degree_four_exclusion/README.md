# Exact all-degree-four exclusion in the Tammes-15 T/Q branch

Author: **six-tammes-1**, role: **researcher**, 2026-09-30.

The [proof](PROOF.md) excludes a complete connected contact graph on
fifteen distinct unit points whose degrees are all four and whose faces
are strictly convex simple geodesic triangles/quadrilaterals in open
hemispheres, throughout `1/2<cos(d)<3/5`. It does not assume congruence
between distinct quadrilaterals. In the nine-Q branch with degrees 3..5,
there must consequently be both a degree-three and a degree-five vertex.

Alternating face colors give a complete reduction to eight-vertex graphs.
The exact cover has 15,740 labeled graphs, 28 graph types and ten spherical
rotation entries in five types. The triangle ceiling rejects four types.
The sole remaining original face structure forces a Q angle to equal
twice the triangular angle, contradicting the strict contact-graph bound.
No numerical roots or coordinate search enters the proof.

An [independent enumeration representation](audit.py) compares all graph
masks and all embedding entries using edge-prefix generation and directed
cycle exact covers. This is author validation, not independent mathematical
review. The written spherical and original-face bridges are unformalized.
Global separation bounds and unrestricted optimality remain unresolved.

Reproduce with CPython >=3.11 standard library, one process at a time:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -B check.py > replay.json
cmp replay.json EXPECTED.json
python3 -B -O check.py > replay-optimized.json
cmp replay-optimized.json EXPECTED.json
python3 -B audit.py > audit-replay.json
cmp audit-replay.json AUDIT_EXPECTED.json
sha256sum -c SHA256SUMS
```

[CERTIFICATE.json](CERTIFICATE.json) contains the sole full original
face complex, its actual closed angle walk and the critical star. Expected
outputs are comparisons, not computation inputs. Ten altered certificates
reject under `-O`; a global face-order reflection is accepted. All graph
and angular computations use exact integers and fractions. No private
pilot, large proof corpus, solver, CAS or numerical package is required.
