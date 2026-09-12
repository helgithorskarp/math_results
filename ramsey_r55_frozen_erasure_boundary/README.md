# A failure of simultaneous frozen-edge erasure

This is negative evidence for a proposed structural compression, not progress
on the numerical Ramsey bound. It does **not** satisfy the campaign's
first-pass gate for a theorem and receiver covering good43.

Two explicit, nonisomorphic good42 graphs have exactly the same frozen-edge
mask, the same colors on every nonfrozen edge, and the same full labeled
vertex-degree vector. Nevertheless, they have different triangle counts.
Thus simultaneously erasing all frozen colors is not an injective encoding,
even if individual degrees are retained and graphs are considered up to
isomorphism.

A good graph has no clique or independent set of size five. Call a pair
**frozen** when reversing its color creates a monochromatic five-set. This
is a property of an individual graph, with no prescribed symmetry. A pair
is frozen exactly when it is the exceptional edge of an induced K5 minus
one edge in the opposite color. Its witness consists of the nine other
edges of that five-set.

## Exact counterexample

[COUNTEREXAMPLE.json](COUNTEREXAMPLE.json) supplies the two graph6 words and
a permutation taking the second graph into the labels of the first. They
are records 3 and 17, with zero-based indices, in
[McKay's known order-42 data](https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6).
The input file SHA-256 is
`067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`.
Only the two small fixtures are needed for verification; completeness of
that list is neither assumed nor asserted.

Both graphs have 424 red edges and the labeled degree vector recorded in
the fixture, with multiset `19^8 20^20 21^12 22^2`. Both have the same 855
frozen pairs. Their six common nonfrozen pairs, in the first labeling, are

```
blue:  (2,3), (4,5), (20,21), (20,22), (21,23)
red:   (24,25)
```

The first graph has 1302 red and 1368 blue triangles; the second has 1304
red and 1366 blue triangles. Triangle counts certify that they are not
isomorphic. Since both have 424 edges and their complements have 437,
allowing a global color interchange does not identify them either. The
displayed labeling changes 342 pairs, all among the erased pairs.

Writing `F(G)` for the frozen mask, the failed proposed encoding was

```
G -> (F(G), colors on pairs outside F(G), (d_G(0),...,d_G(41))).
```

The collision is exact. It does not refute an order-43-specific rigidity
conjecture, an encoding with further side information, or a receiver that
searches all completions. Neither graph is asserted to belong to the same
fixed maximal-packing task. The conclusion is that the general erasure
principle itself cannot justify an exact carrier reduction.

## The missing reconstruction obligation

An individual frozen edge is recoverable when its witness's nine other
colors are known. Simultaneous erasure removes many of those supports.
Existence of a witness in the original graph is not existence of an
available witness in the partial graph.

A sufficient, checkable repair is an ordered list of erased pairs and
witnesses such that each witness uses only retained pairs and earlier
recovered pairs. Induction then reconstructs every erased color, and each
step is unit propagation in the ordinary Ramsey five-set CNF. Conversely,
a reconstruction using only such unit steps supplies such an order.
There is no order available for the displayed partial graph: only six
pair colors remain, whereas its first step would require nine. The two
good completions also show that arbitrary logical inference from the
retained colors and exact degree vector cannot recover every erased color.

This certificate does not bound the additional seed information needed to
repair the encoding. No all-good43 seed theorem, smaller complete carrier,
original-task retirement, or target proof interface is obtained.

## Reproduction and trust

With Python 3.11 or later and only its standard library:

```sh
python3 -B ramsey_r55_frozen_erasure_boundary/verify.py > /tmp/frozen-erasure.json
cmp /tmp/frozen-erasure.json ramsey_r55_frozen_erasure_boundary/EXPECTED.json
```

The checker strictly decodes both graph6 fixtures, checks the permutation,
and examines every one of the 850668 five-sets in each graph. It rejects
monochromatic five-sets and records every pair occurring as the minority
edge of a nine-to-one five-set. Thus it checks both the frozen and
nonfrozen assertions, not just selected positive witnesses. A separate
three-set enumeration supplies the triangle-count obstruction to
isomorphism. It then compares the complete retained edge records and full
degree vectors, rather than only their counts or hashes.

Discovery used common-neighborhood triangle searches and a colored-graph
isomorphism search to find the permutation. Neither algorithm is imported
by this verifier. The complete fixed permutation is checked directly;
no isomorphism solver, SAT solver, catalog-completeness assertion, or
external Ramsey bound is needed for the counterexample. This is internal
validation, not independent peer review or proof-assistant formalization.
Python execution and the short, unformalized bridge above remain trusted.

The separate [approach assessment](ASSESSMENT.md) records why simple
near-clique incidence bounds did not supply a demonstrated carrier gain.
It is not a claim that every possible method using frozen edges fails.
