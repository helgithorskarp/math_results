# Two curved-trapezoid coronas and a three-copy interior obstruction

Author **six-heesch-3**, role **researcher**, 2026-09-30. Written geometric
proof with exact standard-library computation; no formalization or independent
reviewer verdict. All real Euclidean translations, rotations and reflections
are allowed in the mathematical claims.

For the explicit unmarked Jordan-disc tile T below, we prove

\[
                       2\le H_c(T)\le H_h(T)\le85.
\]

The new result is a three-copy pattern that cannot lie strictly inside any
finite packing of congruent tiles. It also closes every route to three
coronas over the specified eleven-copy first prefix: **any second surround
of that first prefix cannot itself be strictly surrounded**, even allowing
holes and arbitrary real motions in both extensions. Different first
coronas remain unclassified. This is neither an exact Heesch-value theorem
nor a finite-seven construction or record claim.

## Geometry, motions and conventions

Use axial coordinates L(q,r)=(q+r/2,sqrt(3)r/2). The labelled vertices are

\[
 v_0=(0,0),\quad v_1=(0,-1),\quad v_2=(0,1),\quad
 v_{2j+1}=(j,-1),\quad v_{2j+2}=(j,1)\ (1\le j\le7),\quad
 v_{17}=(8,-1).
\]

Their counterclockwise cycle is

    0,1,3,5,7,9,11,13,15,17,16,14,12,10,8,6,4,2.

The quadrilateral's genuine angles at vertices1,17,16,2 are60,90,90,120
degrees; fourteen intermediate labels have angle180 degrees. Ports0..17
use the endpoint pairs below, directed counterclockwise in [input.json](input.json):

    0:(0,1)    1:(0,2)    2:(1,3)    3:(2,4)    4:(3,5)    5:(4,6)
    6:(5,7)    7:(6,8)    8:(7,9)    9:(8,10)  10:(9,11)  11:(10,12)
    12:(11,13) 13:(12,14) 14:(13,15) 15:(14,16) 16:(15,17) 17:(16,17).

The signs are

    1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,0.

On each physical unit port, from v to v+e in counterclockwise direction,
replace the chord by

\[
 v+ze+s_i(1/100)z^2(1-z)^2(e_y,-e_x),\qquad 0\le z\le1.
\]

Port17 remains straight of length sqrt(3). These profiles are actual
geometry; the finished tile has no artificial matching marks. The straight
quadrilateral alone tiles the plane and is not the finite candidate.

Let R(q,r)=(-r,q+r), J(q,r)=(q+r,-r). Pose(h,k,a,b) denotes
R^k J^h applied to the prototype, followed by translation(a,b). The finite
catalogues below concern only placements forced by specified contacts;
unrelated real motions, including sliding or split straight contacts,
remain unrestricted.

A corona is finite; its copies have disjoint interiors, each new copy
touches the preceding corona, and the previous cumulative prefix lies
strictly inside the new one. Hc requires disc prefixes; Hh may allow holes
in the final prefix. The obstruction and finite upper bound also apply to
the weaker convention allowing holes at every prefix.

## Geometric prerequisites and exact transfer

The [earlier quartic-contact proof](../heesch_weighted_matching_obstruction/quartic_realization.md)
establishes that a nontrivial shared subarc of these unit quartics forces
the full arc, both endpoints and opposite signs. Its polynomial argument
does not depend on a polyform grid. The homogeneous degree-four term fixes
the tangential axis; coefficient comparison fixes the tangential shift,
amplitude and normal displacement. Noncoincident transformed quartics have
only finitely many intersections; straight lines cannot share their arcs.
Thus every interior charged arc in a finite packing has one full
complementary mate. Partial or split charged contacts add no possibilities.

For a specified integral-D6 tile pose, such a mate has an integral-D6
pose: a complete unit chord fixes the orthogonal map up to its two hands,
and an endpoint fixes the translation. This is a local consequence, not
global locking of all tiles.

The [trapezoid-specific buffered-overlap proof](../heesch_trapezoid_extension_obstruction/proof.md)
shows that positive-area overlap of two forced quadrilateral skeletons
contains a physical disk of radius at least1/96. Primitive edge directions
have norm1 or sqrt(3), and determinants at most3. Intersection vertices
have axial denominators1,2,3; averaging at most eight gives determinant
slack at least1/48 and physical edge-line distance at least1/96.
The boundary deformation is at most1/1600, so this center stays inside
both actual curved tiles. Every such skeleton overlap is therefore a sound
curved-overlap exclusion. The checker independently audits the denominators,
slack and distance for every positive overlap used in the small proof.
No converse assertion about touching skeletons is needed.

For positive constructions, a separate network isotopy supplies the bridge.
Our witnesses have no skeleton overlap, every shared labelled port is
coincident with opposite signs, and each outside boundary is one simple
directed cycle. Exact integer point-to-segment distances give minimum
nonincident squared distance3/4 at both prefixes. Distinct incident rays
separate by at least30 degrees. The quartic displacement is at most1/1600;
its endpoint cone deviation is at most arctan(1/675), because
z(1-z)^2<=4/27 and the same bound holds at the other endpoint.
Twice the displacement is below the nonincident separation, and twice
the cone deviation is below30 degrees. Increasing the amplitude continuously
from0 to1/100 preserves the embedded network and its cyclic order.
Complementary arcs coincide throughout. Extending this isotopy over the
faces preserves the disc unions, nonoverlap and strict containment.

## The three-copy obstruction

Consider these three poses, in order:

    A=(1,4,8,-1), B=(0,0,0,0), C=(0,0,-2,2).

They are a nonoverlapping pattern. A congruent image occurs in the checked
second prefix below, so the pattern's actual curved realization is also
certified by that witness.

**Lemma.** No finite packing of congruent copies of T has all three
specified copies A,B,C strictly inside its union. No disc condition is
required on the larger union. A common real Euclidean isometry of the
entire pattern preserves the lemma.

Proof. Require complementary mates for only five exposed charged arcs:
A's port3 and B's ports10,6,2,1. Their signs are +,-,-,-,+. The checker
verifies that none is already paired within the three-copy pattern.
Enumerating every opposite-sign prototype port and both hands yields66
distinct raw poses. Exact whole-quadrilateral intersection with the three
old copies excludes47 and leaves19. All possible mates under arbitrary
real motions are included by the quartic-contact lemma. Other new copies
can be omitted from this necessary finite selection problem.

The five covering clauses have sizes1,5,9,13,1. Exact rational polygon
clipping finds134 positive whole-overlap pairs among the19 candidates.
Their negative binary clauses are sound by the uniform buffer. Direct
unit propagation on these five positive clauses and134 negative clauses
reaches a contradiction after assigning19 variables. It makes no choices
and does not call a SAT solver. The complete inventories and clause hashes
are reconstructed from the definition, rather than trusted as opaque input.
Every hypothetical finite strict surround would satisfy these clauses,
a contradiction. This proves the lemma. Additional flat-only or
vertex-only copies cannot remove it.

In discovery, a native280-variable necessary selector for the full36-copy
second prefix gave a20-clause core, all involving these five charged arcs
and positive skeleton overlaps. Projection against exactly A,B,C, with
the mate catalogues rebuilt, retained the identical19 relevant poses.
The public checker is a different implementation: Gram-column enumeration
replaces repeated rotations, rational half-plane clipping replaces
separating axes, and unit propagation replaces native solving. It does
not require the full native formula, trace, full-prefix filtering or solver.
Separately implemented checking by the same author is not peer review.

## Two complete disc coronas

[input.json](input.json) gives36 exact pose codes with levels0,1,2.
The first corona has10 copies; the second has25. Both cumulative prefixes
are discs. Their exact counts are

| prefix | cumulative copies | full interfaces | exposed ports |
|---|---:|---:|---:|
| first |11|61|76|
| second |36|255|138|

At every vertex of every previous-prefix copy, the checker reconstructs
the twelve30-degree tangent sectors and verifies complete nonoverlapping
coverage. No previous-copy port remains exposed. Every new copy has a
shared physical vertex with a preceding-level copy. The simple-cycle and
network-isotopy checks above transfer the complete skeleton construction
to the actual curved shape. Thus Hc(T)>=2 is proved by an exact witness,
not a picture or a necessary SAT model.

This eleven-copy first prefix differs from the
[previously excluded six-copy first prefix](../heesch_trapezoid_extension_obstruction/proof.md).
The older obstruction retains its original scope; a new first layout
permits two coronas without contradicting it.

## Every second surround over this first prefix stops before three

Fix the eleven poses of levels0..1 in the witness; their order is retained
in input.json. Any finite strict surrounding of them forces these three
additional poses:

    (0,4,8,-9), (1,2,16,-16), (1,2,18,-16).

The first is the unique mate of copy8's port1. Independent enumeration
gives16 raw opposite-sign mates; exact overlaps with the eleven old
copies leave only that pose.

The other two fill isolated90-degree gaps at(9,-8) and(11,-8). All
prototype angles are at least60 degrees, so each gap requires exactly
one90-degree vertex. An arc-interior sector has180 degrees and cannot fit.
Both90-degree prototype corners have one charged port and one straight
port. Each gap has one charged and one straight bounding side. Matching
the charged side invokes atomic contact, forcing an integral-D6 pose;
both geometric possibilities are enumerated. Complete sign/endpoint
compatibility and full footprints leave one at each point. The straight
side is endpoint-anchored and has the same length sqrt(3), so no sliding
degree of freedom remains for these particular fillers. Unrelated flat
contacts elsewhere are unrestricted. Finite nonincident copies have
positive clearance and cannot replace the local incident filler.

These three poses are exactly the image of A,B,C under the common pose
(1,2,16,-16). Every possible second surround therefore contains the
forbidden pattern. A further strict surrounding would put all three
copies in its interior, contradicting the lemma. This excludes every
arbitrary-motion second-to-third extension over the fixed first prefix,
even with holes. It also excludes extension of the displayed second prefix.
It makes no assertion about other first coronas.

A separate native208-variable lookahead had three transported pattern
clauses and a four-clause unit core: three forced providers and their
forbidden conjunction. The public proof checks the forced arc, both complete
90-degree pools and the common pattern embedding directly. That native
formula and its signed variable labels are not prerequisites.

## Finite upper bound, literature and remaining frontier

The previously proved all-arrangement upper bound85 applies to this
identical T, independently of the new first/second layouts. There are nine
positive and eight negative arcs. Cumulative prefixes satisfy
N(i+1)>=ceil(9N(i)/8). Area A=15sqrt(3)/2+1/3000>1299/100 and
diameter D<=sqrt(67)+1/800<6553/800 give

\[
 N_i\le\left\lfloor
 \frac{(22/7)(6553/800)^2}{1299/100}(i+1)^2\right\rfloor.
\]

The rounded recurrence requires130235 copies at depth86 but area allows
only122872. The public checker replays this arithmetic; the
[earlier proof](../heesch_trapezoid_extension_obstruction/proof.md)
supplies the analytic charging and contact-radius/area argument. Therefore
2<=Hc(T)<=Hh(T)<=85. No exact value or global no-third-corona theorem
is claimed.

The bump/nick imbalance mechanism is prior art in
[Mann2004](https://faculty.washington.edu/cemann/Heesch.pdf), including
hexapillar-five and polypillar-three families.
[Kaplan's paper](https://arxiv.org/abs/2105.09438) and
[author data](https://cs.uwaterloo.ca/~csk/heesch/) are bounded censuses,
not global bounds on all unmarked polyforms. The
[2025 account](https://arxiv.org/html/2509.12216v1) uses topological-disc
shapes and reports the connected finite record6. Theorem7 of
[Bašić–Džuklevski–Slivková2023](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v30i2p50/pdf/)
already realizes every positive finite Heesch number with two-part
disconnected tiles under relaxed conventions; that does not resolve the
connected-disc finite-seven frontier. The targeted literature check does
not establish historical priority for this low-Heesch profile family.

The complementary [fixed-fourth-prefix polyiamond work](../heesch_polyiamond_fixed_fourth_extension/proof.md)
uses different geometric patterns and has its own integral-fifth-layer
scope; no triangular-grid theorem is imported here. Its independently
developed pattern transport illustrates how compact interior obstructions
can eliminate construction branches. The broader
[local corner work](../heesch_polyomino_corner_obstruction/proof.md)
also keeps unrelated motions unrestricted. Neither publication reviews
this new trapezoid lemma.

The remaining task is to choose a different first layout or geometry and
obtain seven complete admissible coronas with a sound finite upper bound.
The new three-copy rule can prune any prospective inner layer containing
a congruent instance. A bounded necessary-selector SAT model, native
UNKNOWN or failure of an integral construction search is not a corona
or a universal exclusion.
