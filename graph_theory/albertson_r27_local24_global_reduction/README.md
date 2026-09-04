# The local 24-vertex endpoint is decisive for Albertson `r=27`

This note identifies a single remaining analytic target for the current
Albertson campaign.  It proves the following conditional reduction.

> **Conditional theorem.**  If every simple graph with 24 vertices and 132
> edges has crossing number at least 165, then every simple graph with 53
> vertices and 713 edges has crossing number at least 6089.  Consequently
> Albertson's conjecture holds for chromatic number 27.

The hypothesis

```text
cr(24,132) >= 165                                      (L24)
```

is not proved here.  It is the order-24 endpoint of Pach--Radoicic--Tardos--
Toth Conjecture 5.7.  A preceding, independently reviewed campaign result
reduces its failure to two equality profiles, each with one non-full crossing
`C5`.  The new conclusion is that excluding those two profiles would settle
the whole `r=27` case, not merely the already closed order-54 branch.

## From `(L24)` to a universal order-24 line

Büngener--Kaufmann prove, for every 24-vertex simple graph with `q` edges,

```text
cr >= ceil((37q-3410)/9),
cr >= 5q-496.
```

For every integer `q<=131`, the first inequality is at least `5q-495`.
At `q=132`, hypothesis `(L24)` supplies `165=5*132-495`.  Above 132 edges,
Ackerman's sharp `6(n-2)` density bound for simple 4-planar drawings permits
iterative deletion of an edge with at least five crossings.  Deleting down
to 132 edges gives the conditional universal line

```text
cr(H) >= 5|E(H)|-495                                  (1)
```

for every simple graph `H` of order 24.

## Recursive induced sampling

Let `F_n(q)` be the exact integer lower-bound table obtained from the four
published universal lines

```text
0,
q-3(n-2),
7q/3-25(n-2)/3,
37q/9-155(n-2)/9,
5q-203(n-2)/9,
```

with integer rounding, the conditional seed (1) at order 24, and closure
under convex induced sampling.

For completeness, if `F_s` is valid at order `s` and `bar(F_s)` is its
greatest convex piecewise-linear minorant, then

```text
cr(G) >= ceil(
  C(n,s)/C(n-4,s-4)
  * bar(F_s)(m*s*(s-1)/(n*(n-1)))
).                                                     (2)
```

Indeed, sum the inherited drawings over all induced `s`-vertex subgraphs.
Every crossing survives `C(n-4,s-4)` times and every edge survives
`C(n-2,s-2)` times; Jensen's inequality for `bar(F_s)` gives (2).

The exact closure through order 52 has the pointwise supporting line

```text
5 F_52(q) >= 136q-65166                               (3)
```

for every integer `0<=q<=C(52,2)`.  Equality in the computed comparison
occurs only at `q=686,691`, where the hull vertices are `(686,5626)` and
`(691,5762)`.  Thus (3) is also transparent as the supporting line through
those two hull vertices.

Now let `G` have 53 vertices and 713 edges.  Delete every vertex from a fixed
crossing-minimal good drawing.  Each crossing survives 49 deletions, while

```text
sum_v |E(G-v)| = 53*713-2*713 = 36363.
```

Summing (3) over the 53 deletions gives

```text
49 cr(G)
 >= (136*36363-53*65166)/5
  = 298314
  = 49*6088+2.
```

Therefore

```text
cr(G) >= 6089.                                        (4)
```

Since the standard drawing gives `cr(K_27)<=Z(27)=6084`, (4) excludes the
sole surviving `(53,713)` frontier row.  The 54-vertex branch and the
714/715-edge order-53 rows are already closed unconditionally.  Sadhu's
September 2026 theorem reduces any `r=27` counterexample to those rows, so
`(L24)` implies the full conjecture at `r=27`.

## Reproduction and trust boundary

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
```

Expected conclusion:

```text
PASS conditional local-24 Albertson r=27 reduction
conditional conclusion: cr(53,713)>=6089>6084
```

The verifier constructs every table entry through order 53 with exact
integer and `fractions.Fraction` arithmetic.  It constructs each lower convex
hull independently by an orientation-based monotone chain and by pooled
adjacent secant slopes, checks that they agree, checks convexity and the
minorant inequality at every integer edge count, verifies (3) pointwise, and
checks the final deletion arithmetic.  It uses no floating point, solver,
randomness, generated input, external data, or project import.

The executable computation proves the finite conditional propagation, not
`(L24)`.  The mathematical trust boundary consists of standard good-drawing
normalization, the four cited universal crossing inequalities, Ackerman's
simple 4-planar density theorem, the convex induced-sampling lemma, Sadhu's
frontier, and the already published unconditional closures of the other
rows.

## Sources and novelty scope

- A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the order-53/54 frontier.
- A. Büngener and M. Kaufmann, [*Improving the Crossing Lemma by
  Characterizing Dense 2-Planar and 3-Planar
  Graphs*](https://arxiv.org/abs/2409.01733v2), for the `37/9` and slope-5
  universal inequalities.
- J. Pach, R. Radoicic, G. Tardos, and G. Toth, [*Improving the Crossing
  Lemma by Finding More Crossings in Sparse
  Graphs*](https://doi.org/10.1007/s00454-006-1264-9), for the `7/3`
  inequality and Conjecture 5.7.
- E. Ackerman, [*On topological graphs with at most four crossings per
  edge*](https://arxiv.org/abs/1509.01932v2), for the simple 4-planar density
  bound.
- The preceding [24-vertex equality-profile
  reduction](../albertson_r27_local_4planar_obstruction/README.md), its
  [independent review](../albertson_r27_local_4planar_obstruction_review/README.md),
  and the [recursive convex-sampling
  certificate](../albertson_r27_recursive_convex_sampling/README.md).

The local inequality is a specialization of an existing conjecture, and its
two-profile reduction is prior campaign work.  Targeted current primary-
literature and committed-graph searches found no prior observation that this
single order-24 endpoint conditionally closes the later sole order-53 row via
recursive sampling.  This is a search-relative novelty statement, not a
claim of historical priority.
