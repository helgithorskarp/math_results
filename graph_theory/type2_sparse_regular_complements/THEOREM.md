# Sparse regular complements without a 1-factor are Type 2

All graphs are finite and simple.  A total colouring assigns colours to the
vertices and edges so that adjacent vertices, adjacent edges, and incident
vertex-edge pairs have different colours.  Its minimum number of colours is
denoted by `chi''(G)`.  A graph is **Type 2** when
`chi''(G)=Delta(G)+2`.

## 1. The parity--matching obstruction

### Lemma

Let `G` be a `d`-regular graph of even order `N`.  If `G` has a total
colouring with `d+1` colours and `alpha(G)<=3`, then the complement of `G`
has a perfect matching.

### Proof

Fix a colour `c`.  Let `s_c` be the number of vertices coloured `c` and let
`e_c` be the number of edges coloured `c`.

At each vertex `v`, the vertex itself and the `d` incident edges are `d+1`
pairwise conflicting elements.  A total colouring with exactly `d+1`
colours therefore displays every colour exactly once among those elements.
Counting the occurrences of `c` over all vertices gives

```text
s_c + 2 e_c = N.                                      (1)
```

Because `N` is even, every `s_c` is even.  The vertices coloured `c` form an
independent set in `G`, so `s_c<=alpha(G)<=3`.  Consequently every nonempty
vertex-colour class has size exactly two.  Its two vertices are nonadjacent
in `G`, hence adjacent in the complement.  The nonempty colour classes
partition `V(G)` into disjoint complement edges, which is a perfect matching.
This proves the lemma.  (It is the needed special case of the classical fact
that every Type-1 graph is conformable.)

## 2. Exact theorem

### Theorem

Let `H` be a `K_4`-free `r`-regular graph of even order `N`, and suppose
that `H` has no perfect matching.  Put

```text
G = complement(H).
```

If either

```text
(a) r <= 4,
```

or

```text
(b) N > 4r+2,
```

then

```text
chi''(G) = Delta(G)+2 = N-r+1.                        (2)
```

### Proof

The complement `G` is regular of degree

```text
d = N-1-r.
```

Since independent sets of `G` are cliques of `H`, the `K_4`-free hypothesis
gives `alpha(G)<=3`.  If `G` admitted a `(d+1)`-total-colouring, the lemma
would give a perfect matching of `H`, contrary to hypothesis.  Hence

```text
chi''(G) >= d+2.                                      (3)
```

For (a), `d=N-1-r>=N-5`.  Yap and Chew proved the Total Colouring
Conjecture for every graph of order `N` and maximum degree at least `N-5`, so
`chi''(G)<=d+2`.

For (b), the displayed inequality is equivalent to

```text
N-1-r > 3N/4 - 1/2.
```

Chew's high-maximum-degree theorem again gives `chi''(G)<=d+2`.
Combining either upper bound with (3) proves (2).

### What is structural here

No enumeration or total-colouring search is used.  Once an input graph `H`
is certified to be regular, `K_4`-free, and without a perfect matching, its
complement is certified Type 2 throughout the two stated density regimes.
For `r<=4` the conclusion has no order threshold.

## 3. An explicit connected cubic family

For `m>=4`, let `P_m=C_m square K_2` be the prism with vertices `(i,b)`,
where `i` is modulo `m` and `b` is zero or one.  Its edges are

```text
(i,b)--(i+1,b)  and  (i,0)--(i,1).
```

Take three disjoint copies of `P_m`.  In each copy subdivide the rung
`(0,0)--(0,1)` once, calling the new vertex `s_j`.  Add a new vertex `x` and
the three edges `x--s_j`.  Call the resulting graph `H_m`.

Every old prism vertex still has degree three, each `s_j` has its two
subdivision neighbours and `x`, and `x` has the three neighbours `s_j`.
Thus `H_m` is connected and cubic.  It is triangle-free: prisms with
`m>=4` are triangle-free, subdivision creates no triangle, and the three
neighbours of `x` lie in different copies.

Each edge `x--s_j` is a bridge.  More generally, if `e` is a bridge of a
cubic graph, each component of the graph minus `e` has odd order, since

```text
3|C| = 2|E(C)| + 1.
```

Every perfect matching must therefore use `e`.  A perfect matching of
`H_m` would have to contain all three bridges at `x`, which is impossible.
The theorem with `r=3` now yields

```text
|V(H_m)| = 3(2m+1)+1 = 6m+4,
Delta(complement(H_m)) = 6m,
chi''(complement(H_m)) = 6m+2.                        (4)
```

This supplies a connected infinite family beyond the classical
complement-degree-two case.

## 4. Scope

The direct parity lemma and the conformability necessity behind it are
classical.  The upper bounds are also quoted theorems.  The contribution is
the exact sparse-complement criterion and its explicit connected cubic
family, obtained by combining those ingredients.  No claim is made that all
complements of cubic graphs are classified, or that conformability is
sufficient for Type 1.
