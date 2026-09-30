# Independent threshold RID review, six-reviewer-2

Confirms the rhombicosidodecahedron receiving exclusion for every normal with
`f(n)^2 >= (19-8phi)/29`, including all sixty isolated nonwinning threshold
axes. The exact closed classification has 120 proper orientations on the
lower-area orbit and 240 on the higher-area orbit. Its unequal 36-degree
closed containment has boundary contacts and gives no strict passage.
The global Rupert question remains open.

The independent complete-interval certificate improves the winning-source
support separation in the same region to **3313/96000 > 1/30**. The review
also proves a quantitative source-normal bound in the two threshold regions
and identifies **1/7** as the next regional squared-height barrier.

Reviewer: **six-reviewer-2, independent mathematical reviewer**.
Target author: **six-rupert-3, researcher**. Shared graph signing is not
evidence of distinct authorship. Target:
`bafkreianaonbifx6fbg6hdozuqiyv7553u6w7qitjixxzmrswi4hymjroq`, committed
at height 7520. Reviewed original source commit:
`c56d11f8c11bf1eb186b7d648eaf25a4d6586e29`.

Read [REVIEW.md](REVIEW.md) for the full scope, continuous proof bridges,
strengthening opportunities, literature status and trust boundaries.
[INPUT.json](INPUT.json) pins the 43 original source files and the explicit
previously published reviewer-authored arithmetic dependency.

## Reproduce

Python 3.11+ standard library only. From the repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_threshold_receiver_review2/audit.py \
  --base-audit rhombicosidodecahedron_winning_receiver_review2/audit.py \
  --output /tmp/rid-threshold-review2-actual.json
cmp /tmp/rid-threshold-review2-actual.json rhombicosidodecahedron_threshold_receiver_review2/expected.json
```

The previous reviewer kernel is checked against its exact SHA256 before
import. No target Python module or original fixture is imported or consumed
by the independent computation. The checker reconstructs the original
vertices and group, 436 sign regions, both threshold orbits, full polygon
supports, every circle correspondence and all proper orientation cosets.
It brackets positive roots with exact 80-bit dyadic endpoints and proves
strictly positive quadratic Bernstein bounds on all 1,024 closed roll arcs
for the two receiving representatives. Six malformed interval or coverage
controls must be rejected. Explicit checks remain active under `python3 -O`.
Expected output SHA256:
`1103fb6cca5f13c047b275f9e535cc7b65d9a18367c22e9b48aeb96627d4645c`.

The supplementary native replay is distinct from the independent check.
Extract the pinned original contribution when its current files have advanced:

```bash
mkdir -p /tmp/rid-threshold-original
git archive c56d11f8c11bf1eb186b7d648eaf25a4d6586e29 \
  rhombicosidodecahedron_mirror_cluster_obstruction | \
  tar -x -C /tmp/rid-threshold-original
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B /tmp/rid-threshold-original/rhombicosidodecahedron_mirror_cluster_obstruction/threshold_receiver_certificate.py \
  --self-test > /tmp/rid-threshold-native.json
cmp /tmp/rid-threshold-native.json /tmp/rid-threshold-original/rhombicosidodecahedron_mirror_cluster_obstruction/threshold_receiver_expected.json
```

Native output SHA256:
`5516794048036b35ce73b63b0fdf5eb1c01620b260b11f87dfc401e0e5ccfeac`.
[VALIDATION.json](VALIDATION.json) records actual normal/optimized runtimes,
memory, checker and output hashes. All runs were sequential and within the
existing single-CPU scope. No solver, proof assistant, floating-point proof
premise, generated search corpus or private ledger is required.
