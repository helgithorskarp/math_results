# An all-motion obstruction to extending one curved-trapezoid corona

Author **six-heesch-3**, role **researcher**, 2026-09-30. Written geometric
proof and exact finite certificates; no formalization or independent
peer-review verdict. The checker uses only Python's standard library.

The tile below is an unmarked topological disc, with all real Euclidean
translations, rotations and reflections allowed. We prove

\[
               1\le H_c(T)\le H_h(T)\le85.
\]

Here every earlier cumulative prefix lies strictly in the interior of the
next; each new copy touches the preceding corona. All prefixes for \(H_c\)
are discs. For \(H_h\), holes and pinches may occur in the last prefix.
The upper bound also holds if holes are allowed at every prefix.

The new extension result is narrower than a Heesch-value theorem:
**the specified six-copy first corona admits no finite strict surrounding,
under arbitrary real motions of the additional copies.** Holes in that
surrounding do not avoid the obstruction. Different first coronas remain
open, so this does not prove \(H_c(T)=1\), exclude all second coronas, or
produce a finite-seven shape.

## Explicit geometry

Use axial coordinates
\(L(q,r)=(q+r/2,\sqrt3r/2)\), with squared physical norm
\(q^2+qr+r^2\). The eighteen labelled vertices are

\[
v_0=(0,0),\quad v_1=(0,-1),\quad v_2=(0,1),\quad
v_{2j+1}=(j,-1),\quad v_{2j+2}=(j,1)\ (1\le j\le7),\quad
v_{17}=(8,-1).
\]

Their counterclockwise order is
\(0,1,3,5,7,9,11,13,15,17,16,14,12,10,8,6,4,2\).
The four genuine corners are \(v_1,v_{17},v_{16},v_2\), of angles
\(60,90,90,120\) degrees; the other fourteen labelled vertices have
angle180 degrees. The straight trapezoid tiles the plane. The finite
candidate is its curved boundary, rather than that quadrilateral.

Port indices use endpoint pairs

```
0:(0,1)   1:(0,2)   2:(1,3)   3:(2,4)   4:(3,5)   5:(4,6)
6:(5,7)   7:(6,8)   8:(7,9)   9:(8,10) 10:(9,11) 11:(10,12)
12:(11,13) 13:(12,14) 14:(13,15) 15:(14,16) 16:(15,17) 17:(16,17).
```

Their directions in [input.json](input.json) are counterclockwise. Ports0
through16 have length1, and port17 has length \(\sqrt3\). The signs are

```
1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,0.
```

On a counterclockwise physical unit chord from \(v\) to \(v+e\), use
\[
 v+ze+s_i\lambda z^2(1-z)^2n,\qquad
 0\le z\le1,\quad n=(e_y,-e_x),\quad\lambda=1/100.
\]
Port17 stays straight. Signs describe geometry, and impose no symbolic
markings on the final tile. A positive arc bows outward; a negative arc
bows inward. There are nine positive arcs and eight negative arcs.

Let \(R(q,r)=(-r,q+r)\) and \(J(q,r)=(q+r,-r)\). A pose code
\((h,k,a,b)\) means \(R^kJ^h(q,r)+(a,b)\). The six fixed poses, with
copy0 the root, are

```
0:(0,0,0,0)    1:(0,0,0,-2)   2:(0,0,0,2)
3:(0,1,-1,-5)  4:(1,3,15,-2)  5:(1,3,15,0).
```

They retain29 complementary full ports, with50 exposed ports. Every added
copy shares an edge with the root. These particular poses came from
releasing one interface of the prior hexapillar first-corona network;
the earlier [global endpoint-rigidity lemma](../heesch_weighted_matching_obstruction/first_corona_global.md)
concerns the unreleased network. Its hypotheses do not cover this changed
trapezoid or different contact arrangements.

## Analytic contacts and the first-corona geometry

The polynomial portion of the
[quartic contact proof](../heesch_weighted_matching_obstruction/quartic_realization.md)
does not use a polyform grid. Here it applies to all seventeen nonflat
unit arcs. For completeness, if an isometry shares a nontrivial subarc,
the defining degree-four polynomial divides the transformed defining
polynomial. Equal degrees make them constant multiples. The homogeneous
degree-four term forces the tangential axis to be preserved. Orthogonality
leaves \(Q=\operatorname{diag}(a,b)\), \(a,b\in\{1,-1\}\).
Coefficient comparison forces equal amplitudes,
\(x\mapsto ax+(1-a)/2\), and no normal translation. Thus the complete
unit arcs and both chord endpoints coincide. A straight line cannot share
such an arc. Two noncoincident transformed quartics meet at only finitely
many points.

A charged boundary arc strictly inside a finite union is covered by other
tile boundaries. Finite intersections alone cannot cover it, so it has a
full coincident arc on another copy. Their interior sides are opposite,
forcing opposite signs. The mate is unique because two copies on the same
side would overlap locally. This covers all motions and any attempted
partial or split charged contact. The straight port remains uncharged;
no grid locking or atomicity is assumed for flat contacts.

The separate first-corona test uses exact convex half-plane intersections,
all labelled shared ports and one simple oriented outer cycle. It checks
all root vertex stars are filled and no exposed edge contains a root
vertex. There is no interior overlap, the root has five neighbours, and
the union is a disc strictly surrounding the root.

The first-corona chord network has minimum nonincident squared distance
\(3/4\), no crossings or unrecorded partial overlaps, and distinct
incident rays separated by at least30 degrees. Each charged arc moves by
at most \(\lambda/16=1/1600\). From either endpoint its cone deviation
is at most \(\arctan(1/675)\), since
\(z^2(1-z)^2/z\le4/27\), and likewise at the other endpoint.
Twice the cone deviation is below30 degrees, and twice the displacement
is below \(\sqrt3/2\). Scaling the amplitude from0 to1/100 therefore
preserves incidence and cyclic order of the network. Complementary matched
arcs coincide throughout. This network isotopy extends over the disc faces
and exterior, preserving nonoverlap, topology and strict containment.
It proves the actual curved shape is a Jordan disc and \(H_c(T)\ge1\).

## A uniform buffer for forced skeleton overlaps

It is necessary to justify using the undeformed quadrilaterals to exclude
curved copies. Only placements forced by charged contacts will be used.
Their linear maps belong to the twelve triangular-lattice isometries, and
their translations are integral axially: the unit chord image fixes the
map up to its two possible hands, then one integer endpoint fixes the
translation.

**Buffered-overlap lemma.** If two such straight quadrilaterals have
positive-area intersection, their intersection contains a physical disk
of radius at least \(1/96\).

Proof. Write each edge direction as its primitive integer vector. All are
one of the six unit directions or the six30-degree-offset directions of
physical length \(\sqrt3\). Determinants of two such primitive vectors
have absolute values at most3. Integer half-plane offsets imply each
intersection vertex has coordinates with denominators1,2 or3, hence lies
in \((1/6)\mathbb Z^2\). The convex intersection has at most eight
vertices. Average its distinct vertices. For a positive-area intersection
this point is strictly inside every defining half-plane, with determinant
slack at least \(1/(6m)\ge1/48\), \(m\le8\). Under \(L\), the distance
to the corresponding line is that slack times
\(\sqrt3/(2|Le|)\ge1/2\). Thus its distance to every edge line is at
least1/96. The checker also audits these rational vertex, slack and squared
distance bounds on every positive intersection used in the inventories.

Since1/96 exceeds1/1600, the center remains strictly inside both curved
copies: their boundary homotopies stay within1/1600 of their polygon
boundaries and cannot pass through it. Therefore every positive skeleton
overlap is a sound curved-overlap exclusion for these forced placements.
This direction is all that the proof needs; it makes no converse assertion
about skeletons that merely touch.

Two positive arcs on opposite sides of the same skeleton chord also cause
physical overlap: their outward bows enclose an open lens occupied by both
copies. This supplies extra binary conflicts. Equal negative signs are
not used as physical conflicts in the final necessary relaxation.

## Complete finite charged-port selector

The fixed six-copy first prefix has48 exposed charged arcs:27 positive
and21 negative. In a hypothetical finite strict surrounding, each one has
an opposite-sign mate. Enumerate every prototype unit port, both endpoint
correspondences and all Gram-preserving triangular-lattice maps. Endpoint
equations give275 distinct potential full poses. The buffered-overlap lemma
removes90 that overlap fixed copies, retaining185. No other new copy is
assumed to lie on a lattice: retain only these required charged-arc mates
from the hypothetical real surrounding, and omit unrelated copies.

For each of48 charged ports require at least one of its candidate mates.
Reject every candidate pair with positive skeleton overlap:3,043 pairs.
Add1,864 distinct positive/positive chord conflicts; these may duplicate
some skeleton conflicts. These are necessary constraints, not a complete
construction encoding. In particular there is no flat-port coverage,
window restriction, whole-neighbour integrality or disc requirement.

The catalogue is independently reconstructed by enumerating integral
unit-norm column pairs with Gram product1/2, instead of repeated rotations.
Rational half-plane clipping independently reconstructs every overlap
pair, instead of the discovery code's separating-axis tests. A private
comparison matches every pose, covered port and individually classified
conflict. Canonical hashes are in [expected.json](expected.json).

## Fifteen local exclusions under arbitrary real motions

The base selector admits models. The certificate adds fifteen exclusions
specified in input.json: two unary and thirteen binary. Every row gives
an earlier-prefix vertex, a conjunction of selected candidate poses, and
an empty angular component created there by those copies together with
the fixed first prefix. The earlier vertex must become interior in any
strict surrounding. Extra copies away from that point have positive
clearance, since the surrounding is finite, and cannot fill its local gap.

All fifteen rows use only the following two elementary obstructions:

* Eight rows leave an isolated30-degree sector. Every incident sector of
  this tile has angle at least60 degrees; an arc-interior point contributes
  180 degrees and an interior point360 degrees. No new tile can fill it.
* Seven rows leave an isolated60-degree sector bounded by two charged
  arcs of the **same** sign. Exactly one60-degree vertex must fill it.
  There is only one such prototype vertex, \(v_1\); its adjacent ports0
  and2 have signs positive and negative. To share the two gap boundaries
  it would need signs opposite to both bounding signs. Two equal signs
  cannot be complemented by its mixed pair. Partial charged contacts do
  not help, by the analytic lemma. No second tile fits a60-degree gap.

Every cut is thus a necessary local exclusion of its provider conjunction.
The checker reconstructs occupied sectors and unique radial boundary owners
from the actual complete prototypes; it verifies the stated gap, width
and signs. No integrality or orientation restriction is placed on the
excluded prospective filler. Wider gaps and120-degree partitions are
unneeded by this certificate.

The final finite cover problem is exhausted directly. At each node choose
an uncovered required arc with the fewest available candidate mates. Branch
on **every** available mate, add all ports covered by it, and remove it and
every incompatible candidate from future choices. Empty cover sets close
a branch. Selected unary and binary cuts are treated as exclusions.
Any hypothetical model has a mate for the chosen arc, so occurs in one of
these branches. This is a complete search, without a SAT solver. It has13
recursive calls and12 failed states, and no accepting leaf.

The discovery SAT formula independently has185 variables and4,970 clauses
(48 coverage,3,043 skeleton,1,864 positive-arc and15 local-cut clauses).
Its cold native trace passes RUP checking with zero RAT lemmas. The private
trace/input hashes and checker provenance are recorded in README.md;
neither the trace nor the solver is required by the public direct checker.
Therefore no arbitrary-motion finite strict surrounding of the fixed
first corona exists, even permitting holes in the surrounding union.

## Sound finiteness independent of that prefix exclusion

The tile area and diameter bounds are
\[
 A=15\sqrt3/2+1/3000>1299/100,\qquad
 D\le\sqrt{67}+1/800<6553/800.
\]
The checker verifies the straight area and all vertex-pair distances, and
the rational bounds \((433/250)^2<3\), \((819/100)^2>67\).
The area correction is \(\lambda(9-8)\int_0^1z^2(1-z)^2dz=1/3000\).
The diameter increases by at most twice the maximum arc displacement.

If \(N_i\) counts the cumulative copies through level \(i\), every one
of its \(9N_i\) positive arcs is paired injectively to a negative arc in
the next prefix, with only \(8N_{i+1}\) available. Thus
\[
 N_{i+1}\ge\lceil9N_i/8\rceil.
\]
Every level-\(i\) tile is joined to the root by at most \(i\) contacts
and lies in a disk of radius \((i+1)D\) about a root point. Disjoint area
and \(\pi<22/7\) give
\[
 N_i\le\left\lfloor
 \frac{(22/7)(6553/800)^2}{1299/100}(i+1)^2\right\rfloor.
\]
Starting with one root, depth86 requires130,235 copies but permits at most
122,872. Hence even relaxed86-corona patches are impossible and
\(H_h(T)\le85\). In a putative plane tiling, bounded diameter and disjoint
positive area give local finiteness; the same growth and packing argument
applies to finite contact-graph balls at every depth and excludes tiling.

## Literature and remaining frontier

The general bump/nick imbalance mechanism is established prior art in
[Mann2004](https://faculty.washington.edu/cemann/Heesch.pdf), including
hexapillars of Heesch number5 and square polypillars of number3.
The contact lemma and explicit depth estimate here extend the previously
published quartic argument to this particular non-polyform trapezoid;
no new imbalance principle or historical priority for a low-Heesch shape
is claimed. A bounded candidate-specific literature check did not establish
an exact prior classification for this profile family. It is not an
exhaustive novelty audit.

[Kaplan2022](https://arxiv.org/abs/2105.09438) and its
[author dataset](https://cs.uwaterloo.ca/~csk/heesch/) concern bounded
polyform sizes and distinct corona conventions. The
[2025 account](https://arxiv.org/html/2509.12216v1) uses topological-disc
shapes and reports the connected finite record6. Theorem7 of
[Bašić–Džuklevski–Slivková2023](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v30i2p50/pdf/)
already realizes every positive finite Heesch value with two-part
disconnected tiles and a relaxed nesting convention. That does not resolve
the connected-disc finite-seven target.

Complementary [214-cell polyiamond work](../heesch_polyiamond_local_deficit/proof.md)
and its [independent review](../heesch_polyiamond_deficit_review1/REVIEW.md)
prove \(5\le H_c\le H_h\le385\) for a different known-family shape.
Their corner certificates do not classify this trapezoid. The analogous
[polyomino corner work](../heesch_polyomino_corner_obstruction/proof.md)
uses locally forced contacts while leaving unrelated motions unrestricted;
its square-grid and half-grid results are not hypotheses here.

The useful conclusion is to stop trying to extend the particular released
six-copy prefix. Search other first coronas or other released contact
networks, retaining full curved geometry and a finite upper proof. Seven
complete admissible coronas of a connected disc are still absent.
