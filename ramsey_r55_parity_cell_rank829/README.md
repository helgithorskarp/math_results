# An exact rank-829 parity cell for the unrestricted good43 search

This package gives a checked terminal result for one complete parity fiber in
an exhaustive normalization of the physical 43-vertex Ramsey problem.  It does
**not** construct a good43, improve the published bound on `R(5,5)`, or exclude
an isomorphism class of graphs independently of the chosen parity coordinates.

## The code theorem

Order the 861 edges of `K_42` lexicographically as

```text
(1,2),(1,3),...,(1,42),(2,3),...,(41,42).
```

Let `H` be the 829 by 861 binary matrix generated from seed `400517` as
follows.  Start with the 64-bit state equal to the seed.  For each matrix
entry, in row-major order, take the low bit of the next SplitMix64 output,
using the constants written literally in both source files.  The resulting
matrix has rank 829.  Its packed-row SHA-256 is

```text
1d1c87c142399e08d35517df6690d303ec38046e4a31ef5a88973c0c4b3fbab8
```

where each row is packed into 108 little-endian bytes before the rows are
concatenated for hashing.  Its kernel is a binary `[861,32]` code `C`.

**Exact computed theorem.** Every nonzero word of `C`, interpreted as an edge
set on vertices `1,...,42`, contains a `K_5`.  The zero word is the unique word
without a red `K_5`; its complement plainly contains a blue `K_5` (for example
on vertices `1,...,5`).

Both programs exhaust all `2^32 = 4,294,967,296` codewords.  The producer uses
an iterative lexicographic bit-intersection search and records the first
five-clique in a two-component rolling checksum.  The independently written
checker uses recursive clique extension, validates all 32 basis vectors
against all 829 original check rows, and checks every step of its Gray-code
traversal.  Their common classification is

```text
nonzero words containing a red K5 = 4,294,967,295
zero words containing a blue K5   = 1
```

The producer checksum is
`(xor,sum)=(9e8c7dadcb0db86a,55bfc6a7e317de58)`.

## Exact connection to the complete physical problem

Write a physical graph edge as red and a nonedge as blue.  The classical
exact value [`R(4,5)=25`](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf)
implies that every vertex of a hypothetical good43 has
red degree at most 24; applying the same statement to the complement gives
red degree at least 18.

Complement the whole graph if necessary so that red has at most 451 edges.
Its average red degree is then at most `902/43 < 21`, so it has a vertex of
degree `d` in `{18,19,20}`.  Relabel that vertex as 0, its red neighbors as
`1,...,d`, and its blue neighbors as `d+1,...,42`.  The remaining 861 physical
edge bits form a vector `x` in `F_2^861`.

For each `d` in `{18,19,20}` and syndrome `s` in `F_2^829`, define the cell

```text
P(d,s) = {x in F_2^861 : Hx=s},
```

with the stated fixed colors on the root edges.  Because `H` has full row
rank, the `2^829` cells for a fixed `d` are pairwise disjoint, each has exactly
`2^32` members, and their union is the entire physical root template.  The
three degree templates are also disjoint as labeled graphs.  Every good43 has
at least one representative somewhere in this exact partition; no catalogue,
automorphism, carrier normalization, or completeness claim is used.

The code theorem simultaneously excludes `P(18,0)`, `P(19,0)`, and `P(20,0)`.
This complete root-degree fiber contains

```text
3 * 2^32 = 12,884,901,888
```

labeled normalized graphs.  A nonzero kernel word already has a red `K_5`
among the nonroot vertices, independently of `d`; the zero word has a blue
`K_5` there.  Thus the three-cell conclusion has an exact partition join and
does not rely on degree or edge-count filters during enumeration.

The eliminated fraction is only `2^-829` of each fixed-degree root template.
Consequently this is a validated first cell-family milestone and a reusable
certification mechanism, not meaningful endpoint movement by itself.

## Reproduction

On a 64-bit machine with a C++20 compiler:

```sh
./ramsey_r55_parity_cell_rank829/reproduce.sh
```

The producer and checker each make a full pass over all `2^32` codewords.
On the development host they took roughly 2.5 and 3.5 minutes respectively.
No SAT solver, floating point, graph catalogue, saved witness table, or
external data is used.  Expected terminal lines are in
[EXPECTED_OUTPUT.txt](EXPECTED_OUTPUT.txt).

## Trust boundary and next gate

The evidence consists of two same-author native implementations with distinct
clique-search logic, exact integer arithmetic, source hashes, and complete
replays.  It is not a DRAT/LRAT certificate, proof-assistant theorem, external
review, or historical-priority determination.  Compiler correctness, ordinary
hardware, and the displayed normalization argument remain trusted.

The next pass should seek global leverage rather than another comparably tiny
fiber: either certify a substantially lower-rank cell, exclude a quantified
family of nonzero syndromes with one join, or change the parity decomposition
so that its terminal certificates remove a non-negligible part of the
normalized problem.  Solver timeouts at ranks 820 and 832 are not included as
evidence and make no mathematical claim.
