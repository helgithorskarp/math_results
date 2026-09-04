# Independent review evidence for the conditional local-24 reduction

This directory supplies a definition-level independent reproduction of the
finite computation in
[`albertson_r27_local24_global_reduction`](../albertson_r27_local24_global_reduction/README.md).
It checks the conditional claim

```text
cr(24,132) >= 165  ==>  cr(53,713) >= 6089 > Z(27)=6084.
```

The hypothesis on 24 vertices is **not** proved by either computation.

## Independent method

`verify_review.py` reconstructs every recursively sampled integer lower-bound
table through order 53.  Unlike the reviewed verifier's monotone-chain and
pooled-adjacent-slope algorithms, it constructs every lower convex envelope
by exact recursive QuickHull farthest-point splits.  It also writes the four
universal bounds as integer numerator/denominator formulae and replaces
binomial coefficients in the sampling multiplier by the equivalent ratio of
four falling factorials.

The checker audits every QuickHull envelope pointwise, checks two
hand-verifiable nonconvex/convex examples, verifies the order-24 arithmetic,
tests the order-52 supporting line at every edge count, and verifies the final
53 vertex-deletion double count.  Agreement includes the complete table
digest, not only the aggregate conclusion.

## Reproduction

Requirements: CPython 3.9 or later; no third-party packages.

```sh
python3 verify_review.py
```

Expected output:

```text
PASS independent QuickHull reproduction
assumption: cr(24,132)>=165
F_52(686)=5626; F_52(691)=5762
5 F_52(q) >= 136q-65166, equality only at q=686,691
conditional conclusion: cr(53,713)>=6089>6084
conditional_recursive_table_sha256=79e615e691c84d697b2dbc3d6fded0d9657c37d3f91f4bebc1a61097fb39f7f6
```

## Scope and trust boundary

The exact computation independently validates the conditional propagation.
It relies on CPython arbitrary-precision integers and `fractions.Fraction`.
There is no floating point, solver, randomness, external input, generated
certificate, or import from the reviewed directory.

The mathematical trust boundary remains the unproved local hypothesis,
standard good-drawing normalization, the published universal crossing bounds,
Ackerman's simple 4-planar density theorem, convex induced-subgraph sampling,
Sadhu's 2026 frontier, and the already established unconditional closures of
the other frontier rows.  In particular, this evidence does not prove
Albertson's conjecture at chromatic number 27 unconditionally.

Primary sources checked for the review:

- A. Büngener and M. Kaufmann,
  [Theorem 6](https://arxiv.org/abs/2409.01733), for the universal `37/9` and
  slope-5 inequalities.
- E. Ackerman,
  [Theorem 4](https://arxiv.org/abs/1509.01932), for the `6n-12` simple
  4-planar density threshold.
- A. Sadhu,
  [Section 5](https://arxiv.org/abs/2609.01682), for the surviving
  `(53,713..715)` and `(54,726)` frontier rows.
