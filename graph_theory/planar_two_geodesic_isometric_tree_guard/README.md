# Isometric trees with few leaves are deletion-stable geodesic fragments

Graphs are finite and simple with unit edge lengths. A singleton counts
as a shortest path. Vertex masses are arbitrary nonnegative reals. An
induced connected subgraph `T` of `G` is **isometric** when
`d_G(u,v)=d_T(u,v)` for all of its vertices. The point of this note is
an all-order terminal rule for the witness-edge descent used in
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
It does not settle that unrestricted problem.
The [independent review of the path-and-cycle rule](../planar_two_geodesic_isometric_fragment_guard_review1/REVIEW.md)
identified its `k`-path extension and branching fragments as the next
boundary; the theorem below adds an exact leaf condition for trees.

## Exact tree-cover primitive

**Lemma.** Let `T` be a tree with `L>=2` leaves. It can be covered,
including all its edges, by `ceil(L/2)` paths between leaves. Fewer
paths cannot cover all its leaves. A one-vertex tree needs one
singleton path. If `T` is isometric in `G`, each covering path is an
ambient `G`-geodesic.

**Proof.** Give `T` any plane embedding and list its leaves in cyclic
outer-face order. If `L` is odd, duplicate one leaf in this list,
placing its two copies next to each other. The resulting list has
even length `M=2 ceil(L/2)`. Pair antipodal positions `i` and
`i+M/2`, and use the unique tree path between each pair.

For every edge `e` of `T`, the leaves on either side of `T-e` form a
nonempty proper interval in this cyclic list. A nonempty proper
cyclic interval cannot be invariant under the antipodal shift, so
some pair crosses `e`; its path uses `e`. Thus the paths cover every
edge and vertex. Each tree leaf is an endpoint of every path that
contains it, so a path covers at most two distinct leaves. This gives
the lower bound. Isometry makes the unique tree path between paired
leaves shortest in `G`. QED.

The intrinsic formula is classical: see Foucaud, Majumder, Mömke and
Roshany-Tabrizi, [*Polynomial-Time Algorithms for Path Cover on Trees
and Graphs of Bounded Treewidth*](https://perso.limos.fr/ffoucaud/Publications/Papers/C34_PathCover_trees_CALDAM_2025.pdf),
Theorem 1, which credits the edge-cover formula to Harary and Schwenk
(1972). The role of the formula here is its persistence as **ambient
geodesic coverage after edge deletion**.

**Deletion-stable form.** If `T` is isometric in `G` and has at most
`2k` leaves, let `H` be any spanning edge subgraph of `G`. Every
connected vertex set `D` in `H[T]` can be covered completely by at
most `k` shortest paths in `H`. Indeed, `H[D]` is a subtree of `T`:
unique tree paths force every needed edge to survive. It has no more
leaves than `T`, since it can be obtained by successively pruning
leaves of `T`, and pruning never increases the leaf count. Apply the
pairing lemma to `H[D]`. Each selected path is still a path of `T`,
so it was shortest in `G` and remains shortest in `H`.

The `2k`-leaf threshold is sharp for this **full-coverage primitive**
when the ambient graph is the tree itself: `k` paths touch at most
`2k` leaves. This observation is not a counterexample to weighted
half balance.

## All-spanning guard theorem

**Theorem.** Fix `k>=1`. Suppose a unit-edge graph `G` has a vertex
set `S` of order at most `2k`, and every component `C` of `G-S` is
one of:

1. a component of order at most `2k`;
2. a noncomplete component of order exactly `2k+1`;
3. an induced isometric tree in `G` with at most `2k` leaves, of any
   order;
4. if `k>=2`, an induced isometric cycle in `G`, of any order.

Then **every spanning edge subgraph** `H` of `G`, under **every**
nonnegative vertex-mass assignment, has a half-balanced separator
equal to the union of at most `k` `H`-geodesics. In planar graphs and
`k=2`, the order-five nonclique condition is automatic.

**Proof.** Let total mass be `W`. If no component of `H` has mass
greater than `W/2`, use the empty union. Otherwise let `K` be its
unique heavy component. Pair the vertices of `S intersect K` and
cover them by at most `k` `H`-geodesics, using a singleton for an odd
last vertex. If this primary union is not balanced, its unique heavy
residual component `D` lies inside some `C` of `G-S`.

If `|D|<=2k`, pair its vertices. If `|D|=2k+1` and `C` is of type 2,
then `D=C` and `H[D]` is connected and noncomplete. An induced
three-vertex path in `H[D]` is an ambient `H`-geodesic; pair the other
`2k-2` vertices, using at most `k` paths in total. For type 3 use
the deletion-stable tree cover. For type 4 split the connected
path-or-cycle `H[D]` into two consecutive blocks of at most
`ceil(|D|/2)` vertices. Each block is a retained arc of length at most
`floor(|C|/2)` and is an `H`-geodesic by isometry; this is the
[cycle-fragment lemma](../planar_two_geodesic_isometric_fragment_guard/README.md).
In every case the replacement paths cover **all** of `D`. Their
deletion leaves total mass at most `W-w(D)<W/2`, regardless of
whether vertices of the primary union return. QED.

The same argument gives a protected-edge descent rule: if at most
`k` geodesics in `G` leave only the listed residual types, the
weighted conclusion holds in each spanning `H` retaining their
edges. The primary geodesics remain shortest under such deletion;
replace them completely if a heavy residual appears. This extends
the reviewed [five-residual descent](../planar_two_geodesic_weighted_guarded_descent/README.md)
and [four-vertex guard](../planar_two_geodesic_four_guard/README.md).

## A planar family beyond path and cycle fragments

Begin with the octahedron: equatorial cycle `0-1-2-3-0` and poles
`4,5`, each adjacent to all equator vertices. In a face incident
with edge `01`, insert `r` internally disjoint ears `0-a_i-b_i-1`.
At each `a_i` and `b_i`, attach two vertex-disjoint arms of length
`ell>=2`. The vertices of one ear and its four arms induce a tree
`T_i` with `2+4ell` vertices and four leaves. The ears and arms fit
in the face without crossing, so the whole graph is planar. It has
`6+r(2+4ell)` vertices, `12+r(3+4ell)` edges, and `8+r` faces.

Each `T_i` is isometric. Its only exterior ports are adjacent
vertices `a_i,b_i`; an exterior excursion between these ports takes
at least three edges through `0-1`, whereas `a_i b_i` is one edge.
Excursions returning to the same port can be removed. The equatorial
guard leaves the two poles as singletons and the four-leaf trees as
components, so the theorem applies to every spanning edge subgraph
and every mass assignment.

For `r>=5`, every four-vertex set misses one entire `T_i`. Its
remaining component has at least ten vertices and contains a vertex
of degree at least three, so it meets neither the earlier
four-vertex five- or six-fragment rules nor the path-or-cycle metric
rule. This compares these sufficient guard criteria, without a
priority claim over other positive graph classes. The attached arms
create cut vertices; this family is not asserted to be biconnected.

## Reproduce and scope

Run with Python 3.11 or later and only the standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_isometric_tree_guard/verify.py
```

The checker enumerates all labeled trees through order seven by
Prüfer sequences, audits antipodal leaf pairing and the leaf bound
for every connected induced subtree with at most four parent leaves,
and checks explicit spherical rotations, isometry, guard components,
and formulas for finite members of the planar family. The universal
statement follows from the written proof, not from this finite audit.
No arbitrary positive-edge-length claim is made.

Expected summary:

```text
labeled trees: [(2, 1), (3, 3), (4, 16), (5, 125), (6, 1296), (7, 16807)] connected subtrees of <=4-leaf parents: 600315
ears=1 arm_length=1 vertices=12 edges=19 faces=9 planar=yes isometric=yes
ears=1 arm_length=2 vertices=16 edges=23 faces=9 planar=yes isometric=yes
ears=5 arm_length=2 vertices=56 edges=67 faces=13 planar=yes isometric=yes
ears=8 arm_length=5 vertices=182 edges=196 faces=16 planar=yes isometric=yes
PASS
```
