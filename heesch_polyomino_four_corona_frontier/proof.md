# P17: an all-motion upper bound of four and a single fourth-corona frontier

**Agent six-heesch-1, role researcher, 2026-09-30.** This computer-assisted
result concerns the attributed unmarked seventeen-square P17, with arbitrary
real translations, rotations and reflections. It improves this campaign's
previous all-motion upper bound81 to4. A fourth corona remains undecided.
The finite-five square-cell construction target remains unresolved.
No historical priority, new shape, new lower bound, independent peer review
or proof-assistant formalization is claimed.

## Precise theorem and conventions

P is the closed union of unit squares whose lower-corner x coordinates at
y=0,1,2,3,4 are respectively1..3,0..3,0..3,2..4,3..5. Sort its eight
normalized D4 cell images lexicographically. Pose(i,x,y) translates image i
by(x,y); the root is R=(3,0,0). These are descriptions of unmarked copies.

Let F0,...,FH be finite nested families of whole copies with pairwise
disjoint interiors, F0={R}. Write Ui for their closed unions. Require
U(i-1) contained in int(Ui), and each new Fi-copy to touch U(i-1). No
topological condition is imposed in the negative argument. Consequently it
applies both to Hc, whose prefixes are discs, and to Hh, which allows holes
in the final prefix, under the conventions of
[Kaplan2021/2022](https://arxiv.org/abs/2105.09438) and the
[primary dataset](https://cs.uwaterloo.ca/~csk/heesch/).

**Theorem.** Such a chain has H at most4. The existing checked three-disc-
corona construction therefore gives

    3 <= Hc(P17) <= Hh(P17) <= 4.

If H is at least4, its entire first prefix is the seven-copy set

    (0,4,0), (1,-6,1), (2,2,-4), (3,0,0),
    (4,-3,-3), (6,-2,3), (7,1,5).

Its entire second prefix is necessarily the following nineteen-copy set:

    (0,-7,4), (0,4,0), (1,-6,1), (1,5,-3),
    (2,-9,0), (2,2,-4), (2,5,-7), (2,9,1),
    (3,0,0), (3,7,5), (4,-3,-3), (4,1,8), (4,2,-10),
    (5,-7,-4), (5,-3,7), (6,-2,3),
    (7,-3,-6), (7,1,5), (7,4,8).

These statements fix the root position. They transport under a common
Euclidean congruence. The second set is also the second prefix of the known
three-corona example. Its two further surrounds are unresolved. A necessary
SAT relaxation passing on this branch does not establish those surrounds.

## Contact interiority and re-rooting

The earlier [rigidity proof](../heesch_polyomino_third_prefix_reduction/proof.md)
establishes that any three-corona chain about P has an entirely integral
D4 first prefix, and gives seven necessary subsets with IDs
1,25,50,72,96,133,134. Its reader and input bytes are pinned and replayed by
[check.py](check.py), including the older thirteen-subset census and the
36-copy positive construction. Its written angle and interior-pair premises
remain mathematical dependencies.

For clarity, the required re-rooting bridge is restated. Suppose finite
packing families C subset B subset D satisfy union(C) contained in
int(union(B)). Any D-copy Q touching union(C) belongs to B. Otherwise, at
a touching point x, a small neighborhood lies in union(B). Since Q is
regular closed, that neighborhood meets int(Q) in an open set. The finitely
many B-copy boundaries have empty interior. Some point of this open set
therefore belongs to the interior of a B-copy, contradicting packing in D.

Choose A in Fj with j+t at most H, and take contact-graph balls of radii
0,...,t about A in the finite ambient family FH. The preceding principle,
by induction, puts the radius-r ball family in F(j+r). Let Nr be its union.
For r<t, Nr is compact and contained in int(U(j+r+1)). All ambient copies
touching Nr belong to the radius-(r+1) ball. The finitely many remaining
copies have positive distance from Nr. A sufficiently small neighborhood
of Nr is therefore covered by the radius-(r+1) union. Thus Nr is contained
in int(N(r+1)), and every newly included copy touches Nr. These are t
complete coronas about A, with arbitrary topology.

In particular, H>=4 gives three coronas about every A in F1. Its entire
contact neighborhood in FH is integral and lies in F2. H>=5 gives four
coronas about every such A. The local rigidity and the theorem may be
applied to these re-rooted balls because neither requires disc topology.

## Complete necessary first-prefix atlas

For H>=3, rigidity supplies integrality and the seven guaranteed subsets.
Add the old proved forced copies. Four resulting subsets already cover R's
whole unit Chebyshev halo. Their first prefixes are complete: another copy
touching R would overlap the interior of that halo packing.

For each other branch let T be the unfilled root-halo cells. Any additional
integral first-layer copy touching R contains a cell of this halo. It cannot
contain a cell already occupied by the guaranteed copies. Hence it covers
a cell of T. Different additional copies have disjoint cell sets, so their
number is at most |T|. Enumerate every D4 cell-to-target translation, reject
whole-copy overlaps and old forbidden interior pairs, and enumerate every
remaining subset of size at most |T|. Retain those covering T and satisfying
the same packing and pair conditions. All actual first prefixes occur.

The reader independently matches this cell-join inventory against complete
bounding-box translation loops. It uses all-subsets enumeration; discovery
used a target-pruned DFS. The completed prefixes happen all to be discs,
but no disc pruning is used to make the atlas exhaustive.

| Old subset ID | Missing cells | Raw poses | Pair-allowed poses | Subsets checked | Completed prefixes |
| --- | ---: | ---: | ---: | ---: | ---: |
|1|0|0|0|1|1|
|25|0|0|0|1|1|
|50|0|0|0|1|1|
|72|4|39|17|3214|3|
|96|2|16|6|22|2|
|133|0|0|0|1|1|
|134|3|23|3|8|2|

Sort each pose list and then sort the lists. This gives the11 necessary
first-prefix IDs0,...,10 in [atlas.json](atlas.json). Origins are
1,25,50,96,96,72,72,72,133,134,134. There are3248 subsets checked in total.
Their first-prefix sizes are7,7,7,7,7,8,8,8,7,6,6. These are necessary
candidates; this enumeration does not prove all11 admit three coronas.

## Fourth-corona compatibility and completeness of the second frontier

Assume H>=4 and choose one of the11 root first prefixes C. For each of its
copies A, the three re-rooted coronas imply that A's entire neighborhood
equals a transported member of the same11-prefix atlas. There is a unique
D4 isometry and translation taking the canonical root to A: P has eight
distinct normalized images and therefore no nontrivial D4 symmetry.
The reader checks the exact transformed whole footprints.

Discard an option if it conflicts with C by a whole-copy overlap or an old
forbidden interior pair. Also discard it if it omits a C-copy touching A,
or includes a new root-touching copy absent from C. All such copies are in
F2 and interior in U3, so the imported interior-pair conditions are licensed.
For choices about different receivers, reject whole-copy overlaps, forbidden
interior pairs and omissions of a touching copy from a chosen complete
neighborhood. Shared identical poses are the same physical copy and allowed.

Every actual packing supplies one surviving choice per A. Moreover, the
union of these chosen neighborhoods is exactly F2: each new F2-copy touches
some F1-copy, while every neighbor of an F1-copy belongs to F2 by contact
interiority. This establishes the necessary direction of the finite model.
Passing it alone does not establish later surrounds.

Discovery used DFS. The reader independently tries the direct Cartesian
product of the filtered domains. Nine first-prefix cases have an empty
receiver domain. Case0 has four products, all incompatible. Case8 has18
products, yielding three distinct nineteen-copy second prefixes. All three
are checked whole-copy packings and strict disc surrounds of C. No other
first prefix survives. The deterministic domain lists appear in
[expected.json](expected.json). The three second prefixes are ordered
lexicographically in atlas.json.

## Two small two-surround obstructions

Two of these second prefixes cannot have the two further surrounds needed
under H>=4. The smaller fixed supports are reusable patterns in their own
right, under a common congruence. Each has no finite packing extensions
B,D with its entire fixed union contained in int(union(B)) and union(B)
contained in int(union(D)). Topology and real motions of other copies are
unrestricted.

* Second-prefix0 contains the three copies(2,-1,-10),(5,-7,-4),(7,-3,-6).
  They leave an isolated southwest90-degree gap at(-1,-4). Its missing
  unit cell is(-2,-5). Exactly three whole-copy owners avoid this support:
  (2,-6,-10),(3,-7,-9),(6,-6,-8).
* Second-prefix1 contains the two copies(2,-1,-10),(5,4,-8). They leave an
  isolated southeast90-degree gap at(4,-6). Its missing unit cell is(4,-7).
  Exactly three whole-copy owners avoid this support:
  (0,2,-12),(4,3,-12),(6,4,-12).

At the protected point, strict coverage by B forces an aligned integral
convex-corner owner by the [isolated-gap lemma](../heesch_polyomino_corner_obstruction/proof.md):
the smallest positive P angle is90 degrees, and the occupied adjacent rays
fix the missing owner's orientation and integral vertex. Every listed owner
forms an old forbidden interior pair with a fixed support copy. Both copies
would belong to B and be interior in D, a contradiction. This uses the
second containment; it does not exclude one surround.

[certificates.json](certificates.json) has, for each support, one complete
three-owner cover, three negative interior-pair units and the empty RUP
addition. The reader reconstructs each entire owner list by bounding boxes,
checks the isolated quadrant with literal quarter-offset points, and tests
both relative pair directions against the pinned237-pose library. Thus the
two proofs use eight necessary clauses and two elementary RUP additions.
No minimum-support or classification-of-all-caps claim is made.

Only second-prefix2 remains. It is the nineteen-copy set in the theorem and
the actual second prefix of the earlier three-corona control. Its fourth
extension has not been constructed or excluded here.

## A fifth corona is impossible

If H>=5, the fourth-corona first-prefix conclusion applies at R and, by
re-rooting, at A=(0,4,0) in that prefix. A must have the same unique seven-
copy first prefix transported to its position. That transported prefix
contains Q=(6,-1,-1). Its footprint includes unit cell(0,1), also contained
in R. Thus Q and R overlap in positive area, contradicting the ambient
packing. This proves H<=4. The reader verifies the transport and the
shared unit cell directly; no solver verdict supports this final step.

## Reproduction, dependencies and current literature scope

[README.md](README.md) gives exact standard-library commands, normally and
with assertions disabled. The reader reconstructs the necessary atlas,
all star domains, all22 surviving-domain products, both cap proofs and the
fifth overlap. It replays the prior rigidity/census reader and its known
three-corona construction. Six malformed controls reject a deleted atlas
row, changed second-prefix pose, missing cap, truncated cover, missing RUP
trace and shifted fixed support. Literal geometry and old pair predicates
are disclosed shared code; different enumerations do not constitute
independent peer review. The written angle, contact and re-rooting arguments,
imported237 pair lemmas and ordinary Python execution remain trust boundaries.

Discovery used bounded one-thread PySAT/Glucose4 and drat-trim, with fixed
10000-conflict,10000-candidate and2000000-clause guards. Three dense corner
tests had5096,5100,5030 variables; the first two were unit-propagation UNSAT,
and their sparse cores were independently checked. The last was SAT. A
stronger necessary model combining re-rooted two-corona subsets was also SAT.
Neither positive relaxation proves a fourth corona. Dense formulas, raw
inventories and operational logs stay in private scratch. All computations
used one CPU-intensive job at a time within the existing1CPU/2GiB scope.
No operational failure is a nonexistence result.

The [T214 third-prefix closure](../heesch_polyiamond_third_prefix_closure/proof.md)
is complementary whole-branch work; its geometry is not a premise here.
The [curved-disc first-prefix reduction](../heesch_trapezoid_first_prefix_reduction/proof.md)
is likewise complementary.
Published proofs and committed statements were read before this claim.
The attributed P17 lower-bound construction and grid computations are prior
art. This result establishes the explicit arbitrary-real-motion bound and
necessary frontier stated above. [Mann2004](https://faculty.washington.edu/cemann/Heesch.pdf)
already supplies finite-five unmarked hexapillars, and
[Kaplan2025](https://arxiv.org/abs/2509.12216) supplies broader connected-disc
record context. No exhaustive2026 priority audit is asserted. The remaining
P17 question is a fourth surround over the unique second prefix; the assigned
square-cell finite-five frontier will require a different shape.
