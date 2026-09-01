# Asymmetry of the twelve Parts-509 swap graphs

This directory gives a solver-free exact certificate that the strict
509-vertex unit-distance graph published by Jaan Parts and each of the eleven
exceptional one-point swaps in the certified swap closure have trivial
automorphism group.  It also gives a canonical SHA-256 fingerprint for each
abstract graph.  The twelve fingerprints are distinct.

This is a structural result about the existing 509-vertex constructions.  It
does **not** produce a graph below 509 vertices and does not improve the bounds
`5 <= chi(R^2) <= 7`.

## The theorem and proof

Start with the partition of the vertices by degree.  At each round, give a
vertex the signature

```text
(its preceding color, the sorted multiset of preceding colors of its neighbors).
```

Assign a common new color exactly to vertices with equal signatures.  This is
degree-seeded one-dimensional Weisfeiler--Leman refinement (equivalently,
equitable partition refinement).

Every automorphism preserves degree, and inductively preserves every color at
every round.  In all twelve graphs the refinement becomes discrete: every
vertex has its own color.  Therefore every automorphism fixes every vertex, so
the automorphism group is trivial.  Lexicographically numbering the exact
signatures makes the final discrete order canonical; hashing the canonically
relabelled edge list gives a compact identifier for later deduplication.

The proof uses only integer graph incidence.  It has no hash-collision step:
SHA-256 is used to bind input and output bytes, while the actual refinement
compares exact tuples or exact integer neighbor-count vectors.

## Reproduce

From the root of a checkout of this repository, using CPython 3.11 or later:

```bash
python3 hadwiger_nelson_parts509_asymmetry/refinement_certificate.py verify
python3 hadwiger_nelson_parts509_asymmetry/independent_check.py
```

Regenerate the committed certificate with:

```bash
python3 hadwiger_nelson_parts509_asymmetry/refinement_certificate.py certify
```

The first program constructs the twelve graphs from the committed 2,442-edge
base graph and the eleven swap records, recomputes the full refinement
transcript, and verifies `certificate.json` byte for byte.  The independent
checker imports none of the first program; it refines ordered blocks by exact
neighbor-count vectors and checks the same cell counts and canonical hashes.

Expected final lines are:

```text
all_asymmetric=true
all_canonical_hashes_distinct=true
independent_partition_check=true
all_12_graphs_asymmetric=true
all_12_canonical_hashes_distinct=true
```

No external Python packages are required.

## Inputs, scope, and trust boundary

The input bytes are bound to:

- raw `edges.json` SHA-256
  `2308fe8a798113e1c3bee9b571ed21875c44997a9916712bd76b6983f24861c8`;
- canonical base edge-list SHA-256
  `5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c`;
- `swap_certificate.json` SHA-256
  `a36a11bf3e63d3ec887b0f4507d51623773b968842a964a314e364713ac46ca3`.

The statement that these abstract graphs are strict unit-distance,
5-chromatic, and 5-vertex-critical is not reproved here.  It depends on the
exact geometry, coloring, and UNSAT certificates in the preceding Parts-509
criticality and swap-closure contributions.  This contribution certifies only
the graph-theoretic asymmetry and canonical fingerprints of those bound
inputs.  Its implementation trust boundary is CPython's JSON parser, integer
and tuple operations, file I/O, and SHA-256 implementation.  The two checkers
share only the input format and theorem; they implement the refinement in
different ways.

## Literature status

Parts's minimization paper establishes the 509-vertex, 2,442-edge construction
and discusses many nonisomorphic minimization outputs, but does not appear to
state automorphism-group data for this graph.  Targeted literature and
repository searches through 2026-09-01 found no such data for the twelve swap
graphs.  This is therefore presented only as a verified graph-level structural
finding, with no claim of literature priority.

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
  <https://arxiv.org/abs/2010.12665>.
