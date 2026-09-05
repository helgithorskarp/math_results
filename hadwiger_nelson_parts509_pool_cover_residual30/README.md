# A residual selection and a new Parts pool killing set

**Exact finite certificate.** The four specified published killing-set
families do not cover every four-colourable selection in the remaining
fixed-L Parts pool. The explicit selection here has 508 vertices, 2,402
strict unit edges, and a proper four-colouring. It nevertheless satisfies
every one of their 24,788 positive clauses (17,250 distinct killing sets),
as well as degree at least four for every selected pool vertex.

Its colouring extends to a 638-vertex induced subgraph of the same
677-point universe. This supplies a new 39-point killing set, with ten
points in S and 29 in Q5, that excludes the exhibited selection and
strictly strengthens the specified positive-clause relaxation.

This is a cover refinement and an explicit limitation of the existing
cover. It establishes no five-chromatic graph and closes no additional
stratum. In particular, the earlier a=0,...,7 closure theorems remain
unchanged; the present selection has 30 additions.

## Sets and certificate

Use the committed labels `L={0,...,373}`, `S={374,...,508}`, and the
168-point set Q5 in
[pool_S.json](../hadwiger_nelson_parts509_s_replacement_budget/pool_S.json).
Write U=S union Q5 in sorted label order. All of L stays fixed.

[certificate.json](certificate.json) lists R subset S of size 31 and
A subset Q5 of size 30. Set X=(S minus R) union A and H=L union X.
It also lists a set D subset U of size 39 and supplies a 303-character
pool colouring `c`, with a dot exactly at each omitted point of D.
The index `p=11` selects an explicit proper L-colouring from
[interface_L.json](../hadwiger_nelson_parts509_interface_lemma/interface_L.json).
All edges within L, within the surviving pool, and across the interface
are checked directly. Completeness of the interface library is unnecessary.

The resulting colouring is proper on G=L union (U minus D), with 638
vertices and 3,046 strict unit edges. Since X and D are disjoint, its
restriction colours H. Every omitted point of D sees all four colours
in G, so this particular colouring cannot be extended by assigning a
colour to one more point while keeping the existing colours fixed.
This does not assert that D is inclusion-minimal under recolouring.

## Precisely which old cover is separated

The old family C is the union of these exact committed inputs, pinned
by SHA-256 in [manifest.json](manifest.json):

| Source | Rows |
| --- | ---: |
| [a=0,...,5 killing sets](../hadwiger_nelson_parts509_pool_shape_closure/killing_sets.json) | 1,612 |
| [Full S-only family](../hadwiger_nelson_parts509_s_replacement_budget/certificate.json) | 3,575 |
| [a=6 canonical positive instance](../hadwiger_nelson_parts509_pool_shape6_verified/killing_clauses.cnf) | 6,777 |
| [a=7 canonical positive instance](../hadwiger_nelson_parts509_pool_shape7_verified/killing_clauses.cnf) | 12,824 |

In the two CNFs, variable i+1 selects U[i]. There are 17,250 distinct
sets in C after exact equality deduplication. The verifier checks
X intersection E is nonempty for every E in C.

Consequently the characteristic vector of X satisfies the relaxation

```text
|X| <= 134,  |X intersection Q5| >= 8,
degree(v in L union X) >= 4 for each v in X,
X intersection E is nonempty for every E in C.
```

It fails the new clause `X intersection D is nonempty`. That clause is
valid for every non-four-colourable selection Y subset U: if Y missed D,
the verified colouring of G would restrict to L union Y. Thus adding D
strictly strengthens this relaxation. In particular, no old E is a
subset of D. The new row may be reused directly in subsequent masters.

The old families' positive validity has its own published certificates.
The present separation check only needs their explicit sets; it neither
regenerates their old colourings nor reruns their closure proofs.

## Reproduction and trust boundary

From a complete repository checkout, using Python 3.11 and its standard
library only:

```sh
python3 hadwiger_nelson_parts509_pool_cover_residual30/verify.py
```

Expected output is `RESIDUAL SELECTION AND NEW KILLING SET VERIFIED`,
with the exact facts recorded in [expected.json](expected.json).
No SAT solver, proof trace, network access, or private search stream is
needed to check the claim. `--output PATH` optionally saves the facts.

The verifier uses the independently reviewed integer geometry reader
in [independent_check.py](../hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py).
It checks the coordinate-source hashes, reconstructs all 228,826 pairs
of 677 distinct points at common denominator 288 in
Q(sqrt(3),sqrt(5),sqrt(11)), and recovers 3,400 exact unit edges. Coordinates
come from the scale-96 Parts table and the rational completion data;
both are committed inputs. It then checks every edge of both displayed
graphs, all counts and degrees, the old-family intersections, and the
new killing-set property. The selected graph's comma-delimited edge
stream has SHA-256
`43f6f0bfb87dce17fede88ab5e82f6247375ae4ad78289e28aefeca76c0fceff`.

The search used a bounded exact pool master followed by a full-graph
four-colouring solve. Its colouring was extended greedily in increasing
global-label order, then relabelled to the compatible L witness above.
Those search choices are not assumptions of the solver-free certificate.
The trust boundary is the committed exact coordinate data, parsing and
integer arithmetic, the explicit restriction argument, and ordinary
software execution. This is an author-checked artifact, not a claim of
external peer review or proof-assistant formalization.
