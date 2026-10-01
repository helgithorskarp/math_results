# Exact replay of Bašić's six-corona control

Actual agent **six-heesch-3**, role **researcher**,2026-10-01.
This is a reproducible construction-side replay of **known prior art**,
with a small obstruction to extending the given patch in a specified
registered grid. It establishes no new Heesch record, arbitrary-motion
upper bound, or historical priority. Independent peer review is pending.

Primary source: Bojan Bašić, *A Figure with Heesch Number6: Pushing a
Two-Decade-Old Boundary*, The Mathematical Intelligencer43(3),50–53,
2021, [DOI](https://doi.org/10.1007/s00283-020-10034-w),
[open article](https://pmc.ncbi.nlm.nih.gov/articles/PMC7812982/).
The six-corona construction is Figure2 of that paper. Its stated
all-motion grid alignment argument is a tiling proof sketch with cases
omitted; that sketch is not imported as a finite-prefix theorem here.

Run with Python3.11+ standard library on Linux:

```sh
cd round-two/six-heesch-3/basic_six_control
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O check.py
```

Both modes must match `expected.json` exactly. No solver, downloaded
image, external certificate, or floating-point geometric test is needed.
The complete replay took approximately five seconds and less than32MiB
in the author's runs. Negative controls delete one necessary first-layer
tile and translate another into the root; both are rejected.

## Exact tile and lower certificate

Coordinates `(x,y)` mean the Euclidean point `(x,sqrt(3)*y)/4`.
For `j=0,...,5`, put `u=8*j`. The unit hexagon has vertices

```
(u,0),(u+2,2),(u+6,2),(u+8,0),(u+6,-2),(u+2,-2).
```

Attach the triangle `(u+2,2),(u+4,4),(u+6,2)` above each hexagon.
For `j<5`, attach the bridging triangle
`(u+6,2),(u+8,0),(u+10,2)`. Finally attach the half triangle
`(46,2),(48,0),(48,2)`. These atoms have disjoint interiors and
form a simple polygon of area `95*sqrt(3)/8`.

`certificate.json` contains169 poses, including the normalized root.
A pose `[a,f,tx,ty]` first reflects `y` if `f=1`, rotates through
`30*a` degrees, and translates by `(tx,sqrt(3)*ty)/4`. Only even
`a` occurs. The exact60-degree update is
`(x,y) -> ((x-3*y)/2,(x+y)/2)`; every numerator in this certificate
is even. Thus these transformations are Euclidean congruences, although
the incidence reader works in the integer coordinate plane.

`geometry.py` checks convex atom intersections with integer separating
lines. It allows partial straight-edge contacts and T contacts.
For each prefix it splits collinear oriented supports at all endpoints,
cancels internal intervals, and checks that the remaining boundary is
one noncrossing CCW cycle with the correct area. A single simple cycle
and disjoint atom interiors certify a closed topological disc. Every
added copy touches some copy from the preceding level. Consecutive
prefix boundaries are disjoint; since the previous union is included
in the next union, this certifies strict containment in its interior.

The corona counts are `1,6,10,13,32,52,55`, giving cumulative counts
`1,7,17,30,62,114,169`. The final patch has464 touching tile pairs.
All six prefixes satisfy the disc convention in the primary definition,
so they also meet the construction side of both usual Hc/Hh conventions.

## One-cell obstruction for this fixed registered patch

Register the3.6.3.6 grid whose hexagon centers, in the coordinate
system above, are `(4+8*i+4*j,4*j)`. Restrict added copies to positions
where their constituent unit hexagons match that grid, including all
six60-degree rotations and reflections. This is an additional model
assumption; an arbitrary-motion corona has not been reduced to it.

Subdivide every grid triangle at its centroid and edge midpoints into
six fine triangles; a half triangle is three whole fine cells.
`mesh.py` multiplies the integer coordinates above by three so every
centroid remains integral. The prototype consists of six whole hexagon
cells and69 fine triangular cells. The reader independently checks that
this subdivision has disjoint interiors and exactly the tile's outline.

Consider the fine triangle with scaled coordinates
`(-138,-66),(-144,-66),(-144,-68)`; its Euclidean coordinates have
denominator12. Its interior is disjoint from the169-copy patch, while
its vertex `(-138,-66)` belongs to that closed patch. Any registered
extension strictly enclosing the patch must occupy this entire fine
cell, because every registered tile is a union of whole mesh cells.

`one_cell_cut.py` directly aligns each fine prototype cell, in every
allowed orientation and reflection, to this target. Translation
preserves lexicographic vertex order, so the first-vertex difference
determines the only possible alignment; all three vertices are checked.
The first hexagon center must be of the form
`(12+24*i+12*j,12*j)` in scaled coordinates. This generates **all69
registered placements** covering the target. Each has a positive
interior overlap with a tile already in the patch, checked using actual
convex polygons rather than trusting a shared-cell label. The compact
overlap records have SHA256
`d8bce428d1c617c574b21743385b1f7d427dc4c4c684e1e5d69c7a5f3cfb133a`.

Consequently the **given** six-corona patch has no seventh registered
corona. This does not classify other six-corona patches and does not
establish impossibility under unregistered translations or rotations.

## Provenance and trust

The poses were recovered separately from both panels of an
[author-attributed vector copy](https://commons.wikimedia.org/wiki/File:A_polygon_with_Heesch_number_6.svg)
of Figure2, and the two normalized pose sets agreed. The vector contains
rounded coordinates; rounding was only a proposal mechanism. The
published evidence is the exact checked congruence data. The vector is
not redistributed here. Credit: Bojan Bašić; the Commons source figure
is licensed [CC BY-SA4.0](https://creativecommons.org/licenses/by-sa/4.0/).
The extracted placement data retain that attribution and license.

The source SVG SHA256 is
`87aea1e0f3c709c95176a9695dfc85e4ca5a6c160df6f14b29eb84a095ecc126`.
The verification is an author-checked integer computation, with Python
integer arithmetic and the geometric/topological arguments above as its
trust boundary. Matching normal/optimized runs is not independent peer
review. The open target remains a rigorously finite planar Heesch number
at least seven.
