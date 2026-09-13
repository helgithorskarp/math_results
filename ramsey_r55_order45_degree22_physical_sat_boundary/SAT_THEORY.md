# Complete physical degree-22 gate encoding

Fix a root `r` of a hypothetical `(5,5,45)`-graph with degree 22.  Relabeling
its neighbors as `H={0,...,21}` and its nonneighbors as `X={22,...,43}` loses
no graph and assumes no automorphism.  For every pair of nonroot vertices the
original CNF variable is the indicator of an edge of `G`.

For each five-set of nonroot vertices, one ten-literal clause forbids a clique
and its sign-dual clause forbids an independent set.  A five-set containing
the root can be forbidden only when its other four vertices are all in `H`
(a clique) or all in `X` (an independent set), giving the two families of
six-literal root clauses.  Consequently the original-variable clauses are
equivalent to `G` having no `K5` or independent five-set.

Within `H`, a positive edge literal contributes to `e(H)`.  Within `X`, a
negative edge literal contributes to `e(Q)`, where `Q=complement(G[X])`.
Sequential counters encode

```text
e(H) >= 110,              e(H)+e(Q) >= 220.
```

The counter encodes `sum x_i <= k` with forward variables `s[i,j]`.  Its
clauses propagate every true input prefix count forward; a `(k+1)`st true
input conflicts with the overflow clause.  Conversely, when at most `k`
inputs are true, setting `s[i,j]` exactly when the first `i+1` inputs contain
at least `j+1` true values satisfies every clause.  The independent
`verify_sequential_counter.py` exhausts all fixed input assignments through
ten inputs and confirms that unit propagation conflicts exactly above the
bound.

If `e(H)+e(Q)>=220`, at least one of `e(H),e(Q)` is at least 110.  Complementing
the whole graph swaps the two root sides, so orienting `e(H)>=110` is complete.
Thus:

- SAT yields a literal good45, verified independently by testing all
  `C(45,5)` vertex sets and both cardinalities;
- UNSAT, with a checked proof trace, establishes the full paired occurrence
  bound `e(H)+e(Q)<=219` for every degree-22 root;
- that paired bound is strictly below the height-3501 threshold 220 and hence
  completes the degree-22 order-45 inequality.

The optional exact split `e(H)=110,...,114` is exhaustive because every
`(4,5,22)`-graph has at most 114 edges under the imported complete extremal
boundary.  It is a five-class structural split, not a graph catalogue sweep.

The generated unsplit instance has 946 original variables, 139,392 auxiliary
variables, and 2,465,397 clauses.  Exact-layer instances each have 165,638
variables and 2,516,008 clauses.  Catalogue completeness is used only for the
upper endpoint 114 in the five-way join, not for the unsplit encoding.
