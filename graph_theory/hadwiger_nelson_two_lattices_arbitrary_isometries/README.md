# Arbitrary two-lattice unions cannot require five colours

The strict unit-distance graph on the union of **any two unit triangular
lattices is four-colourable**, for every translation and orientation.
This removes the common-vertex hypothesis from the earlier
[intersecting-lattice theorem](../../hadwiger_nelson_triangular_overlays/PROOF.md).
The new case is disjoint full lattices; the old intersecting proof is
attributed and restated to make the complete argument readable here.

The new proof is short. Any point with two unit neighbours in a unit
triangular lattice belongs to that lattice. Hence the cross edges between
disjoint lattices form a matching. Two three-colourable graphs joined by
a matching admit an explicit four-colouring: use fixed colours 1,2 in
two classes of the first part and 3,4 in two classes of the second;
each remaining independent class chooses from the other pair, avoiding
its at most one fixed cross neighbour.

[PROOF.md](PROOF.md) also gives an exact three-versus-four criterion for
disjoint full lattices. Form their bipartite contact graph on the three
residue classes on each side. Three colours suffice exactly when this
six-vertex graph has no vertex of degree three and no K2,2. This is a
structural criterion, not an algorithm claiming to enumerate all contacts
of arbitrary real placements.

The disjoint case is sharp. Two explicitly placed filled triangular
patches, of orders 10 and 6, give a strict **16-point, 30-edge,
Moser-spindle-free four-chromatic graph**. The containing full lattices
are disjoint. Three matching cross edges join three corners forced to
one colour to three corners forced to use all three colours. No size
record or minimality claim is made for this illustrative graph.

## Consequence and scope

A five-chromatic plane unit-distance construction cannot be covered by
two unit triangular lattices. A construction consisting of patches of
unit triangular lattices needs at least three full lattice supports.
The theorem has no vertex bound and covers all relative isometries, not
just a sampled or fixed host family. It does not cover other spacings,
arbitrary additive sums, or three or more lattice supports.

The verified literature benchmark remains Parts's 509-vertex,
2,442-edge construction, reported in
[Parts's paper](https://arxiv.org/abs/2010.12665) and still identified as
the overall record in
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4).
This result does not improve that record or the bounds on the chromatic
number of the plane. It supplies a reusable construction obstruction.

## Reproduction

From the repository root, using Python 3.11 or later and its standard
library:

```sh
python3 -B graph_theory/hadwiger_nelson_two_lattices_arbitrary_isometries/verify.py --check-expected
```

The exact output is [EXPECTED.json](EXPECTED.json). The check takes less
than a second on the reference host and establishes:

- the complete 18-vector norm classification and its unit-circle centres;
- valid four-colour words for all 13,327 partial matchings between two
  complete tripartite six-vertex graphs;
- the Hall criterion for all 512 bipartite contact relations;
- all 120 pair distances of the sharpness witness, agreeing between
  Cartesian radical and complex tensor arithmetic;
- triangle propagation, six three-colourings of each patch, zero of
  their strict union, an explicit four-colouring, and spindle absence;
- rejection of eight malformed inputs and a positive spindle control.

The example's zero-based edge stream, sorted and encoded as `a b\n`, has
SHA-256 `018cd84d64325755ac6845b2f6a93bdafd676b645cce2649df5ba4e6522f1d71`.
Its four-colour word is `3214132213143314`, in the lexicographic lattice
coordinate order specified by the source. Source identities and the
prior theorem's provenance are in [CONTEXT.json](CONTEXT.json).

These finite checks support the written, unbounded proof; they do not
prove it by sampling. The new mathematics is author-checked and awaits
independent review. No SAT solver, floating-point predicate, external
dataset, proof assistant, or omitted large artifact is used. The prior
intersecting theorem has an independent acceptance review; that review
does not validate this extension. No priority claim is made.
