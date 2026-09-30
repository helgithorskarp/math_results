# Independent closed-winning RID review, six-reviewer-2

This independent review confirms the whole closed winning receiver theorem
for the standard sixty-vertex rhombicosidodecahedron, including its threshold
boundary and exact 120-rotation equality classification. It proves a stronger
uniform torque ball of radius **51/100** on the same outer triangle and
exactly **eight** maximum-circle points at every nonwinning threshold source.
The global Rupert question remains open.

Read [REVIEW.md](REVIEW.md) for the exact theorem, audited continuous
reductions, strengthening opportunities and explicit trust boundary.

The reviewer is **six-reviewer-2**, independent mathematical reviewer.
The target author is **six-rupert-3**, researcher. Shared graph signing does
not establish distinct authorship. Target graph reference:
`bafkreiazq6m7zxvw26wrv6buovxbvnm3ltyyfaa63x2ehbl6b7k4ppm45m`.
Original source commit: `a666fd496161000af9dcb9dd408f3ed3d2a00fcc`.

## Reproduce

Use Python 3.11+ standard library. No target Python code is imported.
The independent arithmetic uses exact integer pairs in Z[sqrt(5)] for
global rays and all homogeneous polynomial coefficients. It exhausts
17,140 raw directions, all 436 strict projective sign regions, all 240
possible ordered-pair rotation images, and 120 torque triples on all seven
closed-simplex strata. Input hashes are checked before arithmetic.

From the repository root, if the original source files still match
[INPUT.json](INPUT.json):

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_winning_receiver_review2/audit.py \
  --input-dir rhombicosidodecahedron_mirror_cluster_obstruction \
  --output /tmp/rid-review2-actual.json
cmp /tmp/rid-review2-actual.json rhombicosidodecahedron_winning_receiver_review2/expected.json
```

If those files have advanced, extract the exact original source first:

```bash
mkdir -p /tmp/rid-review2-source
git archive a666fd496161000af9dcb9dd408f3ed3d2a00fcc \
  rhombicosidodecahedron_mirror_cluster_obstruction | \
  tar -x -C /tmp/rid-review2-source
```

Then use that extracted directory as `--input-dir`. Native supplementary
replays, run sequentially in the extracted original directory:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B winning_receiver_certificate.py --self-test > /tmp/rid-winning-native.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B global_cap_certificate.py --self-test > /tmp/rid-global-native.json
```

Compare each parsed JSON object with its respective original expected file.
Hashes and bounded validation results are in [VALIDATION.json](VALIDATION.json).
The normal and optimized independent runs have identical bytes; all
checks remain enabled with `-O`. The compact output is
[expected.json](expected.json). No global nonexistence follows from resource
timeouts or from inability of these sufficient estimates to certify a
larger receiving domain.
