# Two-scale induced sampling closes the Albertson `r=27` order-54 branch

This note proves that every simple graph on 54 vertices with at least 726
edges has crossing number at least 6084.  Combined with Ankan Sadhu's
September 2026 frontier theorem, it eliminates the order-54 branch of a
possible counterexample to Albertson's conjecture at chromatic number 27.
The three order-53 edge rows remain open.

## A 32-vertex affine bound

We first prove the following universal lemma.

> **Lemma.** If `H` is a simple graph with 32 vertices and `q` edges, then
> `cr(H) >= 9q - 1573`.

Büngener and Kaufmann proved that every simple graph `J` with `v>2` vertices
and `e` edges satisfies

```text
cr(J) >= 5e - 203(v-2)/9.                         (1)
```

Fix a crossing-minimal good drawing of `H` and apply (1), including its
integer rounding, to every induced `s`-vertex subgraph.  Each edge occurs in
`binom(30,s-2)` samples and each crossing occurrence in `binom(28,s-4)`
samples.  Consequently

```text
cr(H) >= ceil(B_s(q)),

B_s(q) =
    5q binom(30,s-2) / binom(28,s-4)
  - floor(203(s-2)/9) binom(32,s) / binom(28,s-4).       (2)
```

Two sample sizes give a supporting affine line.  For `s=25`,

```text
B_25(q) = (10875q - 1862728)/1265.
```

At the upper endpoint of the range `q<=251`,

```text
B_25(251) - (9*251-1574) = 372/1265 > 0.
```

The slope of `B_25` is `2175/253 < 9`, so for every integer `q<=251`,

```text
B_25(q) > 9q-1574,
ceil(B_25(q)) >= 9q-1573.                         (3)
```

For `s=24`,

```text
B_24(q) = (50025q - 8918080)/5313.
```

At the lower endpoint of the complementary range `q>=252`,

```text
B_24(252) - (9*252-1574) = 998/5313 > 0.
```

The slope of `B_24` is `725/77 > 9`, so (3) also holds for every integer
`q>=252`.  This proves the lemma for every possible edge count.

The switch between 25- and 24-vertex samples is essential: neither fixed
sample size supplies this affine line on both sides of the threshold.

## The order-54 crossing bound

Let `G` be a 54-vertex simple graph with `m=726` edges, and fix a
crossing-minimal good drawing.  Apply the lemma to every induced 32-vertex
subgraph.  Every edge lies in `binom(52,30)` such subgraphs and every crossing
occurrence lies in `binom(50,28)` of their inherited drawings.  Hence

```text
cr(G) binom(50,28)
 >= 9*726*binom(52,30) - 1573*binom(54,32),

cr(G)
 >= 218768121/35960
  = 6083 + 23441/35960.
```

Since crossing number is integral,

```text
cr(G) >= 6084.                                    (4)
```

The right side is increasing with `m`, so (4) holds for every `m>=726`.
No criticality, degree constraint, or complement hypothesis is used in this
54-vertex theorem.

The standard complete-graph drawing gives
`cr(K_27) <= Z(27) = 6084`.  Therefore (4) implies
`cr(G) >= cr(K_27)`.  Sadhu proved that a hypothetical `r=27` counterexample
has a 27-critical subgraph of order 53 or 54, and his edge dispatch leaves
only `m=726` at order 54.  Thus the order-54 branch is impossible.  This note
does not eliminate the surviving order-53 rows `m in {713,714,715}` and does
not prove the full `r=27` case.

## Reproduction

Python 3.9 or later is sufficient; there are no third-party dependencies.

```sh
python3 verify.py
```

The verifier reconstructs (2) from binomial incidence counts, checks the two
endpoint and slope arguments, exhausts every edge count
`0 <= q <= binom(32,2)`, and verifies the final exact fraction.  It uses only
integer and rational arithmetic.

## Sources, novelty scope, and trust boundary

- A. Büngener and M. Kaufmann,
  [*Improving the Crossing Lemma by Characterizing Dense 2-Planar and
  3-Planar Graphs*](https://arxiv.org/abs/2409.01733v2), Theorem 6(b), for
  (1).
- A. Sadhu,
  [*Albertson's Conjecture Holds for r at Most
  26*](https://arxiv.org/abs/2609.01682v1), Theorem 1.3 and Section 5, for
  the two-order frontier, the four surviving edge rows, and `Z(27)=6084`.

Targeted searches of the current Albertson and crossing-lemma literature and
of the committed Discovery Net found no prior statement of the 32-vertex
supporting line or the resulting order-54 closure.  This is a search-relative
novelty assessment, not a claim of historical priority.

The mathematical trust boundary is Büngener--Kaufmann's universal inequality,
Sadhu's frontier reduction, the standard good-drawing normalization, and the
standard drawing upper bound for `K_27`.  The executable trust boundary is
CPython arbitrary-precision integers and `fractions.Fraction`; the verifier
uses no floating point for assertions, solver, randomness, external data, or
imported project code.
