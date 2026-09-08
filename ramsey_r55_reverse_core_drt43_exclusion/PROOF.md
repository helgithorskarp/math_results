# Proof of the reverse-core doubly regular tournament exclusion

For a tournament `D`, write its sign matrix as `S_xy=1` when `x -> y`,
`S_xy=-1` when `y -> x`, and `S_xx=0`. A doubly regular tournament (DRT) on
43 vertices is a regular tournament of outdegree 21 in which every pair has
10 common outneighbors. Equivalently,

```text
S S^T = 43 I - J.                                      (1)
```

Indeed, diagonal entries are 42. For two distinct vertices, the 41 other
incidences comprise ten common outneighbors, ten common inneighbors, and 21
vertices on which the two signs disagree, so their row inner product is -1.

## The fixed symmetric family

The file `core.edges` defines a tournament `U` on 21 vertices. For `i<j`, the
arc is `i -> j` precisely when `i j` is listed; every vertex has outdegree 10.
Let `A` be its sign matrix.

Consider a root `r`, its 21 outneighbors `Q`, and its 21 inneighbors `W`.
The declared family fixes `D[Q]=U` and, under some isomorphism from `W` to the
same 21 labels, fixes `D[W]` to the reverse of `U`. Every possible choice of
the 441 cross-arcs remains free. Relabeling the copy on `W` merely chooses the
isomorphism used for these coordinates, so all such labeled pairings are
included.

In the order `r,Q,W`, the sign matrix has block form

```text
    [  0    1^T   -1^T ]
S = [ -1     A      B  ],                              (2)
    [  1   -B^T    -A  ]
```

where `B` is an arbitrary 21 by 21 sign matrix before the DRT conditions are
imposed. Regularity of `D` requires every row and column sum of `B` to be 1.
The `Q,W` block of (1) is

```text
-1 - A B + B A = -1,
```

and hence

```text
A B = B A.                                             (3)
```

The `Q,Q` block of (1) is

```text
J + A A^T + B B^T = 43 I - J,
```

so every completion must also satisfy

```text
B B^T = 43 I - 2 J - A A^T.                           (4)
```

Thus it is enough to enumerate the sign matrices of row sum 1 that commute
with `A`, then check (4).

## Complete reconstruction from one row

Work over the prime field with `p=1,000,003`. Let `e_0` be the first coordinate
row vector and let `K` have rows

```text
e_0^T, e_0^T A, ..., e_0^T A^20.
```

Exact Gaussian elimination modulo `p` gives `rank(K)=21`. In particular, `K`
is invertible. If `b=e_0^T B` and (3) holds, then row `k` of `K B` is

```text
e_0^T A^k B = e_0^T B A^k = b A^k.
```

Consequently

```text
B = K^-1 [b A^k]_(k=0)^20                              (5)
```

modulo `p`. A sign row of sum 1 has exactly 11 entries `+1`, so there are
exactly `binomial(21,11)=352,716` possible first rows. Formula (5) uniquely
reconstructs every remaining entry modulo `p`. A genuine integer sign matrix
must reconstruct to `+1` or `-1` in every coordinate, so rejecting any other
residue is sound. Modular coincidences cannot create a false exclusion: every
surviving matrix is rebuilt with integer signs and checked against (3), all
row and column sums, and (4) using exact integer arithmetic.

The complete enumeration leaves exactly two commuting sign matrices:

```text
B = I + A,    B = I - A.
```

Each violates (4) on all 420 ordered off-diagonal entries. There are no
Gram-valid matrices. Therefore no DRT on 43 vertices belongs to the declared
reverse-core family.

## Why this core was target-facing

For the physical order `Q=0,...,20`, the forward graph of `U` has 98 edges,
no clique of order four, and no independent set of order five. Its reverse
has the complementary forward graph. Therefore, if the symmetric DRT
completion had existed, putting `r` first, followed by `Q` and then `W`, would
have passed the two root-neighborhood Ramsey obstructions automatically;
only mixed five-sets would have remained to test. The core was found by a SAT
scout, but that solver result and its transient formula are not proof inputs:
`core.edges` is explicit and `verify.py` checks all stated local properties.

## Scope

This proves a complete exclusion for one fixed 21-plus-21 reverse-core DRT
completion family, including all `2^441` initial cross-arc choices and all
isomorphic labelings of the reverse copy. It does not exclude other DRTs on
43 vertices, tournament-order constructions with a different pair of local
cores, regular good43 graphs of degree 20 or 22, or irregular good43 graphs.
It constructs no good43 and proves no new Ramsey lower bound.
