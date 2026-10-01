# Independent RID Gram and fixed-plane audit

Reviewer: **six-reviewer-4**, independent mathematical reviewer. Read REVIEW.md
for exact scope and the ordinary geometric proof. Target9093 belongs to
six-rupert-3. Global RID remains open.

The independent original-coordinate computation confirms the whole stated
relaxation-gap claim. A new exact certificate excludes every planar rotation
or reflection and arbitrary translation at scale at least one for this
**fixed pair of source/receiving projection planes**. Its maximal fitted
scale is below1-1/65536. This is not an all-source exclusion at the receiver.

From a checkout containing the four pinned sibling own-geometry files:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-reviewer-4/rid-gram-audit/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O round-two/six-reviewer-4/rid-gram-audit/check.py
```

Run sequentially. Expected output is PASS and successful exit. Python3.11+
standard library only, no solver/network/library environment required.
The whole derived independent record is compared byte for byte with
expected.json. --emit writes a fresh whole record for development.

The finite computation reconstructs original hull/group/physical polar
premises, both complete gift-wrapped shadows, all physical edge widths,
all16 directed receiving edges and their maximum excesses, actual equatorial
and transported-row constraints, and both complete full-shadow common-angle
systems. It checks those systems by two distinct algorithms: all active
circle boundaries, and exact complete planar convex-polars. Large redundant
inventories are recomputed and fingerprinted, with exact maxima and attaining
vertices retained explicitly. No external proof corpus is required.

The optional decoded author-record comparison is explicitly partial:

```sh
python3 -B round-two/six-reviewer-4/rid-gram-audit/compare.py PATH_TO_NATIVE_OUTPUT.json --controls
```

It compares physical areas/widths/Gram/row entries, all16 actual edge endpoints,
excesses and supplied maximizers, both complete sixteen-corner inventories,
and the entire2304-control decision fingerprint. It never runs/imports author
code. Whole native replay was separately performed in this review, with its
own exact expected bytes and twelve pinned transitive prerequisites; metrics
are in VALIDATION.json. It is not a second whole-record comparison.

The pure circle.py endpoint algorithm also works with negative thresholds,
zero vectors and singleton arcs. A distinct convex closest-point oracle is
used only for strictly positive thresholds. REVIEW.md proves the reductions
and explains why pairwise positive-support feasibility need not imply a
common angle for three supports. No angle samples prove an exclusion.
