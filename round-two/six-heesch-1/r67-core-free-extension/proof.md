# A uniform extension obstruction with no retained core

Actual author: six-heesch-1, researcher. An exact computer-assisted lemma with
ordinary geometric arguments; author checked, unformalized and independently
unreviewed.

Let S be the 68-cell scale-two expansion of the literal 17-cell P192 seed in
[the pinned prior input](../p192-coupled-template/input.json), ultimately
[Kaplan's primary catalogue](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.txt),
zero-based entry 192. Let U be S together with its exterior four-neighbour
cells, so |U|=105. No cell of S is required to remain in the new prototype Q.

Use the lexicographically sorted normalized D4 images of S. In orientation o,
let M_o be the unique signed permutation matrix and l_o the componentwise
minimum of M_o u over u in S. A pose (o,t_x,t_y) acts on cell indices by

    A_(o,t)(u) = M_o u - l_o + t.

These are fixed physical polygon isometries even when Q changes. If r_o is the
lower corner of M_o[0,1]^2, the corresponding point map is
z -> M_o z - l_o + t - r_o. In particular, cell-index actions preserve whole
unit-square footprints. The seven poses, including the identity root, are:

    (4,  0,  0), (1,  9,  2), (3, -4,  7), (3,  4,  8),
    (6,  7, -8), (7, -9,  3), (7, -4, -7).

They are exactly the earlier R67 first-copy pattern. [input.json](input.json)
also records its six shifts relative to the seed first placements.

**Lemma.** No nonempty disc polyomino Q contained in U has a complete second
corona extending the specified root and six first copies. More explicitly,
if these seven copies pack without interior overlap, form an admissible first
corona and put the entire root strictly inside their union C, then no finite
packing of further congruent copies puts C strictly inside the enlarged union.
Further copies may use arbitrary rotations, real translations and reflections.
The enlarged union may contain holes. Consequently this first pattern cannot
occur in any construction of two or more complete coronas in this domain.

This is a statement about one first-copy pattern, across every prototype mask
in U. It does not bound H(Q) when another first corona is used. The earlier
[R67 result](../p192-coupled-template/proof.md) required all 35 interior cells
and classified nine shifts per neighbour before isolating R67. Here the core
condition disappears, but the first pattern is fixed. The separate
[outer-cluster rigidity](../p192-core-free-rigidity/proof.md) assumed 14
second-reference copies pack internally; none of those copies or motions is
assumed here.

Each possible source cell u in U has a membership variable X_u, numbered in
lexicographic order. Whole-copy packing gives clauses not X_u or not X_w
whenever two of the seven source images share a world cell. For every possible
root cell u and every offset d in {-1,0,1}^2, require X_u to imply that the
world cell u+d is supplied by some one of the seven copies. Their suppliers
are the membership variables of all preimages in U. Tautologies are omitted.
These 952 clauses impose exactly whole-copy packing and the complete root
eight-neighbour collar. They are necessary for a strict first surround.
Add the single positive clause containing all 105 memberships to exclude the
empty mask. No topology cuts or prototype exceptions are added.

Now consider the original vertex v=(3,15), its northeast unit cell p=(3,15),
and the fixed pair consisting of the root and f=(3,-4,7). The source cells
(4,7) and (3,6) of f map to the two unit cells adjacent to p around v.
The root source (3,6) and f source (11,7) map to side-adjacent world cells.
These four source witnesses, with a repeated membership allowed, ensure both
that the neighbouring quadrants are occupied and that f really touches the
root. Thus f belongs to the first corona when these witnesses are present.
All v's neighbourhood must be interior after a complete second corona.

If another one of the seven fixed copies already covers p, impose no new
supplier obligation. Its source-membership bit is included among the positive
disjuncts. This inventory includes preimages from **every fixed copy**, not
just the designated pair. If no fixed copy covers p but all witnesses are
present, any second corona must fill the isolated open 90-degree sector at v.
Every incident sector of a disc polyomino has angle at least 90 degrees.
Therefore one convex 90-degree tile corner fills that sector. Its edges must
align with the sector and its integer source vertex must map to v. This
particular supplier has a D4 orientation and integer translation and covers
the entire unit cell p. Other new tiles need not have integer translations.
This is the local angle mechanism of the earlier
[corner obstruction](../../../heesch_polyomino_corner_obstruction/README.md),
rederived here rather than a global motion restriction.

For each of the eight reference orientations and each u in U, introduce an
option Z for the unique integer translate mapping u to p. These 840 options
include every necessary supplier, even if Q has symmetries. Add Z -> X_u.
For every full supplier source cell s and every fixed source cell w that maps
to the same world cell, add

    not Z or not X_s or not X_w.

Finally add the conditional demand clause consisting of the negations of the
four witness memberships, all fixed-copy preimages of p and all 840 options.
When the gap is already filled or a witness is absent, no supplier is required.
When it is demanded, at least one selected whole copy must avoid every fixed
copy. No collisions between distinct new suppliers are imposed. This is a
necessary relaxation; its SAT assignments would not be complete coronas.

The conditional module has 76,472 clauses and 945 variables. The full union
with the 952 first clauses and the nonempty clause has 77,425 clauses. Its
canonical DIMACS SHA256 is

    83452292cf9f4b6c155128353d4ea33e5e74e0e96461908ffb68b1e3eb48cad5.

The [203-byte proof](obstruction.rup) contains 11 additions, each checked by
reverse unit propagation, and ends with the empty clause. Hence the necessary
formula is contradictory. A hypothetical second-corona extension would give
an assignment to its membership variables and, when demanded, the actual
supplier option; every clause would hold. This contradiction proves the lemma
uniformly over the entire prototype domain.

The reader reconstructs inverse affine preimages independently of discovery's
world-cell incidence. It uses the public byte-pinned
[RUP reader](../finite-contact-types/rup.py) and normalized
[cell-frame reader](../p192-coupled-template/verify.py) as code. Their older
classification, contact-domain theorem and tile-specific Heesch upper are not
premises. The corner angle and strict-corona bridges are written mathematical
arguments, not proof-assistant formalizations.

The first-corona premise is nonvacuous: the pinned 67-cell R67 fixture has a
seven-copy disc patch with 469 cells in this pattern. The reader verifies it
and all 536 literal corner suppliers fail. For the unchanged S68 in its own
first pattern, it verifies two disc coronas (1, 7, 21 cumulative copies), an
actual complete corner supplier, a disabled edge-contact premise and a gap
already filled by a fixed copy outside the designated pair. Nine damaged
certificates/proofs are rejected for exact expected reasons. Both interpreter
modes reproduce [the expected evidence](expected.json).

Corona conventions follow [Kaplan](https://arxiv.org/abs/2105.09438): every
prefix before the final corona is hole-free; the final corona can be required
hole-free (Hc) or allowed holes (Hh). The lemma excludes this pattern under
both conventions. It gives no finite-five construction, new record, global
Heesch upper or plane non-tiling result for these prototypes. The primary
[author census](https://cs.uwaterloo.ca/~csk/heesch/) is context, without an
exhaustive currentness or historical-priority claim.
