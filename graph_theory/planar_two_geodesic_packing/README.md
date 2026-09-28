# Packing three-vertex geodesics: a proof through order 12

**Result.** Every finite simple planar graph with at most **12 vertices** has
a half-balanced separator that is the union of at most two shortest paths in
the original unweighted graph. The proof is elementary and needs no graph
enumeration. The unrestricted question in
[Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf)
remains open.

There is also a diameter reduction. If a connected planar graph on `n>=8`
vertices has diameter `D` and

```
D + 4 >= ceil(n/2),
```

then two geodesics suffice. Consequently, any connected counterexample has

```
n >= 13,          D <= ceil(n/2) - 5.
```

In particular a connected counterexample of order 13 or 14 would have diameter
2. A minimum-order counterexample must be connected.

This sharpens the team's
[previous diameter reduction and computational order-11 result](../planar_two_geodesic_finite/README.md).
That source's `D+3` criterion is replaced here by `D+4` under the clique-number
hypothesis below. Its finite conclusion is recovered by proof and extended to
order 12. No error in its computation is alleged. No priority or
paper-worthiness claim is made for these elementary observations.

## The short-path dichotomy

Write `P3` for an induced path on three vertices. In a simple unweighted graph,
every induced `P3` is an ambient geodesic: its endpoints are nonadjacent, and
its length is two. An induced `P3` in an induced subgraph remains one in the
original graph. Thus deletion does not cause a shortestness problem for this
particular path length.

A graph without an induced `P3` is a disjoint union of cliques. Indeed, a
connected noncomplete component has nonadjacent vertices, and the first three
vertices of a shortest path between them induce a `P3`.

These facts give the following general lemma; planarity is not required.

**Path-extension lemma.** Let `G` have `n` vertices and clique number
`omega(G) <= n/2`. Suppose `P` is an ambient geodesic and
`|V(P)|+3 >= ceil(n/2)`. Then `G` has a half-separator consisting of at most two
ambient geodesics.

**Proof.** If `G-V(P)` has an induced `P3`, call it `Q`. The paths `P,Q` are
vertex-disjoint and both geodesic in `G`. Their union has at least `ceil(n/2)`
vertices, so every remaining component has at most `floor(n/2)` vertices.
If no such `Q` exists, every remaining component is a clique. Each has order
at most `omega(G) <= n/2`, so `P` alone suffices. This proves the lemma.

Choosing a diametral path, which has `D+1` vertices, proves the stated diameter
bound. In a planar graph, `omega(G)<=4`, so the clique hypothesis holds for
`n>=8`.

## The order-12 theorem, including disconnected and tiny graphs

For `9<=n<=12`, a planar graph has `omega(G)<=4<n/2`. If it contains an induced
`P3`, use that path as `P` in the path-extension lemma: `3+3 >= ceil(n/2)`.
If it contains no induced `P3`, it is a union of cliques of order at most four,
so every component is already small enough and the empty separator suffices.

For `n<=8`, the following standard endpoint-cover argument works in **any**
graph. If all components have size at most `n/2`, use the empty separator.
Otherwise there is a unique larger component `H`. Choose
`min(4,|V(H)|)` distinct vertices of `H`, partition them into at most two pairs
or singletons, and take ambient shortest paths between the paired endpoints.
Their union contains all chosen vertices. The remainder of `H` has at most
`max(0,|V(H)|-4) <= max(0,n-4) <= n/2` vertices. Other components were already
small. This includes the empty graph, singleton paths, and disconnected graphs.

Finally, suppose a minimum-order planar counterexample were disconnected. It
would have a unique component `H` larger than half its total order. By
minimality, `H` has a two-geodesic separator with every component of size at
most `|V(H)|/2`, which is at most half the original order. Paths inside `H`
remain geodesic in the whole graph, and the other components are already
small. This is a contradiction. Applying the diameter lemma to a connected
counterexample gives the displayed necessary conditions.

## A general packing statement and its limit

For an integer `k>=1`, if `n<=6k` and `omega(G)<=n/2`, then `G` has a
half-separator consisting of at most `k` ambient geodesics. Greedily take
vertex-disjoint induced `P3`s. Either `k` are found, deleting `3k>=n/2`
vertices, or the residual graph has no induced `P3` and hence consists of
cliques of order at most `n/2`.

The order threshold cannot be increased for this general graph class. In
`K_(3k,3k+1)`, every geodesic has at most three vertices and contains at most
two vertices from either bipartition class. After deleting `k` geodesics,
both classes are still nonempty and at least `3k+1` vertices remain. The
remainder is connected and has more than half of the original `6k+1` vertices.
For `k=2`, this is the nonplanar graph `K_(6,7)` on 13 vertices. It is a control
for the general packing bound, **not** a counterexample to the planar question.

The argument does not apply to arbitrary edge lengths: an induced `P3` need
not be a weighted shortest path. Nor can it be repeated verbatim with induced
paths of four vertices in a unit-edge graph; three consecutive edges of a
5-cycle already give a counterexample to that shortestness assertion. These
limits matter when using the
[weighted reduction](../planar_two_geodesic_weighted_reduction/README.md).

## Reproducible constructive checks

`verify.py` implements the proof's witness construction with BFS, then
checks every returned path using Floyd--Warshall ambient distances and every
remaining component by graph traversal. Explicit fixtures cover empty and disconnected graphs,
complete graphs through order 8, order-12 planar examples, and diameter
instances above order 12. No enumeration of all planar graphs is involved.

The program also checks every geodesic pair in the nonplanar `K_(6,7)` control,
and checks the induced-`P4` warning on a 5-cycle. These are finite regression
checks; the universal conclusions follow from the proof above.

Run from the repository root with Python 3.11 or later, standard library only:

```sh
python3 graph_theory/planar_two_geodesic_packing/verify.py --check
```

Expected: `PASS`, matching `expected.json`. Tested with Python 3.11.2. There is
no external graph generator, planarity library, solver, floating-point input,
or omitted large artifact in the proof or checker. No formalization or
independent peer review is claimed here.

## Prior context

[Diot and Gavoille, Path Separability of Graphs (2010)](https://emilie-diot.eu/Article/DG10a)
already give the general `ceil(n/4)` endpoint-cover bound and two paths for
treewidth at most three. Those are prior results. The current note's role is
to replace a particular bounded computation by a direct proof, improve the
team's diameter filter, and identify the remaining small-order search range.
