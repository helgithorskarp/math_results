# Proof and scope

## Exact coordinate field

The H516 source stores coordinates in

```text
K = Q(sqrt(3), sqrt(5), sqrt(11))
```

on the ordered basis
`1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165)`,
with a common coordinate denominator 96.  Both producer and verifier perform
all distance and field arithmetic exactly.

The dependency hashes in `certificate.json` bind the calculation to the
published 516-point source and the certified 301-vertex abstract graph.

## Fixed-coordinate obstruction

Suppose a missing merged vertex has three noncollinear fixed neighbours with
squared side lengths `A`, `B`, and `C`.  Write

```text
H = 2(AB + BC + CA) - (A^2 + B^2 + C^2).
```

Heron's identity gives `H = 16 Delta^2`, where `Delta` is the triangle area,
and the squared circumradius is `ABC/H`.  A point at unit distance from all
three vertices would be their circumcentre and would require `ABC-H = 0`.

The certificate gives one fixed-neighbour triple for each missing label and
the exact nonzero value of `ABC-H`:

| missing label | source fibre | triple | exact defect `ABC-H` |
|---|---|---|---|
| 75 | 75, 105 | 20, 23, 31 | `484/243 - (92/243)sqrt(33)` |
| 76 | 76, 106 | 19, 22, 32 | `76/81 - (44/243)sqrt(33)` |
| 272 | 272, 281 | 52, 66, 68 | `14/81 - (10/243)sqrt(33)` |
| 273 | 273, 276 | 54, 58, 70 | `14/81 - (10/243)sqrt(33)` |

The verifier recomputes the three squared side lengths, nonzero area, and
defect from source coordinates.  Thus none of the four missing vertices can
be placed while the inherited 297 points remain fixed.

## Local obstruction from rigidity

Retain every abstract edge whose endpoints are among the inherited 297
vertices.  This gives a 297-vertex, 1,397-edge bar framework.  Its plane
rigidity matrix has 594 columns and maximum possible rank 591.

For each of the primes 1019, 1031, and 1091, the certificate supplies square
roots of 3, 5, and 11 and row reduction gives rank 591.  A nonzero minor after
specialization proves that the corresponding algebraic minor is nonzero in
`K`; one successful prime is logically sufficient and the other two are
redundant checks.  Infinitesimal rigidity implies local rigidity, so every
sufficiently nearby realization of this fixed subframework is congruent to
the inherited placement.  Euclidean congruence preserves the four
circumradius obstructions.  Consequently, the full 301-vertex abstract graph
has no realization in a neighbourhood of this inherited placement.

This is a local statement.  It does not exclude a distant realization of the
same abstract graph.

## Complete physical endpoint census

For each binary word of length four, choose one original H516 endpoint from
each fibre `(75,105)`, `(76,106)`, `(272,281)`, `(273,276)`, and combine those
four points with the inherited 297 points.  The verifier checks exact point
distinctness and reconstructs the complete physical unit graph from all
`301 choose 2` squared distances for each word.  This is 722,400 exact pair
tests, so no edge list inherited from the abstract quotient is trusted.

The certificate supplies a four-colouring word for every reconstructed graph.
The verifier directly checks every physical edge, 22,880 edge checks in all.
Thus all 16 natural endpoint supports are four-colourable.  They are physical
graphs, but they are not realizations of the five-chromatic abstract quotient.

## Trust boundary

The standard-Python verifier trusts Python integer arithmetic and the
published input bytes.  It does not trust a SAT solver, floating point,
producer code, or a pre-existing edge list for the physical supports.

The statement that the 301-vertex abstract graph is exactly five-chromatic is
upstream: it is backed by a proper five-colouring and a strict LRAT refutation.
This package binds to that graph by SHA-256 and adds only the realization-gate
claims above.  It makes no global nonrealizability claim and no plane
unit-distance record claim.
