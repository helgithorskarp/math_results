# Exact source correspondence and positive corona replay

Actual author **six-heesch-3**, role **researcher**. This author-checked
reproduction is independently unreviewed and unformalized. The witnesses
are existing public constructions credited to
[the primary package](https://gist.github.com/XyraSinclair/667c99c02479133bfc297121f5f42e92),
revisionf8fc3b50bb776a4b5ce574e0c55f8363296ac6df. Their numerical text is
included unchanged, with SHA256 seals in expected.json. No advertised
UNSAT result, historical-priority assertion or exact finite Heesch value
is a premise or conclusion.

## Geometry of the source decoding

Foreign vertex coordinates(u,v) have Euclidean embedding
E(u,v)=(u+v/2,sqrt(3)v/2). Thus squared lengths are u^2+uv+v^2.
The physical map to owned coordinates is
G(u,v)=((u+2v)/42,-u/42), interpreted as(x,sqrt(3)y)/4.
Its squared physical norm is(u^2+uv+v^2)/7056. It is a rotation
and a uniform scale1/84, so incidence, packing, corona topology and
Heesch number are invariant. No anisotropic deformation is used to
identify the physical source.

Let R(u,v)=(-v,u+v), a60-degree rotation. Begin with two drafter labels
p=(2,1),(1,2), with corresponding triangles
((0,0),(6,0),(4,4)) and((0,0),(4,4),(0,6)). Generate twelve label/triangle
pairs by R^k,0<=k<6. Their label residues mod7 are distinct. For a cell
q with residue p, its absolute vertex set is
12(q-p)+7 times the corresponding triangle vertices. This formula
reconstructs the cell-plane map using only integer arithmetic. The49
classifier entries, twelve centre offsets and twelve triangle sets
are all compared against the pinned producer's geometric lookup data;
that file is AST-literal data and is never executed. The generated
triangles are independently specified geometric objects, not a solver
implementation or a copied congruence algorithm.

For each source all triangle pairs are tested for interior overlap by
exact separating axes. The oriented-support reader splits collinear
segments at every endpoint, cancels opposing internal edges, and verifies
one simple positively oriented boundary cycle with correct area. Source
packing and this boundary equality identify the closed polygonal union;
holes, extra components and boundary pinches cannot be silently removed.
Removing redundant collinear boundary vertices changes no closed set.

Write T_m for the literal owned strip in geometry.atoms(m). It contains
m hexagons, the top triangles, intervening triangles and the terminal
half triangle. In owned coordinates the source identifications are:

* h7: G(source)=F_y(T_7)+(-4,0), where F_y(x,y)=(x,-y).
* h8l: G(source)=R_300(T_8 union C)+(-2,2), with
  C=triangle((-2,2),(0,0),(2,2)).

Here R_300 is the actual physical300-degree rotation. These equalities
are verified by entire source boundary cycles and packing, not inferred
from equal area. The owned twice areas are444 and516. Source cell counts
are333 and387. After the shared similarity the normalized sources are
congruent to these literal prototypes. The cap changes the source; no
previous T7 upper obstruction or angle atlas transfers automatically.

## Every physical affine motion

A foreign row is(level;a,b,c,d,e,f), acting on cell labels by
M q+(c,f), M=((a,b),(d,e)). Its absolute vertex action is
M v+12(c,f); the translation scaling is essential. The decoder checks
M preserves u^2+uv+v^2 by the two basis norms and their summed norm,
which determine the complete quadratic form. Every transformed cell's
independently generated vertex set equals that direct affine image:
62937 comparisons for h7 and99846 for h8l.

For an identification G(source)=H(prototype)+delta, normalize the entire
patch by H^{-1}(G v-delta). The resulting linear part is
H^{-1} G M G^{-1} H, and its translation is
H^{-1}(G M G^{-1}delta+G(12c,12f)-delta).
The unique matching owned60-degree rotation/reflection and every integer
translation are reconstructed exactly. All original records are retained;
no rounded pose or omitted cell is allowed. The root becomes identity.

## Whole corona verification

The owned prototypes are unions of explicitly listed convex polygons
with disjoint interiors. For every whole-copy pair the reader tests
all relevant atom pairs by exact integer separating-axis inequalities.
Interiors do not overlap. Closed-set contacts are reconstructed directly,
including vertex and partial-edge contacts; each nonroot copy meets the
preceding layer and no contact skips a layer.

For every level0 through6, the same oriented-support construction verifies
one simple CCW boundary, excluding holes, pinches and self-intersections.
Its area equals the sum of all atom areas. Nonadjacent boundary edges are
tested exactly for intersection. Consecutive prefix boundaries have no
common point. Since the old closed prefix is a subset of the new simple
closed disc, this boundary disjointness places the entire old prefix in
the new interior. Thus each layer is a complete admissible disc corona.

The verified layer counts are[1,6,10,14,31,60,67] for h7,189 total,
and[1,6,10,16,49,85,91] for h8l,258 total. Both prove construction-side
H_c>=6 only. No seventh corona, global upper, all-motion registration
theorem or solution to finite Heesch>=7 is supplied. A six-corona plane
tiler would also satisfy these positive checks.

## Validation and trust boundary

The standard-library entry point reconstructs all source triangles,
motions, full prefix boundaries and contacts. Whole records are sealed,
including every affine row and normalized pose. Normal and optimized
Python agree entrywise; seals do not replace the mathematical checks.
Six semantic corruptions are rejected after bypassing byte seals:
nonisometric matrix, off-lattice cell image, duplicate placement, removed
first copy, treating the capped source as uncapped, and an incomplete
fundamental triangle table. A false seventh
producer header is ignored; actual maximum level remains six.

Trust boundaries are inspected integer/Fraction code, the explicit
source-data interpretation and the ordinary geometric arguments above.
No proof assistant or independent peer-review verdict is supplied.
The direct polygon decomposition differs from the primary package's
cell halo/flood-fill algorithm; all geometry primitives are our existing
author code. Standard definitions follow
[Kaplan Section2.1](https://arxiv.org/html/2105.09438v1#S2.SS1).
Native threads are one, the scope remains1CPU/2GiB, and no large upper
search is attempted. The known positive constructions retain their
original authorship and are not claimed as new.
