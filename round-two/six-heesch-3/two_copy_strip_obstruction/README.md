# Uniform two-copy obstruction for planar strips

Actual author: **six-heesch-3**, role **researcher**.

For every integer m>=2 and1<=r<=m-1, the literal strip T_m has a
packing pair A=(0,0,0,0), B=(0,0,8r+4,-4) that cannot be surrounded
further. More precisely, no interior-disjoint congruent-copy packing
containing the pair covers open neighborhoods of both u=(8r,0) and
v=(8r+6,-2). Added copies may have arbitrary translations, rotations
and reflections. Holes elsewhere are allowed. A common arbitrary
Euclidean isometry preserves the theorem.

The [written proof](PROOF.md) uses complete60-degree corner domains,
whole-hexagon overlaps and a distance obstruction. Its parameter range
is proved by an indexed boundary argument and affine identities; no
sampling extrapolation or plane-registration lemma is used.
This is an author-checked, independently unreviewed lemma, not a
formalization or historical priority claim.

The result can prune a search only when **both copies require a later
surround**. An occurrence in an uncovered final corona is admissible.
The compact T7 fixture here has five complete strict disc coronas and
contains such a pair in its fifth. This particular fifth cannot acquire
a sixth under arbitrary motions. This does not exclude a different
fifth or give a global Heesch upper bound for T7. No seven-corona
construction, finite-seven solution, or original-grid polyform claim
is made for T7, which includes a terminal half-triangle.

## Reproduction

Tested with CPython3.12.14, standard library only, one process/thread.
From this directory run:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O check.py
```

The two modes compare the complete evidence with `expected.json`, not
just aggregate counts. Expected stable evidence SHA256:

    1bb86d55759bd8226e817f717659236fecbd65d97ce65768a7640799a1c40203

Expected:11 affine identities,12 nonvacuous finite controls, actual
positive fixture corona depths[6,5],8 rejected damaged certificates.
Optional `--out PATH` saves the complete evidence and resource metrics;
the checker refuses to overwrite an existing output. The build check
took7.700seconds with24768KiB peak RSS on the author's machine.

The finite controls and damaged inputs validate code, rather than
establishing the infinite parameter range. `geometry.py` reuses exact
integer convex-atom, intersection and boundary primitives from the
[earlier T7 lower reader](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/basic_m7_lower/README.md),
source commit533da1863e9014356acf297441c48ef7f631a4c8. The current
positive fixtures are fully included and require no external download.
Normal/-O agreement is by the same author and is not independent review.

## Files and input provenance

- `PROOF.md`: complete boundary, gap, supplier and overlap argument.
- `check.py`: exact affine, finite supplier and positive-preservation checks.
- `geometry.py`: shared exact polygon reader; no upper-bound algorithm.
- `certificate.json`: eleven affine rows, twelve control parameters and
  one explicit pair in the T7 fifth.
- `fixtures.json`: compact rows[a,f,x,y,level] for the actual T6/T7 patches.
- `expected.json`: deterministic complete expected evidence.

Coordinates mean physical(x,sqrt(3)y)/4. A pose(a,f,x,y) first reflects
in the x-axis if f=1, then rotates by30a degrees, then translates.
Only even a are needed by the forced60-degree suppliers and these
positive fixtures. The proof permits arbitrary added motions because
matching a corner's two rays pins its motion; the checker does not
assume all packings lie on this module.

The T6 positive is the169-copy, six-corona construction of
[Bašić2021](https://doi.org/10.1007/s00283-020-10034-w), reconstructed
from the primary figure and checked as literal polygons. T7 is the
same explicitly defined atom family with seven hexagons; its129-copy
five-corona fixture is this author's saved alternative lower patch.
No finite upper for that shape is asserted. The reader requires every
prefix to be a simple closed disc strictly containing its predecessor,
and every new copy to touch the preceding corona.

Primary background:
[Kaplan2021/2022](https://arxiv.org/abs/2105.09438),
[author census and Hc/Hh conventions](https://cs.uwaterloo.ca/~csk/heesch/),
and [Kaplan2025 survey](https://arxiv.org/html/2509.12216v1).
The finite census is not a size-free record bound. No exhaustive
current-record search or claim that an older theorem is new is made.
The earlier four-copy [continuous-shift obstruction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/two_gap_shift_obstruction/PROOF.md),
source commitd4f702d83abb26bc735dd97b6a87d08ea4f8591a, uses different
local points/configurations; this result does not claim to generalize
that point-only theorem.
