# T375 degree-four/five target closure

Let `T` be the exact 375-vertex, 1,661-edge triangle-forcing graph in
[`hadwiger_nelson_small_triangle_forcer375`](../hadwiger_nelson_small_triangle_forcer375/README.md).
Its coordinates lie in the lattice

```text
Lambda = {((a sqrt3+b sqrt11)/36, (c+d sqrt33)/36) : a,b,c,d integers}.
```

For a lattice point `q` outside `T`, let `degree_T(q)` be its number of unit
neighbours in `T`.  Define

```text
H = T union {q in Lambda : degree_T(q) >= 6},
P = {q in Lambda : degree_T(q) is 4 or 5}.
```

Only points with at least one neighbour in `T` need be considered in these
sets.  The exact result is:

> The strict unit-distance graph on `H union X` is four-colourable for every
> subset `X` of `P` with at most two elements.

Here `H` has 506 vertices and 2,677 unit edges.  The optional set has 427
points: 286 of `T`-degree four and 141 of `T`-degree five.  Thus the theorem
checks **91,379 physical graphs** of orders 506, 507 and 508, including all
90,951 two-point choices at the target order.  Their strict edge counts range
from 2,685 to 2,695.

There is no five-chromatic graph or record improvement.  This extends the
[preceding degree-five closure](../hadwiger_nelson_t375_high_contact_target_closure/README.md),
which checked the 141 degree-five points only.  It remains a restricted-family
exclusion, not a lower bound for arbitrary plane unit-distance graphs.

## Exact terminal-relation stopping boundary

The first three vertices of `T` form the marked equilateral triangle of side
`1/sqrt(3)`.  The parent theorem says they cannot be monochromatic in a proper
four-colouring.  For every single optional point `q` in `P`, this package also
proves that **every non-monochromatic assignment** to those three terminals
extends to `H union {q}`.

Up to a global permutation of four colour names, the four non-monochromatic
patterns are

```text
001, 010, 011, 012.
```

Twenty-seven checked core colourings cover all 427 optional points for each
of these patterns.  Hence neither `H` nor any one-point degree-four/five
extension gives a stricter terminal relation.  This is the construction-lane
stop condition: relation-preserving minimization cannot start from a single
member of this optional band.

The two-point theorem does not claim that every terminal pattern survives
every pair.  It needs only one proper colouring for each pair.

## Complete exact geometry

For an integer difference row `[a,b,c,d]`, squared distance one is equivalent
to

```text
3 a^2 + 11 b^2 + c^2 + 33 d^2 = 1296,
a b + c d = 0.
```

The nonnegative first equation bounds all four coefficients.  The verifier
enumerates exactly 54 oriented unit directions.  Adding them to all 375 seed
points, deduplicating and removing `T` gives 12,184 lattice completion points.
Their `T`-degree distribution is

| degree | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| points | 9,615 | 1,482 | 529 | 286 | 141 | 71 | 21 | 16 | 18 | 5 |

The 131 points of degree at least six form the additions in `H`.  Appending
the 427 optional points gives a 933-point audit support with 5,483 strict unit
edges.  The verifier scans all unordered pairs with the two integer equations;
no floating-point distance or supplied edge list is trusted.

## Positive colour certificate

The certificate contains 15 proper four-colourings of the 506-point core.
For a core colouring `f` and optional point `q`, define its available list

```text
A_f(q) = {0,1,2,3} minus {f(v) : v in H and |v-q|=1}.
```

A pair `q,r` extends `f` exactly when both lists are nonempty and, if `q,r`
are unit adjacent, their lists admit two different colours.  The verifier
checks this elementary condition for all 90,951 pairs.  The first eight rows
are byte-for-byte the predecessor's published core words and cover 90,469
pairs; seven added rows cover the remaining 482.  Every singleton is also
covered.  The empty choice uses any checked core row.

The separate 27-row relation certificate is checked in the same way, with
the terminal colours pinned to each canonical pattern.  Colour-name
permutation then covers every labelled non-monochromatic assignment.

The final checker uses no SAT verdict.  Discovery used PySAT 1.9.dev15 with
CaDiCaL195 only to find the positive words; every word, unit edge, availability
list and family-coverage claim is reconstructed directly.  Ten malformed
certificate controls must be rejected.

## Reproduce

CPython 3.11 or later and the standard library suffice.  From this directory:

```sh
python3 -B verify.py
python3 -O -B verify.py
sha256sum -c SHA256SUMS
```

The first two commands must print the same one-line JSON object, equal to
[`expected.json`](expected.json).  The parent and predecessor packages remain
at their repository paths and are hash-pinned in `provenance.json`.

## Scope and disposition

This theorem concerns the fixed T375 support, the exact lattice `Lambda`, the
degree-at-least-six core and at most two points from the degree-four/five band.
It does not classify degree-three or lower completions, arbitrary non-lattice
points, multiple completion generations, altered cores or other geometric
motifs.  Every subgraph of a covered support is four-colourable by restriction.

The published comparison remains Parts's 509-vertex plane unit-distance graph
([arXiv:2010.12665](https://arxiv.org/abs/2010.12665)), also described as the
record in Haugland's 2026 paper
([arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4)).  This package is
author-side exact verification, not independent-author review.  It closes this
band and recommends a geometry change rather than a routine descent through
lower contact degrees.

The Discovery Net contribution receipt is recorded as pending in
`DISCOVERY_RECEIPT.json`: the broadcast was accepted, but the stale committed
ledger did not index it.  It must not be described as committed or resubmitted.
