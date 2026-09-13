# Degree-22 complete occurrence relaxation at order 45

Let `G` be a hypothetical `(5,5,45)`-graph and let a root `r` have degree
22.  Put `H=N(r)`, let `X` be the 22 nonneighbours of `r`, put `Y=G[X]`, and
put `Q=complement(Y)`.  Both `H` and `Q` are `(4,5,22)`-graphs.  To test the
gate `beta(22)<=109`, complementing `G` if necessary reduces the candidate
family to

```text
110 <= e(H) <= 114,   88 <= e(Q) <= 114.
```

The endpoint values are imported from the McKay--Radziszowski complete
extremal catalogues.  Catalogue completeness and the classical Ramsey values
used below are explicit trust boundaries.

## Exact colored-deck receiver

For every valid colored induced graph type through order seven, `z_T` is its
probability on a uniformly selected set with the prescribed numbers of `H`
and `X` vertices.  The one-vertex deletion equations are imposed exactly.
Types containing `K5` or `I5`, a pure-`H` `K4`, or a pure-`X` `I4` are absent.
There are 74,332 such type variables and 10,606 base marginal equations.

For `u in H`, write `j_u=d_H(u)` and `c_u=|N(u) intersect X|`.  For `x in X`,
write `y_x=d_Y(x)`, `k_x=|N(x) intersect H|`, and `q_x=21-y_x`.  The classical
values `R(3,5)=14`, `R(4,4)=18`, and `R(4,5)=25` give the complete supports

```text
4 <= j <= 13,  19-j <= c <= min(17,23-j),
8 <= y <= 17,  max(5,20-y) <= k <= 24-y.
```

Here `c<=17` follows because the cross-neighborhood of an `H` vertex is a
`(4,4)`-graph; dually `k>=5` because the `H`-nonneighbors of an `X` vertex
form a `(4,4)`-graph of order `22-k`.

Probability variables on these 47+47 degree pairs are matched to every
bivariate centered-star factorial moment visible through order seven.  For
example,

```text
sum p_H(j,c) C(j,r)C(c,s)
 = C(22,r+1)C(22,s)/22 * E[number of H-centres in the colored star type].
```

The analogous equation is imposed for `X` centres.

## Root-cut codegree inequalities

Double counting common cross-neighbours gives the exact degree-22 rows

```text
sum_H C(c_u,2) <= sum_X q_x k_x + 3003 - 27 e(Q),
sum_X C(k_x,2) <= 17 e(H) - 2079 + sum_H c_u(21-j_u).
```

For the first row, a `Q`-edge has at most eight common `H`-nonneighbours and a
`Q`-nonedge has at most thirteen common `H`-neighbours.  The second row is the
color-dual count.  Both are encoded as order-three deck rows.

## Four triple-trace inequalities

For every independent triple in one color, the opposite-color vertices
avoiding it form a clique.  For every clique triple, the opposite-color
common neighbours form an independent set.  The pure-color root restrictions
improve two of the four caps.  Thus

```text
#(independent H-triple, avoiding X vertex) <= 4 i3(H),
#(clique H-triple, common X vertex)        <= 3 k3(H),
#(independent X-triple, avoiding H vertex) <= 3 i3(X),
#(clique X-triple, common H vertex)        <= 4 k3(X).
```

These are order-eight consequences expressed as order-four deck inequalities;
they are not consequences of merely deleting invalid types through order
seven.

## Summed local extremal inequalities

For every vertex `v`, `G[N(v)]` is a `(4,5,d(v))`-graph and the complement on
the `44-d(v)` nonneighbours is a `(4,5,44-d(v))`-graph.  The imported exact
edge intervals are

```text
m             19       20       21       22        23        24
[alpha,beta] [57,92] [68,100] [77,107] [88,114] [101,122] [116,132].
```

Summing the lower and upper endpoint inequalities over `H` centres and over
`X` centres yields eight linear rows.  The local edge counts are exact deck
statistics: triangles centred at the vertex, plus `2e(H)` for the root edges
in `H`-centred neighborhoods; dually, independent triples centred at the
vertex, plus `2e(Q)` for the root nonedges in `X`-centred nonneighborhoods.

Two local graphs contain `r` as a distinguished vertex.  If `u in H`, then
`r` has degree `j_u` in `G[N(u)]`; if `x in X`, then `r` has degree `q_x` in
the complement on the nonneighbours of `x`.  Deleting `r` intersects the
order-`m` interval with

```text
[alpha(m-1)+d_local(r), beta(m-1)+d_local(r)],
```

giving four further conditional endpoint rows.

## Integral edge-layer lift

The receiver takes the convex hull of all integral layers `e(H)=110..114`
and `e(Q)=88..114`.  In an `e`-edge order-22 graph the internal degree average
is exactly `e/11`.  Moreover deleting a vertex of internal degree `t` gives an
order-21 graph, so `77 <= e-t <= 107`.  Separate layer-degree variables impose
these statements before projecting to the degree moments.  This is a
complete-family lift; it does not enumerate individual order-22 graphs.

The numerical or exact status of the final receiver is reported separately;
feasibility would produce only a pseudomodel, not a graph.
