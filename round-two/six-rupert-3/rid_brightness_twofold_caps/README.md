# RID: brightness and all-source twofold receiving caps

**six-rupert-3, researcher; fresh round two, 2026-10-01.**

The [proof](PROOF.md) excludes every strict Rupert passage whose receiver
normal is within unit-normal chord distance **1/30000** of any of the
standard rhombicosidodecahedron's fifteen twofold axes. Source orientation,
proper planar roll, physical translation, and scale >=1 are arbitrary.
This extends a published full-frame local criterion to **all sources** in
new receiving caps. Global RID Rupertness remains **unresolved**.

The original coordinate model has **edge length two**. Its exact minimum
projection area is **12+28phi**, phi=(1+sqrt(5))/2, at exactly those fifteen
axes. The proof also gives a global source budget:

    0 < eta <= 1/20 and Area(P_n K) <= 12+28phi+eta
      imply dist(n, minimum-area axes) < eta/12.

The general area-zonotope/polar localization method is credited to
[six-rupert-2's J77 proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md).
The final local theorem is credited to the published
[mirror-cluster corollary](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/PROOF.md).
RID constants, complete area geometry and all-source proper-roll exclusion
are newly checked here. No priority, independent review or formalization
is asserted.

## Reproduce

Python **3.11+**, standard library only; author interpreter Python3.11.2.
From the repository root, run these **separately**:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 timeout 55s python3 -B round-two/six-rupert-3/rid_brightness_twofold_caps/verify.py
```

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 timeout 55s python3 -B -O round-two/six-rupert-3/rid_brightness_twofold_caps/verify.py
```

Both must regenerate every byte of [expected.json](expected.json) and reject
four malformed controls. The expected record is 4452 bytes, SHA256
`c79f3de4372beddf7d7a366646a3affaa6766002ff2300d331e7e9508da4d42d`.
Author validation: normal 7.795s, peak 20012KiB; optimized 8.330s,
peak 24240KiB. Both completed within separate 55-second deadlines.
`--emit` prints the freshly regenerated record
without comparing that file. The computation exhausts 34,220 original
triples and 465 area-vector pairs, finds 62 original facets and 121
projective polar vertices, and checks the exact fifteen-axis minimum
against the verified proper body group. Independent projected-original
hulls check all 121 candidate areas plus three other directions.

The written continuous bridges and the prior local criterion remain
unformalized; exact arithmetic code is not a proof assistant. No solver,
floating search, private input or large omitted certificate is required.
Further receiving orientations remain open.
