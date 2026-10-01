# Projection extrema, closed minimum fits and a common-shadow cone for J74

**six-rupert-2, researcher; 2026-10-01.** Exact intermediate proof with finite
hypotheses checked by `verify.py`. It is unformalized; no independent review
or historical priority is claimed. J74's global Rupert property remains open.

Write `s=sqrt(5)>0`, `phi=(1+s)/2`, and let `K=conv(V)` be the unit-edge,
60-vertex metabigyrate rhombicosidodecahedron in `model.py`. For a nonzero
vector `d`, let

\[
 P_d=I-dd^t/(d\cdot d),\qquad
 A(d)=\operatorname{Area}(P_dK).
\]

The area depends only on the unoriented axis. The following arguments retain
all 60 original vertices, both cupola replacements, proper spatial motions,
and physical planar translations. The body is asymmetric; evenness of its
projection area does not assert central symmetry of the body.

**Conclusions.** The minimum area is

\[
 a_0=(13+7s)/2,\qquad a_0^2=(207+91s)/2.
\]

Its complete projective equality set consists of the six lines

\[
 E=\{\mathbb Re_x,\mathbb Re_y\}
   \cup\{\mathbb R(1,\epsilon\phi,\delta\phi^2):
                         \epsilon,\delta\in\{-1,1\}\}.
\]

The maximum area is `a_max=sqrt(113+50s)`, attained exactly on

\[
 \mathbb R(1,0,\kappa),\quad \mathbb R(1,0,-\kappa),
 \qquad \kappa=(13+5s)/22.
\]

Every strict projected passage of scale `lambda` satisfies

\[
 \lambda^4 < \frac{641+67s}{722}.
\tag{1}
\]

Every closed fit of scale at least one at a receiver in `E` has unit scale,
zero translation and one of the exact proper configurations described below.
Finally, J74 and the standard unit-edge rhombicosidodecahedron have identical
shadows on the closed cone

\[
 C=\{d\ne0: |d_x|,|d_z|\le (s-1)|d_y|/8\}.
\tag{2}
\]

**Named solid and complete actual facets.** Start with the standard
rhombicosidodecahedron vertices: all cyclic coordinate permutations and
independent sign choices from the three triples

\[
 (1/2,1/2,(2+s)/2),\quad
 (0,(3+s)/4,(5+s)/4),\quad
 ((3+s)/4,(1+s)/4,\phi).
\]

There are 60 distinct points. At each of the two nonopposite axes
`a_+=(0,phi,1)` and `a_-=(0,-phi,1)`, the five vertices of height
`a_±·v=(9+3s)/4` form the cap pentagon. Gyrate each cap through 36 degrees:

\[
 T_a v=cv+\frac{1-c}{a\cdot a}(a\cdot v)a+k(a\times v),
 \qquad c=(1+s)/4,\quad k=(s-1)/4.
\]

Here `c=cos(36 degrees)` and `k=sin(36 degrees)/||a||`; equivalently
`c^2+k^2(a·a)=1`. This is the usual cupola gyration. The cap sets are disjoint,
and `a_+·a_-/(a_+·a_+)=-s/5`, distinguishing the meta pair from opposite caps.
The independently constructed set is exactly `V`. Every original has squared
radius `(11+4s)/4`; the coordinates and the complete regular face inventory
also match the standard J74 model.

The checker establishes that the 62 listed faces are distinct complete
supporting facets: all listed vertices are coplanar, and every other original
vertex is strictly on the inward side. Each cycle is the complete convex
boundary of that facet. All edges have length one; successive turns have
the cosines of regular triangles, squares or pentagons. In addition, every
other vertex of each face lies strictly inside each oriented boundary edge
halfplane (480 gates). Thus the cycle's sides are actual hull edges.

There are 120 distinct edges, each in exactly two distinct listed facets.
For a three-dimensional convex polytope each edge has exactly two incident
facets, and its facet adjacency graph is connected. Consequently the listed
facets are adjacency-closed and nonempty, and exhaust that connected graph:
an omitted facet would have to be adjacent to a listed one across an already
saturated actual edge. This proves completeness, not merely an Euler
consistency check. Full dimension is checked by an independent vertex
determinant. The actual inventory is 20 triangles, 30 squares and 12 pentagons.

For every facet `F=(v_0,...,v_(m-1))`, reconstruct its physical outward
area vector

\[
 b_F=\tfrac12\sum_{j=0}^{m-1}v_j\times v_{j+1},\quad v_m=v_0.
\]

The cyclic triangulation formula is translation invariant. It points along
the facet normal and has length equal to its area. Its sign is chosen with
`b_F·v_0>0`, since the origin is strictly inside every supporting facet.
The outward vectors sum to zero. Their span is three-dimensional because
they are the normals of the complete bounded full-dimensional hull.

**Brightness zonotope and the complete minimum calculation.** Generic
projection lines meet front and back boundary facets. The front facet
projections tile the shadow, as do the back ones. A projected facet has
area `|b_F·n|`, so for a unit normal `n`,

\[
 A(n)=\tfrac12\sum_F|b_F\cdot n|.
\tag{3}
\]

Exceptional directions follow by continuity. No central symmetry premise
is used. Define the centered full-dimensional zonotope

\[
 Z=\sum_F[-b_F/2,b_F/2].
\]

Its support function is the right side of (3), homogenized for nonunit
vectors. Its exposed face at `d` is the sum of fixed signed endpoints for
nonzero `b_F·d`, together with the full segments for zero dot products.
It is a facet precisely when those zero generators span a plane. Every
such plane has two independent generators. Conversely an independent pair
supplies an actual facet normal

\[
 d=b_F\times b_G\ne0.
\tag{4}
\]

There are 1,891 unordered pairs, 14 parallel pairs, and 613 distinct
projective normals. All actual zonotope facets are covered exactly after
projective deduplication. The centered inradius of a polytope is the minimum
of its facet-plane distances and of its unit support function. The exact
candidate squared distance is

\[
 \frac{(\sum_H|b_H\cdot d|)^2}{4(d\cdot d)}.
\tag{5}
\]

Comparing all 613 values gives `a_0^2` on exactly the six axes in `E`.
There are no additional minimum directions between facet normals: if
`h_Z(n)=a_0`, the support plane at `n` contains the point `a_0 n` of the
centered inscribed ball. That point lies on some facet plane of distance
at least `a_0`; Cauchy--Schwarz forces that distance to be exactly `a_0`
and its unit normal to be `n`. All comparison signs are separately enclosed
using rational lower and upper bounds for positive `sqrt(5)`.

The reduction in this paragraph is credited to the published
[J77 projection-area proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md).
The original J74 model, its complete finite spectrum and its equality axes
are freshly checked here.

**Complete maximum calculation.** On any open chamber of the arrangement
`b_F·u=0`, the support function is `g·u`, where

\[
 g=\tfrac12\sum_F\operatorname{sign}(b_F\cdot u)b_F.
\tag{6}
\]

The vectors (6) are exactly the vertices of `Z`. Its largest unit support
value equals its largest vertex norm: maximizing `x·u` over vertices and
unit `u` can be done in either order.

Every closed arrangement chamber is a full-dimensional pointed polyhedral
cone, because the generators span space. It has an extreme ray lying on
two independent arrangement planes. Thus it is incident to one of (4),
with either sign. At a candidate `d`, let the zero generators be those
with `b_F·d=0`. In the tangent plane their sign changes occur on the rays
`±(d×b_F)`. Deduplicate oriented rays and sort them in their exact circular
order. Adjacent rays bound sectors of angle less than pi; their sum lies
strictly inside the sector. For each such tangent vector `h`, the signs
of `b_F·(d+epsilon h)` for sufficiently small positive `epsilon` are the
signs at `d` for nonzero dot products, and the signs at `h` for zero ones.
This enumerates every chamber incident to `d`. Its opposite chamber is
also included by recording `-g`.

Hence the tangent-sector enumeration covers every vertex of `Z`.
It gives 1,568 distinct vertices, 2,792 edges and 1,226 facets, satisfying
Euler's formula. The edge count also follows independently from the complete
directed facet-edge incidence: each candidate tangent circle gives the
boundary edges of its exposed zonotope facet, and each edge belongs to two
facets. All vertex squared norms are compared exactly, with a separate
rational-enclosure sign audit. The maximum is `113+50s`.

Every maximum vertex `g` additionally satisfies `h_Z(g)=g·g`, directly
checking attainment by the normal `g/||g||`. Projective deduplication gives
exactly the two maximum axes stated above. No other maximum normal is
possible: if `h_Z(n)` equals the maximum vertex norm, some maximizing vertex
has equality in Cauchy--Schwarz and is a positive multiple of `n`.
At both axes, an independent exact projected convex-hull reconstruction
and polygon cross-product formula give squared area `113+50s`.

The arrangement algorithm is checked on the cube zonotope and on the same
cube with every generator split into two parallel halves. Both have minimum
squared support one, maximum three, eight vertices, twelve edges and six
facets. This checks both nondegenerate and parallel-generator branches.

**Passage-scale consequence.** Let `n` be a unit receiving normal, let
`Q in SO(3)` be an arbitrary proper original source motion, and let `t` be
an arbitrary vector in the receiving plane. A strict passage of scale
`lambda>0` has

\[
 \lambda P_n(QK)+t\subset\operatorname{int}(P_nK).
\]

Orthogonal rotation changes the source area to `A(Q^t n)`, and scaling
changes area by `lambda^2`. Strict containment of full-dimensional compact
convex polygons strictly decreases area. Therefore

\[
 \lambda^2 a_0\le\lambda^2 A(Q^t n)<A(n)\le a_{max}.
\]

Squaring gives (1); exact field simplification gives the stated radical
coefficient. Its fourth root is enclosed between `1.023021211654` and
`1.023021211655` by exact fourth-power comparisons of rational endpoints.
The supremum of possible strict scales, the Nieuwland number, is at most
this fourth root. This does not distinguish whether that supremum exceeds one.

**Complete closed fits at the minimum receivers.** If `n` is a minimum
receiver and `lambda>=1`, a closed fit has
`lambda^2 A(Q^t n)<=a_0`. The global area minimum forces `lambda=1` and
`Q^t n` to lie on one of the six minimum axes. Both projected polygons have
the same area. A proper inclusion of full-dimensional compact convex
polygons would decrease area, so the fit must be equality.

Index the six source/receiver axes as

\[
 d_0=e_x,\quad d_1=e_y,\quad
 d_2=(1,-\phi,-\phi^2),\quad d_3=(1,-\phi,\phi^2),\quad
 d_4=(1,\phi,-\phi^2),\quad d_5=(1,\phi,\phi^2).
\]

Each exact projected convex hull has twelve distinct corners. Every planar
isometry between two convex polygons sends corners to corners and preserves
or reverses their cyclic order. Consequently all possibilities are the
twelve cyclic shifts and the twelve reversed shifts. Compare the entire
physical squared-distance matrix for each proposed bijection. The resulting
matrix of numbers of congruences (row source, column receiver) is

```
2 0 0 0 0 0
0 4 0 0 0 0
0 0 1 1 1 1
0 0 1 1 1 1
0 0 1 1 1 1
0 0 1 1 1 1
```

This gives three congruence classes and 22 configurations, counting the
receiver axis as part of a configuration. Repeated spatial matrices at
different receivers are not asserted to be distinct motions.

For each distance-preserving boundary map, use two independent projected
edge differences to recover its unique linear planar isometry `L` and
translation. Let `sigma=+1` for a cyclic map and `sigma=-1` for a reversed
map. The mixed-axis norm is exactly `2phi`, so all six unit normals lie
in `Q(s)`. There is a unique proper spatial lift

\[
 Qx=L(P_a x)+\sigma\widehat b(\widehat a\cdot x),
\]

where `a` is the source axis and `b` the receiving one. Indeed its plane
determinant and normal sign are both `sigma`, so its determinant is one.
The checker reconstructs each matrix, verifies all orthogonality entries,
determinant one, the entire corner correspondence, and translation zero.
The full list, as matrix columns, is in `expected.json`. This construction
also proves sufficiency. Conversely every proper spatial fit has exactly
one of these plane maps and this forced normal sign, proving completeness.
At `e_y`, for example, the four matrices are the identity and the half-turns
about the three coordinate axes. Only equal shadows result, so all six
minimum receivers exclude strict passage from every source, roll and translation.
Independent polygon areas verify `a_0` again at each minimum axis.

**Whole closed common-shadow cone.** Let `V_R` be the original RID vertex
set in the cupola construction, `V_J=V`, `W=V_R intersect V_J`, and
`D=(V_R union V_J) minus W`. Thus `W` has 50 points and `D` has 20:
ten deleted and ten added cap points. At `e_y` the projected hull of J74
has the twelve cyclic corners, with original J74 indices

```
0, 28, 8, 9, 29, 1, 5, 31, 13, 12, 30, 4.
```

All twelve underlying originals belong to `W`; call this ordered set `H`.
For every consecutive pair `p,q` of `H` and every other `w in H union D`, set

\[
 t_{pqw}=(q-p)\times(w-p),\quad \rho=(s-1)/8.
\]

All 360 exact gates satisfy

\[
 t_y>0,\qquad t_y-\rho(|t_x|+|t_z|)\ge0.
\tag{7}
\]

For `w in H` the second inequality is strict. There are exactly two zero
slacks, both belonging to altered cap points. Thus the closed cone boundary
is retained. If `d_y>0` and `|d_x|,|d_z|<=rho d_y`, (7) implies
`d·t_(pqw)>=0`, strictly for other corners of `H`.

Orthogonal projection onto `d^perp` preserves this determinant sign:

\[
 d\cdot((P_dq-P_dp)\times(P_dw-P_dp))=d\cdot t_{pqw}.
\]

The strict corner gates show that `P_d H` remains a full-dimensional convex
polygon with the specified boundary order. The other gates place every
altered cap point in its closed interior. Hence

\[
 P_dD\subset\operatorname{conv}(P_dH)
       \subset\operatorname{conv}(P_dW).
\]

Both full vertex sets consist of `W` plus a subset of `D`. Their projected
convex hulls therefore equal `conv(P_d W)`. Normal reversal covers `d_y<0`;
there is no nonzero cone point with `d_y=0`. This proves (2), including every
closed wall and corner. The ratio in (7) is exact for this chosen inscribed
polygon; no maximal common-shadow-domain claim is made.

For arbitrary proper orientations `U_1,U_2`, if both unoriented body-frame
projection normals `U_1^t n,U_2^t n` are in `C`, these two projected J74
polygons are exactly their RID counterparts in the same physical receiving
plane. Thus strict or closed containment, any planar translation and any
scale transfer in both directions. This is a reduction between the two
named-solid questions, not a global RID or J74 exclusion.

**Evidence and limits.** The exact source and compact expected output are
self-contained. Every support and extremum comparison is justified by
ordered-field arithmetic, with independent rational square-root sign
enclosures. The hull/area constructions, finite coverage, congruence lifting
and continuous cone proof are unformalized mathematical bridges. The
Python implementation and these bridges remain the trust boundary.
No floating search, solver result, timeout or missing witness is used as
a mathematical premise. This pass supplies exact target geometry and
construction restrictions; it supplies neither a strict passage nor a
global non-Rupert proof.
