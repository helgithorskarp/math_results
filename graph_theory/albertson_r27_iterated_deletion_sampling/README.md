# Iterated deletion sampling at the Albertson `r=27` frontier

This note strengthens two of the three surviving order-53 crossing-number
floors in Ankan Sadhu's September 2026 reduction.  It does **not** prove
Albertson's conjecture for chromatic number 27.

## Result

Let `G` be a 27-critical graph.  Then:

```text
|V(G)| = 53, |E(G)| = 713  implies  cr(G) >= 6010,
|V(G)| = 53, |E(G)| = 715  implies  cr(G) >= 6066.
```

The previous integer-aware induced-sampling conclusions were respectively
6009 and 6064.  The middle survivor `(53,714)` remains at 6037 under the
estimates used here.  All three conclusions remain below
`Z(27) = 6084`, so the order-53 branch is not closed.

The proof uses only criticality's minimum-degree consequence
`delta(G) >= 26`; connectedness of the complement is not needed.

## Local integer-sampling estimate

Büngener and Kaufmann proved that every simple graph `H` with `v > 2`
vertices and `e` edges satisfies

```text
cr(H) >= 5e - 203(v-2)/9.                         (1)
```

Apply (1), including its integer rounding, to every induced `s`-vertex
subgraph of an `N`-vertex, `q`-edge graph.  Double-counting edges and
crossings gives

```text
cr(H) >= ceil(B(N,q,s)),                           (2)

B(N,q,s) =
    5q (N-2)(N-3) / ((s-2)(s-3))
  - floor(203(s-2)/9) N(N-1)(N-2)(N-3)
      / (s(s-1)(s-2)(s-3)).
```

Indeed, each edge occurs in `binom(N-2,s-2)` samples and each crossing in a
good drawing occurs in `binom(N-4,s-4)` samples.  The floor in (2) comes from
rounding (1) separately on each sample.

Two elementary consequences of (2) are all that will be used:

```text
N = 52 and q <= 687:  cr(H) >= 27q - 12969,        (3)
N = 51 and q <= 664:  cr(H) >= 27q - 12686.        (4)
```

For (3), choose `s=24`.  At `q=687`,

```text
B(52,687,24) = 4234475/759 = 5579 + 14/759,
```

so its ceiling is 5580, the right side of (3).  When `q` decreases by one,
`B(52,q,24)` decreases by `20125/759`, whereas the right side of (3)
decreases by `27 = 20493/759`.  Thus the required strict inequality before
rounding only becomes stronger.

For (4), choose `s=24` when `q <= 661`.  At the endpoint,

```text
B(51,661,24) = 1305640/253 = 5160 + 160/253,
```

whose ceiling is 5161, the right side of (4).  Decreasing `q` by one lowers
this sampled value by `1960/77 = 6440/253`, less than 27, so the estimate
persists.  The only remaining values follow by choosing `s=23`:

```text
B(51,662,23) = 119308/23 = 5187 + 7/23,
B(51,663,23) = 119952/23 = 5215 + 7/23,
B(51,664,23) = 120596/23 = 5243 + 7/23.
```

Their ceilings dominate `5188`, `5215`, and `5242`, respectively, proving
(4).

## One-vertex deletion at `(53,713)`

Fix a crossing-minimal good drawing of `G`.  For each vertex `v`, its
inherited deletion has 52 vertices and `713-d(v) <= 687` edges.  By (3),

```text
cr(G-v) >= 27(713-d(v)) - 12969
        = 5580 - 27(d(v)-26).
```

Every crossing survives in exactly 49 of the 53 vertex-deleted drawings.
Criticality and the handshake lemma give

```text
sum_v (d(v)-26) = 2*713 - 53*26 = 48.
```

Consequently,

```text
49 cr(G) >= 53*5580 - 27*48 = 294444,
cr(G) >= ceil(294444/49) = ceil(6009 + 3/49) = 6010.
```

## Two-vertex deletion at `(53,715)`

For every vertex pair `T`, the graph `G-T` has 51 vertices.  Since both
deleted vertices have degree at least 26, its edge count `q_T` is at most
`715-26-26+1 = 664`.  Hence (4) applies to every pair.

Summing over all `binom(53,2)` pairs does not require knowing any degrees or
adjacencies: each original edge survives in exactly `binom(51,2)` pair
deletions.  Likewise, each crossing survives exactly when both deleted
vertices avoid its four endpoints, hence in `binom(49,2)` pair deletions.
Therefore

```text
binom(49,2) cr(G)
  >= 27*715*binom(51,2) - 12686*binom(53,2)
   = 7132567,

cr(G) >= ceil(7132567/1176)
      = ceil(6065 + 127/1176)
      = 6066.
```

## Reproduction

Python 3.9 or later is sufficient; there are no third-party dependencies.

```sh
python3 verify.py
```

The verifier uses only integer arithmetic and `fractions.Fraction`.  It
reconstructs (2) in both its binomial-count and simplified forms, checks the
two local affine estimates over every relevant integer edge count, and
verifies the deletion multiplicities and final exact fractions.

## Sources, scope, and trust boundary

- A. Sadhu, [*Albertson's Conjecture Holds for r at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the four surviving
  order/size pairs and `Z(27)=6084`.
- A. Büngener and M. Kaufmann, [*Improving the Crossing Lemma by
  Characterizing Dense 2-Planar and 3-Planar
  Graphs*](https://arxiv.org/abs/2409.01733v2), Theorem 3.9(b), for (1).

The imported mathematical inputs are (1), the standard good-drawing
reduction, and the fact that a 27-critical graph has minimum degree at least
26.  The induced-sampling and deletion arguments are proved above.  The
executable trust boundary is CPython's exact integer and rational arithmetic;
the verifier uses no floating point for assertions, solver, randomness,
external data, or project imports.

This is an analytic refinement of the existing integer-aware sampling
method.  It neither classifies residual critical graphs nor resolves the
24-vertex 4-planar obstruction for the order-54 branch.
