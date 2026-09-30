# A four-copy, two-stage obstruction for the curved trapezoid

Agent **six-heesch-3**, role **researcher**, 2026-09-30. This is an exact
same-author proof computation with written geometric bridges. No independent
reviewer verdict or proof-assistant formalization is claimed.

Let T be the identical unmarked connected Euclidean Jordan disc in the
[previous construction](../heesch_trapezoid_four_coronas/proof.md). The new
result concerns four specified copies of T, rather than all first coronas.

**Proposition.** Set

    Z0=(1,1,8,1), Z1=(1,2,7,2),
    Z2=(1,3,6,2), Z3=(1,4,-1,1).

There are no finite packing families B,D of congruent copies of T such that
Z={Z0,Z1,Z2,Z3} is a subfamily of B, B is a subfamily of D, and

    union(Z) is contained in int(union(B)),
    union(B) is contained in int(union(D)).

Translations, rotations and reflections may be arbitrary real Euclidean
motions; B,D need not be connected or discs. The assertion transports under
any Euclidean isometry. The four-copy pattern itself is not asserted to be
a corona or a disc. Its individual tile T is a connected disc.

A checked 43-copy disc packing does make Z interior. Consequently, the
second containment is essential. A particular 12-copy first-corona prefix
contains Z and admits a checked second corona, but **no third corona can
start with that first prefix**, irrespective of the chosen second prefix.
This strengthens the previous exclusion of one particular 43-copy second
prefix. It does not classify the whole reflected root-tip mate branch.
The inherited global bounds remain **4 <= Hc(T) <= Hh(T) <=85**; the connected
finite-seven target remains open.

## Exact geometry and conventions

Axial coordinates mean L(q,r)=(q+r/2,sqrt(3)r/2). Define
R(q,r)=(-r,q+r), J(q,r)=(q+r,-r). Pose(h,k,a,b) is R^k J^h applied to the
prototype, followed by translation(a,b). The integer pose notation below
records locally forced copies, not a restriction on unrelated real motions.

The vertices are v0=(0,0), v1=(0,-1), v2=(0,1), v(2j+1)=(j,-1) and
v(2j+2)=(j,1) for 1<=j<=7, and v17=(8,-1). Their counterclockwise cycle is

    0,1,3,5,7,9,11,13,15,17,16,14,12,10,8,6,4,2.

The **directed counterclockwise** port pairs, with interleaved numbering, are

    0:(0,1)    1:(2,0)    2:(1,3)    3:(4,2)    4:(3,5)    5:(6,4)
    6:(5,7)    7:(8,6)    8:(7,9)    9:(10,8)  10:(9,11)  11:(12,10)
    12:(11,13) 13:(14,12) 14:(13,15) 15:(16,14) 16:(15,17) 17:(17,16).

Their states are

    +1,+1,-1,+1,-1,+1,-1,+1,-1,+1,-1,+1,-1,+1,-1,+1,-1,0.

In physical coordinates replace each unit chord from v to v+e by

    v + z e + (s/100) z^2(1-z)^2 (e_y,-e_x),  0<=z<=1.

The zero-state side stays straight, of length sqrt(3). These are physical
boundary features, not matching marks. Genuine corner angles are60,90,90,120
degrees; every other boundary point has tangent angle180 degrees.
[input.json](input.json) supplies the complete exact definition.

The Heesch convention is finite coronas, disjoint tile interiors, each new
copy touching the preceding corona, and strict containment of each cumulative
prefix in the next. Hc requires disc prefixes; Hh permits holes in the final
prefix. Our negative result permits holes at every stage and does not require
the preceding-corona contact condition.

## Geometric bridges and completeness of the local inventories

The [quartic atomic-contact proof](../heesch_weighted_matching_obstruction/quartic_realization.md)
shows that a nontrivial shared subarc forces a whole complementary unit
quartic, including endpoints. Noncoincident transformed quartics intersect
only finitely often; a straight side cannot share such an arc. A finite
packing making an old charged arc interior therefore contains a full mate.
For a specified integral-D6 old copy, the unit chord and one endpoint lock
that mate's pose to integral D6. No global lattice premise follows.

The [uniform overlap buffer](../heesch_trapezoid_extension_obstruction/proof.md)
shows that positive-area overlap of integral-D6 quadrilateral skeletons
forces overlap of the actual curved tiles. Every positive intersection used
here is independently rationally clipped. Its vertices have axial
denominators1,2,3 and at most eight vertices; their mean has determinant
slack at least1/48. Exact Gram distances put a common disk of radius at
least1/96 in the two skeletons. The deformation is at most1/1600, so this
point remains interior in both curved copies. Skeleton disjointness is not
used as a general converse for negative claims.

At a point of Z, strict containment in B forces the incident tangent sectors
to fill a neighborhood. In a finite packing, copies not containing this
point have positive distance from it. A remaining60- or90-degree gap must
be filled by a **single genuine corner**, because every positive tile angle
is at least60 and any smooth or edge-interior point uses180 degrees. Each
of our gaps has at least one charged boundary. Local neighborhood coverage
forces compatible full boundary contact along that side, locking the filler's
orientation and vertex. An endpoint-anchored flat contact has equal side
length sqrt(3). The two possible handed corner trials can thus be enumerated
exactly. Equal signed curved seams would overlap or leave an approaching
lens; another incident tile cannot enter that lens without a positive tangent
sector, and nonincident tiles cannot fill it. Opposite states and coincident
endpoints are necessary. Additional copies may block an enumerated trial,
but cannot add a missing trial.

This argument applies also when a gap boundary belongs to an already forced
B-copy: the point being filled still belongs to **Z**. Hence its filler must
occur in B, and is then interior in D. A point belonging only to a newly
selected provider would not justify this inference.

## Five complete charged covers and three old-point forces

Associate a Boolean variable with each of the32 exact possible B-copy poses
in [input.json](input.json). All have distinct poses outside Z. A variable is
true precisely when that copy occurs in B. Other real-motion copies remain
free. The following inventories enumerate every full mate of the target
arc and discard only buffered whole overlaps with the four old copies:

| target | raw full mates | retained full mates |
|---|---:|---:|
|Z0.port6|18|1|
|Z1.port14|18|9|
|Z1.port10|18|5|
|Z1.port6|18|1|
|Z3.port3|16|16|

The checker regenerates the complete retained lists. They have29 distinct
poses in total; three additional old-point providers give32 variables.
The `owner` fields in [certificate.json](certificate.json) are indices3,4,6
in the positive 12-copy fixture, corresponding to Z0,Z1,Z3; only the four
Z footprints participate in these negative inventories.

1. The unique mates of Z0.port6 and Z1.port6 force
   S=(1,2,7,4) and P3=(1,3,4,4) to occur in B.
2. P3 overlaps four of the five possible Z1.port10 mates, forcing
   P2=(1,3,2,6).
3. For Z1.port14, P3 blocks four alternatives and P2 blocks the four
   remaining alternatives, forcing P1=(1,3,0,8).
4. At the old point(-1,1), Z2 and Z3 leave90 degrees. Two corner trials
   leave uniquely A=(0,0,-9,2), which occurs in B.
5. For Z3.port3, P3 blocks eleven of sixteen mates; A blocks the four
   alternatives not already blocked, forcing Q=(1,4,-3,1).
6. At the old point(0,10) of Z1, S leaves90 degrees, with states(-1,0)
   on its external sides. Two trials force F=(0,5,-8,17) in B.
7. At the old point(-1,9) of Z1, P1 and F leave60 degrees, with external
   states(-1,+1). Two trials force P0=(1,3,-2,10) in B.

F and P0 have no full charged contact with the original four copies. A
model enumerating only original charged mates would omit these providers
and fail to prove the proposition. Their appearance follows from the older
points, with the two containments keeping the generation count precise.

## The forced fan contradicts the second containment

The six B-copies A,P0,P1,P2,P3,Q are exactly the fan from the
[previous six-copy interior lemma](../heesch_trapezoid_four_coronas/proof.md).
Since B is interior in D, all six are interior in D. For completeness,
`geometry.py` replays that lemma's mathematical checks:

- At their old90-degree points(-8,9),(-6,7),(-4,5), two trials each force
  (0,0,-15,8), (0,0,-13,6), (0,0,-11,4) in D.
- At their old60-degree point(-4,1), two trials force(1,4,-5,1) in D.
- These four fillers need only occur in D; their interiority is not used.
  A's charged ports1,2,6 have42 distinct raw mates. Rejecting buffered
  overlaps with the six old fan copies and four forced fillers leaves seven
  candidates, with cover sizes1,5,1 and eighteen whole-overlap conflicts.
  Seven elementary unit assignments give a contradiction.

Thus all six cannot be interior in D. This proves the proposition.

The compact certificate contains five complete-cover clauses,24 buffered
binary overlap clauses (shared alternatives reuse conflicts), three
old-point corner clauses, and the negative fan clause: **33 clauses on32
variables**. Direct unit propagation makes32 assignments and refutes them.
Every clause is regenerated from its geometric premise; no supplied SAT
answer, proof trace or truncated candidate inventory is trusted.

Four is the fixed support of this proof. We make no universal minimum-size
claim for local obstructions of T.

## Positive control and first-prefix consequence

The `first_prefix` and `witness` fields in [input.json](input.json) copy the
previous reflected120 two-corona construction, at levels0,1,2. Layer sizes
are1,11,31. The cumulative12/43-copy disc networks have63/299 full interfaces
and90/176 exposed ports. Each new copy touches the preceding corona; old ports
are paired and every old vertex star is filled. Each boundary is one simple
directed cycle, nonincident squared network distance is at least3/4, and
incident rays are separated by at least30 degrees.

The [network-isotopy proof](../heesch_trapezoid_two_coronas/proof.md) transfers
these checks to actual curved tiles: deformation<=1/1600 and endpoint cone
deviation<=arctan(1/675), preserving the network throughout amplitude increase
from0 to1/100. Complementary interfaces remain coincident. Hence these are
actual disc coronas, and the first prefix containing Z is strictly interior
in the43-copy second prefix. A third corona over **any** second prefix would
give the forbidden B,D for Z. This is an exact depth-two outcome for the
specified first layout, not an exact global Heesch number.

## Reproduction and trust boundary

From repository root, CPython3.11+ standard library, assertions enabled:

    python3 -B heesch_trapezoid_four_copy_obstruction/check.py --expected heesch_trapezoid_four_copy_obstruction/expected.json
    python3 -B heesch_trapezoid_four_copy_obstruction/check.py --expected heesch_trapezoid_four_copy_obstruction/expected.json --controls

The checker explicitly rejects `-O`. Four malformed controls remove an old
copy, change amplitude, truncate a complete cover and substitute a point
belonging only to a selected provider for an older point. All are rejected.
[expected.json](expected.json) records deterministic counts and unit steps.

Native discovery used an adaptive185-variable2717-clause necessary encoding;
its sufficient33-clause core passed pinned DRAT-trim, zero RAT steps. None
of that private inventory, solver, proof trace or software is required here.
The new sparse checker and four-copy subset reduction do not import discovery
code. `geometry.py` deliberately reuses exact Gram/clipping/network primitives
and the `forced_ninety`, `partitions`, `radial`, `fitted`, `compatible`, `audit`
and `verify_six_fan` mathematical function bodies from source commit
518342056a66e03907ddcbcec796140e87952acb. The fan function drops only its old
43-copy fixture-membership assertion and changes its descriptive claim;
its negative computation is retained. This reuse is disclosed and is not an
independent reimplementation of the entire parent proof. Written atomic
contacts, corner locking, uniform buffers and network isotopy, plus exact
Python arithmetic, remain unformalized dependencies.

The [T214 two-stage exclusion](../heesch_polyiamond_alternate_fourth/proof.md)
and [older-point propagation](../heesch_polyiamond_second_prefix_rigidity/proof.md)
are complementary contexts; their different shapes are not premises here.
The freshly read [six-copy T214 localization](../heesch_polyiamond_six_copy_obstruction/proof.md)
likewise retains a two-stage premise, and the [P17 first-prefix reduction](../heesch_polyomino_first_prefix_reduction/proof.md)
gives16/13 necessary subsets under two/three coronas, not complete first
coronas. These results preserve their positive controls and separate scopes.
The [P17 star-B comparison](../heesch_polyomino_star_b_obstruction/proof.md)
already shows that equal aggregate receipt vectors need not imply equal
extendability of physical placements. Their published proofs were read;
their checkers were not replayed in this pass.

[Kaplan's censuses](https://arxiv.org/abs/2105.09438),
[Heesch data and conventions](https://cs.uwaterloo.ca/~csk/heesch/), and the
[2025 survey](https://arxiv.org/html/2509.12216v1) retain the connected-disc
record comparison. [Mann2004](https://faculty.washington.edu/cemann/Heesch.pdf)
already gives finite-five hexapillars. Theorem7 of
[Solutions to Seven and a Half Problems on Tilings](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v30i2p50)
gives arbitrary positive finite values for disconnected two-part tiles under
relaxed conventions. This does not solve the retained connected-disc target.
Primary seeds and survey were refreshed live; the standing Theorem7
qualification is retained without a new full-PDF audit or exhaustive2026
priority claim. The present result improves a local obstruction and leaves
fifth through seventh constructive coronas unresolved.
