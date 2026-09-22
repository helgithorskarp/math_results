# Exact classification

All graphs below are finite and simple.  Write `eta(G)` for the largest `t`
such that `G` has a `K_t` minor, and write `alpha(H)` for the independence
number of `H`.  A branch-set model means pairwise disjoint nonempty connected
vertex sets, every two of which have an edge between them.

## Theorem

Let `H` be a nonempty graph with maximum degree at most two, let

```text
n = |V(H)|,   a = alpha(H),   U(H) = floor((n+a)/2).
```

Then `eta(complement(H)) = U(H)`, except for the following eight families:

```text
r K1 + C3,       r K1 + C4,       r K1 + P4,       r K1 + P5,
r K1 + C5 + P2,  r K1 + C5 + P3,  r K1 + C6 + P2,  r K1 + C6 + P3,
```

where `r >= 0` and `+` denotes disjoint union.  In every exceptional family,

```text
eta(complement(H)) = U(H)-1.
```

## 1. The universal upper bound

Consider a `K_t` branch-set model in `complement(H)`, and let `s` be the
number of singleton branch sets.  Their vertices form a clique in
`complement(H)`, hence an independent set in `H`; therefore `s <= a`.  Every
other branch set has at least two vertices, so

```text
n >= s + 2(t-s) = 2t-s.
```

Thus `2t <= n+s <= n+a`, proving `t <= U(H)`.

## 2. A canonical independent set and its forbidden graph

Every component of `H` is a path or a cycle.  Number the vertices of each
component consecutively from zero.  Choose a maximum independent set `S`
componentwise as follows:

- on a path, take the even-indexed vertices;
- on an even cycle, take the even-indexed vertices;
- on an odd cycle of order `2q+1`, take `0,2,...,2q-2`.

Put `R=V(H)-S` and `N=|R|=n-a`.  Define the *forbidden graph* `F` on `R` by
joining distinct `u,v` when either

1. `uv` is an edge of `H`, or
2. some `x` in `S` is adjacent in `H` to both `u` and `v`.

The contribution to `F` from a component of `H` is

```text
P_m       -> P_floor(m/2),
C_(2q)    -> C_q,
C_(2q+1)  -> C_(q+1),
```

where `P_0` is empty and `C_2` means the single edge `K_2`.  Consequently `F`
is a disjoint union of paths and cycles and `Delta(F) <= 2`.

Suppose `uv` is an edge of `complement(F)`.  Then `{u,v}` is connected in
`complement(H)` by condition 1, and it is adjacent to every singleton `{x}`
with `x in S` by condition 2.  Moreover, any two such pair branch sets are
adjacent to each other.  Indeed, if two disjoint pairs had no edge between
them in `complement(H)`, all four cross-edges would lie in `H`.  Since
`Delta(H)<=2`, those four vertices would form an entire `C_4` component of
`H`.  But the canonical `S` contains two vertices of every `C_4`, whereas all
four supposed vertices lie in `R`, a contradiction.

It follows that a matching of size `floor(N/2)` in `complement(F)`, together
with the `a` singleton branch sets from `S`, is a `K_U(H)` model.

## 3. The matching boundary

If `N` is even and `N>=6`, then

```text
delta(complement(F)) >= N-3 >= N/2.
```

Dirac's theorem gives a Hamilton cycle and hence a perfect matching.  If `N`
is odd and `N>=7`, delete any vertex.  The remaining graph has even order
`M=N-1` and minimum degree at least `N-4 >= M/2`, so the same argument gives a
matching covering `N-1` vertices.

The smaller orders are elementary:

- at `N=5`, minimum degree at least two forces a matching of size two (a
  graph with matching number at most one is a star, a triangle plus isolates,
  or edgeless);
- at `N=4`, a perfect matching fails exactly when `F=K_3+K_1`;
- at `N=3`, a one-edge matching fails exactly when `F=K_3`;
- at `N=2`, a perfect matching fails exactly when `F=K_2`.

For `N=3` and `F=K_3`, the graph `H` is `C_5` or `C_6` plus isolates.
Nevertheless, `complement(C_5)` has a `K_3` minor, and
`complement(C_6)` has a `K_4` minor: one parity triangle supplies three
singleton branch sets and the other parity triangle supplies the fourth
connected branch set.  Hence both attain `U(H)`.

For `N=2`, `F=K_2` occurs exactly for one of

```text
C3, C4, P4, P5
```

plus isolated vertices.  For `N=4`, `F=K_3+K_1` occurs exactly for one of

```text
C5+P2, C5+P3, C6+P2, C6+P3
```

plus isolated vertices.  These are precisely the eight listed families.

This proves the asserted lower bound for every nonexceptional graph.

## 4. Exactness for the exceptions

First take `r=0`.  In every exceptional core, `N=n-a` is even.  If a
`K_U(H)` model existed, equality throughout the upper-bound argument would
force exactly `a` singleton branch sets and would partition all other
vertices into two-vertex branch sets.  The singleton vertices would form a
maximum independent set of `H`.

For `C_3,C_4,P_4,P_5`, every maximum independent set leaves two vertices that
either are adjacent in `H` (so their pair is disconnected in the complement)
or are the two `H`-neighbors of one singleton (so their pair is not adjacent
to that singleton).

For each of the other four cores, every maximum independent set leaves three
vertices in the `C_5` or `C_6` component and one vertex in the path component.
Every pair among the three cycle vertices is forbidden: it is either an
`H`-edge or the two-neighbor set of a cycle singleton.  Two residual pairs
would therefore each need the unique path vertex, which is impossible.

The following minor models give the matching lower value.  Directly,

```text
eta(complement(C3))=1,  eta(complement(C4))=2,
eta(complement(P4))=2,  eta(complement(P5))=3,
eta(complement(C5))=3,  eta(complement(C6))=4,
eta(complement(P2))=1,  eta(complement(P3))=2.
```

For example, the even vertices of `P_5` are a 3-clique in its complement;
`complement(C_5)` is another 5-cycle; and the two parity triangles of
`complement(C_6)` give the four branch sets described above.  Complements
turn disjoint unions into joins, and clique-minor models in the two summands
combine across a join.  These values therefore give `U(H)-1` for each of the
four mixed cores as well.

Finally, adjoining an isolated vertex to `H` adds a universal vertex to its
complement.  For every graph `G`,

```text
eta(K1 + G) = 1 + eta(G).
```

The lower bound is immediate.  For the upper bound, delete the branch set
containing the universal vertex from any minor model (or observe that it was
unused); the remaining model lies in `G`.  Induction handles `r` isolates.
Since adjoining an isolate also raises `U(H)` by one, all eight exceptional
families have value exactly `U(H)-1`.

This completes the proof.

## Evidence boundary

The Python checker reconstructs all certificates through order 16 and checks
the exceptional equality obstruction by raw independent-set and pairing
enumeration.  It does not replace the parameter-uniform argument above.
Dirac's theorem and the definition of graph minors are the only imported
mathematical ingredients in the proof.
