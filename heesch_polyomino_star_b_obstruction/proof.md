# A placement-sensitive second-generation obstruction for P17

Agent **six-heesch-1**, role **researcher**, 2026-09-30. This is a written
geometric reduction with exact finite certificates and a checker implemented
separately from discovery. No independent peer review or formalization of
this result is claimed.

Let P be the unmarked seventeen-square disc with unit-cell lower corners
having x ranges, at y=0,...,4,

    1..3, 0..3, 0..3, 2..4, 3..5.

It is the attributed P17 example in Kaplan's
[paper](https://arxiv.org/abs/2105.09438) and
[dataset](https://cs.uwaterloo.ca/~csk/heesch/), record44 of the
[seventeen-cell list](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.txt).
Copies have disjoint whole interiors and allow arbitrary real translations,
rotations and reflections. The shape has no edge markings.

A copy is interior if its entire closed polygon lies inside the interior
of the finite packing union. An incoming provider of R is a copy whose
270-degree reentrant corner coincides with a 90-degree convex tip of R;
their sectors complement one another. The first provider generation contains
all actual incoming providers of R. The second contains all actual incoming
providers of those first providers. These are geometric contacts, not labels
that constrain allowed placements.

Normalize each D4 image by subtracting its coordinate minima, sort the
unit-cell lower corners, and sort the eight resulting lists to index the
orientations. A code(i,x,y) means orientation i translated by(x,y). P is
orientation3. Consider these four fixed copies, called star B:

| copy | i | x | y |
| --- | ---: | ---: | ---: |
| R | 3 | 0 | 0 |
| Q1 | 0 | 4 | 0 |
| Q2 | 6 | -2 | 3 |
| Q3 | 7 | -3 | -3 |

The Q copies are incoming providers of R. They receive five distinct tips,
with intrinsic source-corner receipt vector(1,2,2,0,0). This is the B
placement in the earlier
[weighting obstruction](../heesch_polyomino_weighted_obstruction/proof.md).
The five source labels order P's reentrant vertices lexicographically:
(1,1),(2,3),(3,4),(4,3),(5,4). A weight belongs to a copy's intrinsic source
corner and is transported by that copy's unique D4 isometry.

**Lemma.** No finite packing containing this fixed star B makes R, all
actual first-generation providers, and all actual second-generation
providers interior. Additional providers are allowed; the final union may
have arbitrary topology.

**Placement distinction.** Replacing Q3 by orientation4 at(-3,-3) gives
star D. A compact, previously published three-corona packing realizes D,
with all actual first- and second-generation providers interior. Its
receipt vector is also(1,2,2,0,0). Therefore the lemma excludes the B
placement, not its entire receipt-vector class.

## Necessary corner constraints

At a270/90 contact the rays align with the integer receiver's axes, and
vertex coincidence locks the provider to an integral D4 pose. Each fixed
receiver has56 incoming poses. Their absolute union has218 poses. Excluding
the fixed copies and every full-footprint overlap with their union C leaves
97 conditional providers. Any of these that occurs is interior under the
lemma's hypothesis: it is incoming to R or to one of its fixed Q providers.

At a required-interior integer vertex, an empty quadrant with both cyclic
neighbors occupied is an isolated90-degree gap. A filling copy must place
a convex90-degree vertex there: P's positive boundary angles are at least
90 degrees, and a straight-edge sector cannot fit. The sector rays and
vertex coincidence force an integral D4 pose, covering the adjoining unit
cell. This is the all-motion gap argument in the earlier
[corner theorem](../heesch_polyomino_corner_obstruction/proof.md).

Take every such gap at C's cell vertices. For a conditional provider q,
also take the gaps at q's vertices relative to C union q, required only
when q occurs. Include all integral D4 copies avoiding C and covering
any target, together with all97 conditional providers. This gives a complete
2944-candidate inventory. Each occurrence has one Boolean variable. Require
unconditional covers, conditional covers, and nonoverlap on entire
footprints. Apply the previously proved237 interior-pair exclusions only
to fixed or conditional copies whose interiority is licensed. Ordinary
outer fillers are not assumed interior.

A hypothetical packing selects its occurring conditional providers and
the integral fillers forced at active isolated gaps. Their complete
footprints satisfy all these constraints. Other copies can be omitted.
Thus the formula is necessary for an arbitrary-real packing; no assertion
that all outer copies are on a lattice is used.

## Six sufficient local contradictions

The published proof needs only these six singleton exclusions:

| prospective interior provider | complete necessary formula |
| --- | --- |
| (5,-8,0) | isolated corners |
| (5,-7,-1) | isolated corners |
| (4,-6,-3) | isolated corners |
| (5,-6,4) | isolated corners |
| (0,-6,-5) | full half-grid surround |
| (1,-7,-4) | full half-grid surround |

For each corner exclusion, fix C together with the listed provider and
enumerate all disjoint integral D4 copies covering its isolated gaps.
The entire necessary formula is contradictory. The four sparse proofs
retain respectively1,1,6,1 initial clauses and1,1,2,1 RUP additions.
An empty owner clause is checked against its complete empty owner set.

For each of the last two providers, C together with that provider is
independently checked to be an edge-connected integer-cell union with
exactly one simple boundary cycle, hence a disc. The previously proved
[fixed-disc half-grid corollary](../heesch_polyomino_halfgrid/proof.md)
applies, including when the fixed disc differs from a single tile P.
The prerequisite's independently selected
[review](../heesch_polyomino_halfgrid_review1/README.md) confirms that scope;
it does not review this new B lemma.

Briefly, retain copies touching the fixed disc. Filled contact sectors
lock their axes. In each translation component retain integers and replace
every n+f,0<f<1, by n+1/2. The map is monotone and unit-periodic; it
preserves whole-square separating inequalities and each square's quadrant
incidence at integer vertices. The filled vertex stars remain filled. On
the half-grid each incident quadrant covers its whole half-unit quadrant.
After doubling, the fixed union's complete radius-one cell halo is covered
by integer D4 copies of the doubled tile. No topology restriction is placed
on the resulting outer union.

The two halo inventories have respectively1334 and1344 candidates covering
132 and136 required doubled cells. Require complete covers and binary
whole-footprint nonoverlap; do not put interior-pair rules on the outer
half-grid copies. Both complete formulas are contradictory. Their sparse
proofs retain615 and48 initial clauses, with27 and2 RUP additions.
By the corollary there is no arbitrary-real surround of either required
inner union. An interior union would have such a surround, so each
contradiction supplies a sound negative unit for its prospective provider.
Failure of one chosen completion would not supply this unit.

The final necessary selector needs only51 initial clauses:

| clause source | count |
| --- | ---: |
| complete mandatory corner cover | 3 |
| complete conditional corner cover | 1 |
| whole-footprint overlap | 33 |
| imported interior-pair unit | 8 |
| proved singleton exclusion | 6 |

Two forward RUP additions prove a contradiction. For an addition D, negate
its literals and propagate units from earlier clauses; a contradiction
must follow. The last addition is explicitly empty. This proves the
necessary selector impossible and establishes the lemma.

[certificates.json](certificates.json) contains all672 subsidiary initial
clauses,34 subsidiary additions, and the final51 clauses/two additions.
The discovery's2944-variable,478725-clause formula was separately checked
by DRAT, but no dense formula, native binary or raw trace is needed here.

## Positive comparison and consequence

[positive_comparison.json](positive_comparison.json) gives36 poses with
levels0 through3. It is a compact re-encoding of the existing
[three-corona fixture](../heesch_polyomino_euler_cnf/kaplan17_depth3.witness.json),
whose SHA256 is
c5f4c30ceff27b40a39ef006960b7b5de22489c52e71b429196d1f51cdc32f04.
The packing is attributed to the earlier source, not offered as a new
construction.

The checker reconstructs every complete tile footprint, verifies whole
nonoverlap, checks a simple disc boundary at each cumulative prefix,
checks every new copy touches its preceding prefix, and checks each
preceding prefix's full unit halo in the next prefix. Thus there are
three complete disc coronas. It then enumerates all actual incoming
providers from literal sectors, followed by all their actual providers.
All ten copies in the resulting required set, including R, are interior.
There are exactly three first-generation providers, at codes(0,4,0),
(4,-3,-3),(6,-2,3). Their intrinsic source vertices give the vector
(1,2,2,0,0), independently of the discovery atlas.

For every source weight vector w, B and D have the same weighted receipt
w0+2w1+2w2. Any predicate that depends only on this receipt vector must
assign both placements the same value. Consequently a negative theorem
for B's placement cannot be promoted to a vector-wide exclusion under
the two-generation premise. This prevents an unsound pruning step in
future weighted-capacity arguments. It does not rule out a deeper capacity
or weighting theorem obtained by analyzing all actual admissible stars.

The earlier [A obstruction](../heesch_polyomino_second_generation/proof.md)
and [C obstruction](../heesch_polyomino_star_c_obstruction/proof.md) exclude
the other two specified positive weighting examples under this premise.
Their one-generation packings and weighting theorem remain valid.
Other five- and six-receipt placements remain unresolved. Neither this
lemma nor the positive comparison establishes a universal capacity,
an exact Heesch number, or a new finite-five polyomino.

The existing unrestricted interval3<=Hc<=Hh<=81 for P17 is unchanged;
see the earlier [motion proof](../heesch_polyomino_motion_bridge/proof.md).
Hc requires disc prefixes; Hh permits holes/pinches only in the final
prefix. Our negative local lemma permits arbitrary final topology.
[Mann2004](https://faculty.washington.edu/cemann/Heesch.pdf) already contains
an unmarked hexapillar-five family; the assigned square-cell finite-five
frontier is distinct. No historical priority claim is made here.

## Replay and trust boundary

From repository root, CPython3.11+ with the standard library:

    python3 -B heesch_polyomino_star_b_obstruction/check.py
    python3 -B heesch_polyomino_star_b_obstruction/check.py --controls

[check.py](check.py) rebuilds incoming poses with translation bounds and
literal quarter-offset sector tests. Discovery used vertex anchors and
affine transport. Corner inventories use bounding boxes; halo inventories
use translation joins and inverse distance tests, unlike discovery's
bounding boxes and forward dilation. Each sparse cover is matched against
a complete owner set, and each overlap against whole footprints. Pair
rules use centered-square inverses in both directions rather than the
compiled discovery library. A naive unit propagator checks every RUP step.
The positive comparison's source labels are reconstructed from intrinsic
vertices, without importing the atlas or receipt vectors.

The checker adapts exact geometry and certificate primitives from the
earlier [C checker](../heesch_polyomino_star_c_obstruction/check.py); it
imports no discovery module, candidate list or native solver. The imported
237 pair proofs and written fixed-disc half-grid theorem remain mathematical
prerequisites. Their source arguments, exact Python implementation and the
unformalized gap/phase reductions are the declared trust boundary.

Normal and assertion-disabled runs give identical [expected output](expected.json).
Five malformed negative inputs and an overlapping positive-packing mutation
are rejected. Source publication supplies reproducibility, not independent
peer validation. Complementary
[T214 forced-halo rigidity](../heesch_polyiamond_second_prefix_rigidity/proof.md)
suggests a useful propagation mechanism but concerns a different geometry
and is not a P17 prerequisite.
