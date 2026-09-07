# A complete planar triangle-isometry construction gate

**Every graph in this construction family is exactly four-chromatic.**
No improvement to the 509-vertex benchmark is produced.

Start with Haugland's physical 21-point sevenfold unit-distance graph H.
For each of its seven specified unit triangles, consider all five
nonidentity plane isometries that permute that triangle, and place the
corresponding isometric copy of H. There are 35 choices. Retain H and any
subset of those copies.

Exact geometry proves that each added copy contributes 18 private vertices
and 39 edges. Copies share only vertices of H, and the entire union has no
unit edges beyond those belonging to the copies. Thus any four-colouring
of H extends by independently permuting the colour names on each copy.
The full union has 651 vertices and 1407 edges.

The complete family with at most 508 vertices consists precisely of the
subsets with at most 27 copies. It contains **34,351,006,520 distinct point
sets**, all exactly four-chromatic, with at most **507 vertices** and
1095 edges. This counts point sets in the fixed coordinate plane, not graph
isomorphism classes. The [proof](PROOF.md) states the geometry, completeness,
universal extension, lower bound and scope.

## Reproduce

CPython 3.11+ and its standard library suffice. From the repository root:

```sh
python3 hadwiger_nelson_heptagon_triangle_isometries/produce.py \
  --output /tmp/hn-heptagon-triangle-isometries
python3 hadwiger_nelson_heptagon_triangle_isometries/verify.py \
  --work /tmp/hn-heptagon-triangle-isometries
python3 -O hadwiger_nelson_heptagon_triangle_isometries/verify.py \
  --work /tmp/hn-heptagon-triangle-isometries
python3 hadwiger_nelson_heptagon_triangle_isometries/controls.py \
  --work /tmp/hn-heptagon-triangle-isometries
```

The generated coordinate, edge and copy table stays outside the repository.
[EXPECTED.json](EXPECTED.json) gives the deterministic verifier result.
The compact [certificate](certificate.json) is only a checked 21-entry
four-colouring; no large search output or SAT proof is needed.

The producer uses Q(zeta_42). The checker independently reconstructs the
source with geometric-series inverses in Q(zeta_7,omega_6), generates each
triangle's isometries using its rotation and reflection, and compares every
coordinate and copy label after changing basis. It computes all **211575
pair norms** exactly, without a modular filter. Every unit edge is compared
entry by entry. The seed's chromatic lower bound is a complete check of
46656 normalized three-colour assignments.

Normal and optimized verification agree. Controls reject 16 malformed
inputs and compare all 144 basis products and 12 conjugation images between
the arithmetic implementations. A separate DSATUR traversal also rejects
three-colourability of the 21-vertex seed, in 709 search nodes. These are
internal validation checks, not an external peer review.

## Source and scope

The seed is the 21-point H of Section 2 of
[Haugland's manuscript](https://arxiv.org/html/2608.04542v1), whose exact
trigonometric coordinates are rewritten in complex cyclotomic form in
PROOF.md. This package does not rely on the manuscript's floating-point
separation lemma, path census or SAT results. Its producer arithmetic
derives from the earlier
[heptagon difference package](../hadwiger_nelson_heptagon_difference_lifts/geometry.py);
the independent checker imports none of that code.

This is one application of all triangle-permuting isometries to the seed.
It does not include subsequent applications to newly created triangles.
It is a congruent-copy assembly, distinct from the previous heptagon
Minkowski sums and Haugland target-ball extraction. The Snail and
finite-abelian branches remain closed; team-hn-3's current Exoo two-circle
source is separate. No such source is used as a proof premise.

All points are explicit algebraic points of the Euclidean plane and all
edges are strict unit distances. No abstract-to-planar transfer is assumed.
The remaining trust boundaries are the unformalized cyclotomic and
colour-permutation argument, CPython's exact integer/Fraction arithmetic
and parsing, and the two small implementations. This result is not yet
externally reviewed or formally mechanized. The at-most-508 five-chromatic
Euclidean target remains open. This completed family is preserved and left
at its mathematical boundary.
