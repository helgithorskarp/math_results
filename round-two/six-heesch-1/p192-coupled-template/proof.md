# A coupled-template classification and unrestricted extension obstruction

Author: six-heesch-1, researcher. Exact computer-assisted lemma with ordinary
geometric arguments; unformalized, independently unreviewed.

## Statement and literal domain

Let S be the68-cell scale-two copy of the17-cell P192 seed recorded in
[input.json](input.json). This copies the literal input of the earlier
[fixed-motion template](../p192-template-rigidity/proof.md), ultimately from
[Kaplan's primary17-omino catalogue](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.txt),
zero-based entry192. No tile-specific Heesch upper is imported.

For a cell set A, let Halo8(A) be its exterior eight-neighbour collar.
Let I consist of the cells of S whose four side neighbours lie in S;
|I|=35. Let U be S together with all its exterior side neighbours; |U|=105.
A prototype Q is any common unmarked unit-square cell set I subset Q subset U.

Use the eight lexicographically sorted normalized D4 images of S. For each
image choose its unique signed permutation matrix M and let l be the
componentwise minimum of Mx over x in S. An orientation/translation pose
(o,t) maps cell indices x to Mx-l+t. This is a polygon isometry: if r is the
lower-corner shift of M[0,1]^2, its point map is z to Mz-l+t-r.
The seven poses are exactly the first two seed levels in input.json, with
translations doubled. The first is the identity. Add an independent
delta_j in {-1,0,1}^2 to each of the other six translations. These frames
remain fixed from S even when Q changes; normalizing a new prototype does not
silently change the physical motions.

Suppose Q and the six selected copies are interior-disjoint, each selected
copy meets Q's boundary, Q lies strictly in the interior of their union C,
and both Q and C are topological discs. Then either Q=S or Q equals the
literal67-cell R in [exception.json](exception.json). For R there is exactly
one ordered tuple of shifts:

(-1,0), (0,1), (0,0), (-1,0), (1,1), (0,-1).

The resulting seven-copy469-cell first patch C cannot be strictly surrounded
by copies of R under any Euclidean rigid motions, including reflections and
arbitrary real translations. Holes in this hypothetical second union are
permitted. Consequently, every changed prototype Q!=S satisfying this core
and domain has no two-corona construction whose first corona has the six
specified orientation frames and unit shifts. In particular, a balanced
68-cell edit cannot even have an admissible disc first corona in this template.

The theorem places no global upper on R: first coronas outside this template
were not classified. It does not exclude other core choices, larger domains,
changed orientation frames, larger shifts, or additional first-corona copies.

## Necessary finite formula

Give each of the105 possible prototype cells a membership variable X. Force
all35 core variables. Give each of the six placement groups nine selectors Y,
with exactly one true. For every potential pair of copies and every common
world cell, impose conditional non-overlap. The two relevant membership
variables and placement selectors are the only possible conditions; core
membership literals can be removed because their units are present. Exactly-one
clauses handle alternatives from the same group.

For each possible root cell x and each of its nine neighbours p, require
X_x to imply that some active copy supplies p. Root suppliers are membership
variables; nonroot core suppliers are selectors. Every remaining supplier is
an AND gate Z iff Y and X. There are1093 shared gates. Pixel incidence is
unique within an option, so gate keys (Y,X) are unambiguous. This gives1252
variables including105 memberships and54 placement selectors. Exclude the
unchanged S with one clause on its70 editable memberships.

Full integer-cell non-overlap is equivalent to disjoint polygon interiors.
The complete eight-neighbour collar is equivalent to strict containment of
the root boundary for such unions. Thus every edited configuration in the
statement satisfies this necessary formula. It has11409 clauses and DIMACS
SHA256 ce57dafede141a418d2b8c05cb0ac42eceef1a6ee5a4473a1c07bc68dffb61c4.
Topology and designated-neighbour contact are checked directly afterward.

## Geometric exclusions and the prototype exception

The compact [classification data](classification.json) lists three rejected
models: a62-cell non-disc prototype, and61- and60-cell prototypes whose chosen
first unions are non-discs. A non-disc prototype can be blocked as a whole
mask. A bad first layout of a disc prototype is blocked only together with
its six selected placements. This distinction is essential: another layout
of the same mask must remain available.

The67-cell model is an explicit admissible exception. Its full mask is
excluded only to classify the remainder, not as an inadmissible shape.
The [residual RUP trace](residual.rup) proves the necessary formula plus the
three valid geometric exclusions and the explicit exception mask unsatisfiable.
All3160 clause additions are checked by reverse unit propagation; deletion
records, which the reader never used, were omitted. Thus every admissible
changed mask equals R. This is not a census of all placements of every mask.

A finite union of closed grid squares is a topological disc when its
side-adjacency graph is connected, its complement has no bounded component,
and it has no vertex with just two diagonally opposite occupied quadrants.
The last condition excludes pinched boundary points. These tests give a
connected compact planar region with a single simple boundary component.
The reader implements them directly, and checks the seven literal positive
copies of R, strict root coverage, contact and disc topology.

## Unique first layout of R

Freeze R and compile the54 selectors alone. Impose exactly one choice in each
group, root/nonroot and nonroot/nonroot whole-copy packing, contact with the
root, and complete root Halo8 coverage. There are456 clauses, DIMACS SHA256
8ea6dcf5f4deda9737896adadce8a6ba52a5c51e96b1077281058c14f4c136ea.
The supplied selector set is {2,15,23,29,45,49}. The direct positive checks
validate its first patch. Adding the single clause blocking precisely these
six choices makes the formula contradictory by unit propagation, as checked
in [layout.rup](layout.rup). Therefore it is the unique packing/surround
layout, even before first-patch topology is required. The independent layout
compiler uses global world-cell incidence instead of discovery's pairwise
footprint intersections.

## The all-motion corner obstruction

At the original vertex v=(3,15) of C, the northeast unit cell (3,15) is empty;
the two adjacent quadrants are occupied. Strictly covering C must fill the
open90-degree sector at v. Every local incident sector of an orthogonal
polyomino has angle at least90 degrees, so exactly one convex90-degree tile
corner must fill it. Its edges align with the sector, forcing a D4 frame.
Its vertex is mapped to the integral v, forcing integral translation. Its
two incident grid edges have lengths at least one, so it covers the entire
indicated exterior unit cell.

It is therefore necessary that one of the8*67=536 integer whole-copy poses
covering that cell be disjoint in interiors from C. No such pose exists.
The discovery inventory tests full footprints. The reader instead forms
every forbidden translation C-O(R) for each of eight oriented cell sets O(R),
then tests the67 translations taking one cell of O(R) to (3,15). All are
forbidden. This is a complete necessary inventory, not a restricted final
contact domain. The obstructed vertex belongs to the original first patch;
no newly introduced point is improperly required interior.

The90-degree argument is the earlier
[polyomino corner mechanism](../../../heesch_polyomino_corner_obstruction/README.md)
applied to this literal patch. Arbitrary second-corona motions and final holes
cannot repair the local obstruction. Other first patches of R remain outside
the theorem.

## Verification and relation to the assigned frontier

Run the two commands in [README.md](README.md); [verify.py](verify.py) rebuilds
both formulas, verifies both RUP certificates and every geometric premise,
and rejects five damaged cases. Python integers and standard-library code
are used. The only imported module is the public byte-pinned
[RUP reader](../finite-contact-types/rup.py); its source and the literal input
are pinned by [dependencies.json](dependencies.json). A native SAT solver
was used for discovery, but its status is not part of the proof.

The ordinary encoding, planar disc criterion and corner-sector argument are
written bridges, not formalized theorems. The result is author-checked;
independent review is pending. It closes a finite template route toward an
unmarked polyomino with finite Heesch number at least five; that target is
unmet.

Corona conventions follow [Kaplan's primary paper](https://arxiv.org/abs/2105.09438):
every prefix before the final corona is hole-free, and the final union may be
required hole-free (Hc) or allowed holes (Hh). The exclusions here cover both
conventions for two or more coronas in the stated first template. The paper's
finite-five examples in its prior-work discussion concern marked polyforms;
its unmarked enumeration reaches four. The2024
[isohedral-detection paper](https://arxiv.org/abs/2406.16407) is not a finite-five
construction. No exhaustive current record or priority claim is made here.

The [literature note](literature-note.md) corrects the earlier hexapillar baseline description using Mann's primary source.
