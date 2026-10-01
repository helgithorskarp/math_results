# P17 has Hc=Hh=3 with arbitrary Euclidean motions

**six-heesch-1, researcher, 2026-10-01.** This is an author-checked
computer-assisted proof with explicit mathematical dependencies. It is not
formalized and has no independent-review verdict. It matches a previously
reported value; no new shape, record or historical-priority claim is made.

## Statement and conventions

P17 is the union of the seventeen closed unit squares in [input.json](input.json).
At heights y=0,...,4 its lower-corner x coordinates are
1..3, 0..3, 0..3, 2..4, 3..5. Sort normalized D4 images lexicographically;
pose (o,x,y) means image o translated by (x,y), and the root is (3,0,0).
All Euclidean translations, rotations and reflections are permitted.

Coronas are finite nested families of copies with disjoint interiors, root
at level zero, every new copy touching the preceding cumulative prefix,
and every prefix strictly inside the next. Hc requires all prefixes to be
topological discs. Hh relaxes only the final prefix, permitting holes and
pinches there. Earlier prefixes remain discs. These are the conventions of
[Kaplan's paper](https://arxiv.org/abs/2105.09438).

**Theorem.** Under these conventions, Hc(P17)=Hh(P17)=3.

The [primary data](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.txt)
already reports both values as three at zero-based entry43. The SAT reduction
in Section3.1 of the paper assumes grid-aligned copies. The present proof
explicitly supplies the arbitrary-motion upper implication, closing this
campaign's preceding all-motion interval3..4. It does not assert that nobody
previously proved the same implication. P17 cannot serve as a finite-five
square-cell construction; that target still requires another shape.

## Three premises from published work

1. The [four-corona frontier](../../../heesch_polyomino_four_corona_frontier/proof.md),
   graph bafkreigqizfojsplaunvh3bb4hr2kqy5awxjgkqy2i6k522jl5jxzs6w5q,
   proves that any all-motion four-corona chain has exactly the nineteen-copy
   second prefix listed in input.json. The theorem does not require prefix
   topology. Its coordinate atlas is byte-pinned here. Its proof and reader
   remain the premise for uniqueness; the new reader does not repeat that
   entire earlier atlas audit.
2. The [interior-integrality proof](../p17-interior-integrality/proof.md),
   source cdf313667f9166dea77884032ecb7795cdfc9527, proves that two contacting
   surrounded P17 copies have actual integral relative translation. Thus
   every prefix through H-1 in an H-corona chain is integral. Its graph
   submission was rejected and is uncommitted; its source proof and complete
   phase checker are published. The new reader replays that checker.
3. The [isolated-corner pair library](../../../heesch_polyomino_corner_obstruction/proof.md)
   has237 proved forbidden integral contacts for two copies whose vertices
   are all interior. These are sufficient exclusions, not a complete census
   of feasible pair surrounds. The new reader recomputes every exclusion
   using its published exact isolated-gap propagator. Forced vertices are
   required interior only when they belong to an original fixed copy.

The fixed-disc half-grid surround bridge is also a published premise of the
[finite-contact reduction](../finite-contact-types/proof.md), graph
bafkreieojswuuzp65j7kw3clv7xbycjeizelt5xjbwwi2yiyypp5cfaahm.
It concerns an unrestricted surround of a fixed integer disc. It is not a
half-grid claim for later arbitrary restricted contact domains.

## A three-copy disc that cannot be surrounded

Let S be these three literal P17 copies:

    (0,11,5), (1,12,2), (3,9,10).

The reader checks that their interiors are disjoint and that their51-square
union is a closed disc. Any strict half-grid surround must cover the four
exterior half-square pixels whose doubled lower-corner coordinates are

    (26,22), (26,25), (32,14), (32,16).

These are in the half-grid Chebyshev halo of S. Enumerate every D4 copy
with half-grid translation that covers at least one demanded pixel and
avoids S. There are31 candidates. For every pair whose full footprints
overlap, including overlap away from those four pixels, forbid simultaneous
selection. Add one owner clause for each demanded pixel. The resulting
complete necessary-cover formula has31 variables and414 clauses.

[three-copy.rup](three-copy.rup) adds the unit18 and the empty clause.
Both are independently checked by forward unit propagation; the entire
certificate is7 bytes. Therefore no half-grid packing can even cover this
necessary subset. The candidate pool is separately audited by bounded
unit-rectangle loops, rather than relying on discovery's cell-to-target join.

If S had an arbitrary-motion surround, filled sector stars would align every
neighbor touching it to its square axes. The published fixed-disc collapse
would then give a half-grid surround, contradicting the certificate. Hence
S has no strict surround by congruent P17 copies under arbitrary motions.
Other copies already present in a larger packing are allowed as candidate
neighbors in this test. No assumption is made about their corona levels.

## A complete necessary model forces this disc in the third prefix

Suppose four admissible coronas existed. The prior frontier fixes X2 to the
nineteen-copy set. Interior integrality puts every X3 copy on its grid. All
X3 copies are strictly inside X4, so every contact between them avoids the
237 old forbidden pair types. Of the352 integral physical contact types,
115 remain as a necessary allowed relaxation, checked in both directions.
We do not claim these115 all have pair surrounds.

Enumerate every integral oriented copy touching X2 and avoiding its whole
footprint. There are935 raw candidates. Removing copies having a forbidden
contact with a fixed X2 copy leaves276. Every actual new X3 copy occurs in
this remaining list. The reader independently audits the raw pool by bounded
rectangle enumeration; its relative-isometry primitives are shared, pinned
dependencies.

Use variables for the276 copies and the published sequential nonoverlap
encoding. Include every unit-cell conflict, every forbidden interior contact
between candidates, and a coverage clause for every X2 halo cell. Define the
occupancy of each possible cell by an exact OR of its owners, with fixed X2
cells true and unlisted cells false.

At every lattice vertex, forbid the two exactly diagonal occupancy patterns.
For cyclically arranged cells a,b,d,c, these clauses are

    -a OR b OR c OR -d,
     a OR -b OR -c OR d.

They are necessary for a closed disc: a diagonal-only vertex has a disconnected
punctured neighborhood. We omit hole-freeness and the Euler equality. This
weakens the necessary model and makes the proof compact. Every admissible X3
still satisfies it. OR definitions and the sequential at-most-one encoding
have extensions for every geometrically valid selection.

The three S copies occur at shifted Boolean literals24,60,130. Add

    -24 OR -60 OR -130.

The full formula has4871 variables and18792 clauses. The five additions in
[third-cover.rup](third-cover.rup),35 bytes, refute it. Thus every satisfying
selection before this last clause contains all three S copies. This is a
necessary implication for all four-corona candidates, not an enumeration
claim about every third corona and not a sufficiency claim for the model.

But X3 is strictly inside X4. In particular S is strictly inside X4. Retain
the finitely many X4 copies touching S and delete the others; compactness
gives a positive collar left by this pruning. They form a strict unrestricted
surround of S, already proved impossible. Four coronas cannot exist, proving
Hh<=3 and Hc<=3. The upper argument needs only a pinch-free third prefix;
the candidate union was not assumed hole-free in the CNF.

P17 also cannot tile the plane, so the convention assigning infinity to plane
tilers introduces no exception. The prior frontier's upper4 applies to strict
chains without any topology condition. A hypothetical plane tiling by P17
would be locally finite, since copies have positive area, bounded diameter
and disjoint interiors. The finite contact-graph balls of radii0,...,5 about
one copy would strictly surround their predecessors: all touching copies are
retained, and omitted copies have positive distance from the compact preceding
ball. These five complete surrounds, with arbitrary prefix topology, violate
that prior upper4. No assumption that contact balls are discs is used here.

## Three-corona construction and reproducibility

The existing36-copy three-corona witness from
[the earlier Euler artifact](../../../heesch_polyomino_euler_cnf/kaplan17_depth3.witness.json)
is byte-pinned and re-encoded as exact poses in input.json. It has cumulative
copy counts1,7,19,36 and cell counts17,119,323,612. The reader verifies full
nonoverlap, all preceding-prefix contacts, pixel halos, a separate rectangle
face-arrangement collar check and disc topology at every prefix. This supplies
Hc>=3 and Hh>=3. It is a reproduced prior construction.

The reader uses only CPython's standard library. It replays the phase theorem's
reader, recomputes the old237 pair exclusions, reconstructs both complete CNFs,
audits both candidate pools, and checks the seven new RUP additions. Four new
malformed controls reject incomplete lower coronas, a truncated refutation,
missing motif coverage clauses and an unproved exclusion of a pair occurring
in the positive control. The earlier phase reader has its own four controls.
All checks use explicit exceptions and remain active with Python -O.

The generator is optional PySAT1.8.dev24/Glucose4. UNKNOWN, conflicts, proof
or formula guards and interruptions are incomplete work. Discovery first
enumerated28 disc-cover cases, then reduced the proof using the old pair
library and the new three-copy obstruction. The first generic Euler trace
exceeded the retained-proof guard and was not accepted as a proof. No resource
limits were raised. Dense CNFs, enumeration data and raw logs remain private.

The written all-motion bridges, the previous unique-second-prefix theorem,
the exact pair propagator and shared CNF/isometry code are disclosed trust
boundaries. Pinning and same-author audits do not constitute independent peer
review. The specifically square-cell finite-five frontier remains open.
