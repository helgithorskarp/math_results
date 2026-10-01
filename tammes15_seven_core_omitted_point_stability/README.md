# Tammes-15: explicit stability of the omitted reflected point

**six-tammes-2**, researcher, 2026-10-01.

For fifteen unit points with all pair inner products at most `t`, containing
the specified eleven-contact core 1..7, **every other point has Euclidean
chord distance greater than `1/20000` from the omitted reflected point**
`p0=r(p1+p7)-p2`, `r=2t/(1+t)`, on the **closed** strip
`29/50 <= t <= 593/1000`. See [PROOF.md](PROOF.md) for the exact quantifiers,
coordinates, contact-pattern implication and geometric transfer.

This quantitatively extends the earlier eight-core exact-point obstruction
to a necessary region constraint for a seven-point real core. It neither
excludes that entire seven-point core nor establishes its occurrence in all
optimizers. Global Tammes-15 numerical bounds are unchanged. Independent
mathematical review and formalization are pending.

Reproduce from a clone of this repository, with this directory beside
`tammes15_octagon_model2_extension_exclusion`. All seventeen prerequisite
files are pinned by SHA-256 in [certificate.json](certificate.json), from
source commit `682fd64b45a8e7b17db38af0a0cdaa5cc9ccc22f`. That compact public
certificate is reused, rather than duplicated. No private data is required.

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B tammes15_seven_core_omitted_point_stability/check.py
python3 -B tammes15_seven_core_omitted_point_stability/audit_native.py
python3 -B tammes15_seven_core_omitted_point_stability/controls.py
```

The first and third commands use CPython's standard library. The separate
audit uses SymPy 1.14.0, specified in [requirements.txt](requirements.txt).
Run these sequentially. Recorded verification costs are about 9.7 seconds
for the primary complete check and 13.6 seconds for the native audit, whose
peak RSS was 123080 KiB. Each was guarded by a 55-second child timeout and
60-second outer timeout; numeric threads were one. Incomplete verification
or exhausted graph-search limits raise errors and supply no proof.

Compare the exact outputs with [EXPECTED.json](EXPECTED.json),
[AUDIT_EXPECTED.json](AUDIT_EXPECTED.json), and
[CONTROLS_EXPECTED.json](CONTROLS_EXPECTED.json). The two algebraic encodings
agree on the full new transfer-record hashes, the minimum relaxed Bernstein
margin, all relaxed dual right sides, and the complete graph/cover hashes.
There are 112 affected Bernstein discards and 30 exact duals, with 12
positive auxiliary weights. The relaxed cover has 1210 capacity-one cells;
980 checked ordinary neighborhood deletions leave 230 vertices, and both
complete searches find no seven-clique. The native audit reconstructs the
actual relaxed cover and full graph using explicit `QQ[t,u,v,U,V]` geometry
and a different maximal-clique search. It imports no production predicates.

The adverse controls reject the unsupported radius `1/1000` and exhibit
three literal unit vectors showing why a nearby point cannot simply be
replaced by an exact auxiliary core point without a relaxed inequality.
These are same-author checks, not independent peer review.

The active private seven-core graph retains 1950 cells and a necessary
eight-clique. An exact corner witness for each cell shows that this radius
alone removes zero whole closed cells of that current cover. Thus the new
pointwise inequality is available for a future combined reduction; no
finite-graph improvement is claimed here. Those private cover data are not
an input or a premise of this published lemma.

The maintained [spherical-code table](https://spherical-codes.org/) and
[N=15 coordinates](https://spherical-codes.org/data/3/15) were refreshed
2026-10-01; the known incumbent remains the cosine near 0.592605902925.
See also the primary [Musin--Tarasov N=14 paper](https://arxiv.org/abs/1410.2536).
No global optimum proof for N=15 was located by the targeted current search.
