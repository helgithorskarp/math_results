# An all-motion upper bound of six for the curved trapezoid

**Agent six-heesch-3; role researcher; 2026-09-30.**

For the identical connected unmarked Euclidean Jordan disc T of the
[four-corona construction](../heesch_trapezoid_four_coronas/proof.md),

    4 <= Hc(T) <= Hh(T) <= 6.

This improves the campaign's previous upper85. It supplies no new lower
construction, exact height, shape, height record, independent review or
formalization. The tile T is now excluded from the finite-seven target.
Its fifth and sixth coronas remain unresolved. The next construction must
change the physical shape within the assigned connected-disc family.

## Tile, conventions and precise results

The physical tile is fixed by the byte-pinned
[input](../heesch_trapezoid_first_prefix_reduction/input.json) and
[realization proof](../heesch_weighted_matching_obstruction/quartic_realization.md).
Axial(q,r) means(q+r/2,sqrt(3)r/2). The skeleton is the trapezoid with vertices
(0,-1),(8,-1),(7,1),(0,1), subdivided into seventeen unit ports and one straight
sqrt(3) port. Seven upper and two left ports bow outward; eight bottom ports
bow inward. For each counterclockwise unit chord v+ze, the unchanged curve is

    v+ze+(s/100)z^2(1-z)^2(e_y,-e_x), 0<=z<=1,

with s=+1 on the nine positive ports and s=-1 on the eight negative ports.
These are physical curves, not matching marks. Let R(q,r)=(-r,q+r) and
J(q,r)=(q+r,-r). Pose(h,k,a,b) denotes R^k J^h with axial translation(a,b).
ROOT=(0,0,0,0). All initial real motions and reflections are permitted.
T has only the identity automorphism, as checked by the pinned parent.

A packing family consists of congruent closed T copies with disjoint whole
interiors. Cumulative families F0={ROOT},...,FH are nested, and their closed
unions Ui satisfy U(i-1) contained in int(Ui). For coronas every added copy
touches the preceding cumulative boundary; closed point contact suffices.
The negative argument imposes no topology conditions. It therefore applies
to both Hc (disc prefixes) and Hh (holes allowed in the final prefix), following
[Section2.1](https://cs.uwaterloo.ca/~csk/heesch/unmarked.pdf),
[Kaplan2021/2022](https://arxiv.org/abs/2105.09438) and the
[author data](https://cs.uwaterloo.ca/~csk/heesch/).

**Theorem.** No such arbitrary-topology chain has H>=7. In fact seven strict
surrounds are impossible even when the added-copy contact condition is
dropped, by the contact-graph-ball reduction below.

The exact first-family indices Ci are defined in the
[fifteen-family rigidity theorem](../heesch_trapezoid_prefix_rigidity/proof.md):
Ci is ROOT plus the parent candidate poses named by necessary_subsets[i].
Indices i are zero-based; entries inside each subset are one-based. The
entire first prefix in an admissible chain must belong to the following lists:

| Required coronas | Necessary exact first types |
| --- | --- |
|3|0,1,17,18,20,23,24,25,28,30,60,62,64,91,111|
|4|0,17,18,20,23,24,30,60,62,64|
|5|0,17,18,23,24,30,62|
|6|17,62|
|7|none|

Under H>=4, the entire second prefix belongs to thirty supplied necessary
families. Under H>=5, the third prefix belongs to forty-three necessary
families. These are complete necessary catalogs of whole placements; the
passing candidates are not asserted to be actual extendable coronas, discs,
or even complete compatible physical packings. Only the inherited four-corona
witness has its full positive geometry replayed here.

## Contact interiority and available depth after re-rooting

The Jordan-disc contact-interiority argument is written in the
[parent proof](../heesch_trapezoid_prefix_rigidity/proof.md), with the general
method credited to [P17 rigidity](../heesch_polyomino_third_prefix_reduction/proof.md).
If C is contained in the interior of a finite subpacking B of an ambient
packing P, any P tile touching C is already a B tile. At a contact point,
a small ball inside union(B) meets the prospective tile's interior in a
nonempty open set. Finitely many nowhere-dense Jordan boundaries cannot
cover that open set, so it meets a B-tile interior. Packing forces equality.
This handles point-only contact and every real orientation.

For completeness, re-root with a contact-graph ball, as in
[P17's fourth-corona proof](../heesch_polyomino_four_corona_frontier/proof.md).
Choose a copy A in Fj and take the finite contact graph of the ambient
family FH; vertices are whole copies and edges mean nonempty closed contact.
Let Gr be its radius-r ball about A and Nr its closed union. Induction and
contact interiority give Gr as a subfamily of F(j+r), for r<=H-j.
Indeed G(r-1) lies inside int(U(j+r)), so every ambient tile touching it lies
in F(j+r). Further N(r-1) is strictly inside Nr. The former is compact and
inside int(U(j+r)); every F(j+r) tile not touching it has positive distance
from it. The minimum of finitely many such distances, together with the
distance to the complement of int(U(j+r)), supplies a neighborhood covered
only by the contacting ball tiles. If there are no noncontacting tiles,
only the latter distance is needed. Every new ball tile touches the previous
ball by its graph distance. Such a contact is on the previous union's
boundary: a new packing tile cannot meet the interior of that finite union,
by the same Jordan-boundary argument.

Thus A has H-j re-rooted coronas with arbitrary topology. The first ball
is its entire ambient neighborhood and is completely inside F(j+1).
Any necessary first-type list valid for m coronas applies at A whenever
H-j>=m. The same construction starts from arbitrary nested strict-surround
families without the contact condition. Consequently impossibility for
the auxiliary arbitrary-topology coronas also excludes those general chains.

## A finite complete-neighborhood model

The pinned parent proves that three coronas force the ENTIRE first family
to be one of fifteen Ci, each an actual strict disc surround whose nonroot
copies touch the root. This covers every real-motion first family. An option
about a specified copy A is therefore exactly A*Ci under the unique common
isometry taking ROOT to A; no global pose window or new-copy bound is assumed.

Fix the root's first family C. In an H>=4 packing every A in C has three
re-rooted coronas, so choose one of fifteen complete-neighborhood options
about A. The reader independently regenerates every one of these choices.
An option is necessarily invalid if it:

* omits a known C tile touching A;
* includes a root-touching tile absent from C;
* conflicts with a C tile by buffered positive-area skeleton overlap or
  a common positive unit arc.

Between two chosen options, the same whole-copy conflicts are forbidden.
Also a chosen copy touching the other receiver must belong to that receiver's
COMPLETE neighborhood option. Identical pose codes denote the same physical
copy and are allowed to occur in multiple neighborhoods.

For contacts this reader uses only common physical labelled endpoints.
This is a sound sufficient contact witness, not an unproved complete test of
all skeleton or curved contacts. It may leave extra necessary candidates;
it cannot remove an actual packing. The physical endpoints are unchanged
by the quartic deformation. The same logic covers point contacts.

Buffered overlaps use the pinned uniform-overlap proof from the
[older upper-bound work](../heesch_trapezoid_extension_obstruction/proof.md).
The reader transforms each pair to a relative pose with the first tile at
ROOT, audits exact D6 matrix inversion/composition, then uses exact rational
clipping. Intersection vertices, center slack and edge distances certify
a common disk of radius at least1/96, above deformation1/1600. Common
positive arcs also cannot coexist by the pinned atomic-contact bridge.
No converse from skeleton disjointness to actual compatibility is used.

Every hypothetical packing supplies a surviving choice for each A. Moreover
their union is EXACTLY F2: each new F2 tile touches some F1 tile and hence is
in its complete neighborhood; conversely every ambient neighbor of an F1
tile belongs to F2 by contact interiority. This is the required completeness
direction for the finite catalog, independent of any constructor inventory.

The first reader uses bit-mask arc consistency and lexical branching on this
finite binary-constraint model. Discovery used direct Cartesian products.
All domains and pair restrictions are recomputed; no saved discovery masks,
rejection logs, pose windows or solver verdicts are trusted. Canonical
entry-by-entry comparison to [certificate.json](certificate.json) rejects
an omitted model, not merely a wrong aggregate count.

The raw first-domain products total1270. Exactly30 vectors remain, yielding
30 necessary second families and the ten first types in the H>=4 row above.
Their counts by first type are1,2,2,1,3,1,2,2,15,1 in that row's order.

## The complete height-five third-prefix census

If H>=5, every F1 tile has four re-rooted coronas. Its neighborhood type must
therefore belong to the ten-type H>=4 list. Restrict the thirty vectors to
those types. This leaves23 necessary second states over nine first types
`0,17,18,20,23,24,30,60,62`; type64 already has no such vector.

Fix one of those F2 states. Each previously classified F1 tile keeps its
complete neighborhood assignment. Every NEW F2 tile has three re-rooted
coronas, so its neighborhood has one of the original fifteen types. The
reader generates all15 options, rejects necessary conflicts with F2 and
the fixed old neighborhoods, then checks the direct Cartesian product of
the remaining new-frontier domains. Between new options it checks the same
whole-copy and complete-neighborhood restrictions. Its entire union is F3,
by the identical contact-interiority and corona-contact argument.

The23 states give98466 products after fixed-neighborhood constraints.
Every product is checked; no guard, sampled branch, incomplete enumeration,
supplied assignment, SAT verdict or external search file proves a negative.
The public reader keeps every assignment, checks that no different assignment
was silently represented by the same family, and compares the complete
sorted whole-pose catalogs. Discovery instead used MRV prefix DFS, reusing
global-coordinate conflicts. Relative-coordinate geometry, bit-mask first
enumeration and direct frontier products provide a separate reader, while
the shared pinned primitive code is expressly disclosed.

Exactly43 third-prefix models remain:

| First type | Third-prefix models under H>=5 |
| --- | ---: |
|0|1|
|17|1|
|18|1|
|20|0|
|23|2|
|24|1|
|30|1|
|60|0|
|62|36|

Thus five coronas force the seven-type list

    L5={0,17,18,23,24,30,62}.

This statement permits arbitrary intermediate topology; disc or hole pruning
never supplies an exclusion. Passing model families are necessary candidates,
not proved five-corona constructions.

## Two finite refinements finish the upper bound

Let M be the verified thirty first-neighborhood vectors. For a valid
first-type set L define

    Phi(L)={i in L: some (i,vector) in M has every vector entry in L}.

If H>=m+1 and L is necessary under m coronas, each A in the first prefix
has m re-rooted coronas. Its entire neighborhood type lies in L. The root's
vector therefore has every entry in L and its own type is in L as well.
This proves that Phi(L) is necessary under m+1 coronas. It is a finite
necessary deduction, not a presumed tiling-state automaton or converse.

The reader verifies, entry by entry,

    Phi(L5)={17,62},
    Phi({17,62})=empty.

The first equality is a necessary first-family list for six coronas; the
second rules out seven. No eighth-corona computation, transferred grid bound
or assumed integrality of the final two layers is needed. The root has no
possible neighborhood type, contradicting any seven-corona chain. Together
with the old actual four-corona witness, this proves4<=Hc<=Hh<=6.

## Reproduction, controls, context and changed construction

From repository root run:

```sh
python3 -B heesch_trapezoid_six_upper_bound/check.py --expected heesch_trapezoid_six_upper_bound/expected.json
python3 -B heesch_trapezoid_six_upper_bound/check.py --controls
```

CPython3.11+ standard library only. Assertions are required by disclosed
pinned parents; -O is rejected. The reader first replays the whole15-family
proof, its100 exclusions and115-subset prerequisite, and the known actual
147-copy four-corona packing. Its first C0, second45 and third94 prefixes
remain in the appropriate necessary catalogs. Presence of the third94 in
the height-five relaxation does not establish a fifth corona.

Six malformed controls reject an omitted local type, discarded third
surround, omitted first model, omitted third model, shifted whole pose and
false six-corona type elimination. The compact certificate supplies only
the30/43 catalogs and type lists; the reader regenerates all domains and
constraints. No native solver, dense formula, private discovery code,
large corpus, raw log, key or ledger is needed. Ordinary exact Python,
written atomic/buffered/isotopy bridges, contact interiority and the
contact-ball/completeness arguments remain trust boundaries. This is author
validation rather than an independent reviewer verdict or formal proof.

The complete-neighborhood compatibility method is credited to
[P17's fourth-frontier proof](../heesch_polyomino_four_corona_frontier/proof.md).
The newer [P17 three-first-family reduction](../heesch_polyomino_three_first_corona_frontier/proof.md)
and [T214 second-prefix closure](../heesch_polyiamond_second_prefix_closure/proof.md)
are complementary different-tile work. Their source proofs and available
committed bodies were read; their geometry is not a T premise and their
checkers were not replayed. No reviewer target or verdict was requested.

[Kaplan2025](https://arxiv.org/html/2509.12216v1) gives connected-disc record
context through six; [Mann2004](https://faculty.washington.edu/cemann/Heesch.pdf)
already qualifies the generic unmarked finite-five seed. The standing
[disconnected arbitrary-height qualification](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v30i2p50)
does not settle the connected-disc finite-seven target. No exhaustive2026
priority claim is made. This result closes the existing T as a target route.
A changed connected physical construction, with actual seven coronas and
a sound finite upper obstruction, is the continuing frontier.
