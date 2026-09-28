# Two geodesics when the nonneighbors of a vertex are disjoint cliques

**Computer-assisted structural theorem.** Let `G` be a finite simple planar
graph with unit edge lengths. Suppose some vertex `r` satisfies

```
G[V(G) - N[r]] is a disjoint union of cliques.
```

For every assignment of nonnegative real vertex masses, there is a
half-balanced separator equal to the union of at most two paths that are
shortest in the **original** graph. The paths can each have at most two
edges, so the separator has at most six vertices. Singleton paths are
allowed. The graph also has a tree decomposition of width at most five.

The number and orders of the components outside `N[r]` are not bounded in
the hypothesis. Planarity itself bounds each clique order by four. There
is no radius-two assumption: an outside clique may have vertices at
distance three from `r`.

The proof extends the team's
[independent-nonneighbors theorem](../planar_two_geodesic_independent_non_neighbors/README.md).
Its new step replaces a clique patch by a small decomposition whose bags
are covered by two ambient geodesics. A complete finite certificate checks
**751 cores of order at most ten**. This is a proof for an unbounded graph
class, not a census of small planar graphs. Its topological reduction is
a written argument; the finite core lemma is computer-assisted.

This does not settle [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
Arbitrary edge lengths are not covered, and literature priority is not
established. The source and checker are an author-produced certificate,
not an independent review.

## 1. Why covered decomposition bags give exact half balance

Assign each vertex's mass to one bag containing it. A weighted centroid of
the decomposition tree has at most half the total assigned mass on every
side. After its bag is deleted, each remaining graph component occurs
entirely on one side: each surviving vertex has a connected occurrence
subtree avoiding the centroid, and adjacent surviving vertices occur
together in a bag. Thus a centroid bag is a half-balanced separator.

If each bag is contained in the union of two ambient geodesics, use the
cover of the centroid bag. Additional deletions only shrink components.
This argument handles all nonnegative real masses; zero total mass is
immediate. We therefore construct a decomposition with such covers.
All covers below use paths of at most two edges.

## 2. Reduce each outside clique to at most three active vertices

Work first in the connected component of `r`, and write `B=N(r)`. Let `C`
be a clique component of `G-N[r]`. Call its vertices with neighbors in `B`
*active*. There is at least one active vertex.

An inactive vertex has neighbors only in `C`, so its neighborhood is a
clique of order at most three. Remove all inactive vertices for now. They
will be restored by attaching one bag containing the whole original `C`,
of order at most four, to a bag containing its active clique. Two edges
(or singletons for smaller orders) cover such a bag.

There are at most three active vertices in `C`. Indeed, `N[r]` is connected.
Contract it to one vertex, keeping four hypothetical active vertices of
`C`. Their clique together with the contracted vertex would give a `K5`
minor. This is impossible in a planar graph.

Denote an active clique by `A={x_1,...,x_k}`, where `1<=k<=3`, and its
distinct neighbors in `B` by `Y_A`. Every `x_i` has a neighbor in `Y_A`.
All later shortestness checks concern the original graph, including the
inactive vertices. An induced path with two edges stays shortest regardless
of these other vertices.

## 3. Separate the active cliques into outerplanar patches

The following planar replacement is the polygon construction used in the
independent-nonneighbors proof, applied after contracting the active
cliques. We give the details needed for the restoration step.

Contract each connected `A` to a center `s_A`, temporarily retaining its
incident edge ports. These centers are independent. Apart from possible
parallel spokes to the same neighbor, the resulting graph has vertex set
`{r} union B union {s_A}`, and `r` is adjacent to all of `B`.

The ports to any one `b` can be made consecutive around `s_A`. Two parallel
`s_A-b` spokes bound a region on the side away from `r`. That region
contains no other vertex of `B`, since its edge to `r` would have to cross
the boundary. A different center inside that region can have neighbors
only at `b`; it is a one-neighbor attachment, which can be reattached
separately. Thus suppressing repeated spokes retains the cyclic order of
the distinct neighbors and loses no patch with three or more neighbors.

Replace a center with at least three distinct neighbors by the polygon
through those neighbors in their cyclic order. Its replacement edges
follow thin neighborhoods of consecutive spokes. The polygon bounds a
distinguished face `F_A`. A center with two neighbors `a,b` instead gives
a fill edge `ab`; a center with one neighbor gives an attachment at that
neighbor. These replacements are simultaneous: the centers and open
spokes have disjoint neighborhoods, and at shared vertices of `B` they
use their separate incident sectors.

Parallel polygon or fill edges can be simplified. A digon away from `r`
contains no third vertex of `B`, for the same reason as above. In
particular it contains no distinguished face whose boundary has at least
three vertices. Low-degree attachments are retained at their endpoint or
endpoint pair when such digons are collapsed.

The resulting simple graph on `{r} union B` still has a universal `r`.
Deleting `r` leaves an outerplane graph `H` containing all original edges
within `B`, the two-neighbor fill edges, and the distinguished bounded
faces `F_A`. Inverse contraction restores each active clique and its
original spokes inside its own patch: the original port rotation was
retained, and several ports at one boundary vertex occupy consecutive
sectors. Equivalently, the replacement polygon can be drawn around a thin
neighborhood of the clique and its spokes before the contraction.

Complete `H` to an outerplane polygon dissection, preserving the faces
`F_A` and triangulating every other bounded region. Connecting components
and completing the outer boundary uses only the outer face. The weak dual
of this dissection is a tree. All added edges are **decomposition edges**;
they are never added to the shortest-path metric.

An ordinary triangular face with vertices `a,b,c` gets the bag
`{r,a,b,c}`. It is covered by the edge `ra` and by `bc` if that edge is
original, or by `b-r-c` otherwise. A distinguished face will instead get a
local decomposition described below. Adjacent face decompositions will
be joined along a bag containing `{r,a,b}` for their shared boundary edge
`ab`. One- and two-neighbor patches attach along `{r,a}` or `{r,a,b}`.

For `|B|<=2`, use `{r} union B` as the base bag and attach these small
patches directly; there is no polygon completion to perform.

## 4. The order of the spokes and the fan reduction

Consider one patch with active clique `A` and boundary vertices `Y_A`.
No original edge joins nonconsecutive vertices of its boundary: such an
edge would belong to `H` and contradict its being a bounded face in an
outerplane embedding. The one- and two-neighbor cases have the same
interpretation with a point or a two-sided edge as boundary.

The spokes from `x_1,...,x_k` occur in **k consecutive groups** around the
patch, after choosing the order of these vertices and a starting point.
Here is a topological justification. The connected graph on `N[r]` lies
in one face of the embedded clique. For `k=3`, fill the triangular face
on the other side; for `k=1,2`, take a regular neighborhood of the vertex
or edge. The resulting disk has one boundary arc at each `x_i`. All
outgoing spokes at `x_i` lie on that arc. Disjoint spokes in the annulus
between this disk and the patch boundary preserve cyclic order. Ports
ending at the same boundary vertex occur consecutively there. Thus both
the source groups and the repeated destination groups are cyclic
intervals. This argument also applies to a boundary with one or two
distinct vertices by retaining its two-sided neighborhood.

For each source `x_i`, retain its first and last boundary neighbors in
this order. These may be equal. Every other neighbor strictly inside this
fan is adjacent to no other member of `A`: a port from another member
would interrupt the consecutive source group. Eliminate these interior
fan vertices in order, retaining the endpoints. A vertex `t` being
eliminated has later neighbors contained in

```
{r, x_i, a, b},
```

where `a,b` are the neighboring remaining boundary vertices of its fan.
Thus its bag is contained in `{r,x_i,a,t,b}`. It is covered by the ambient
geodesic `r-t-x_i` and a shortest `a`--`b` path: use their edge when
original and `a-r-b` otherwise. If `a=b`, use that singleton. These covers
use only original edges and have at most two edges per path.

For the elimination, complete the bag's remaining neighborhood to a
clique. The only new kinds of edges are consecutive boundary edges and
`r x_i`. Edges within `A` already exist. Every original boundary edge,
together with `r`, occurs in a bag during this elimination or survives in
the central core. This will allow the other patches to be attached later.

After all these eliminations, there are at most `2k` remaining boundary
vertices. List the retained endpoint slots as

```
(first(x_1), last(x_1), ..., first(x_k), last(x_k)).
```

Equal slots form cyclic intervals: this follows from the consecutive
destination groups above. The distinct endpoints have their cyclic order
on the boundary. This reduces all patch sizes to a finite list.

## 5. The finite core lemma and its complete certificate

The lemma is stated for every following abstract core; no planarity test
is used to prune the list.

Choose `1<=k<=3` and a partition of `2k` cyclically ordered slots into
cyclic intervals. There is also the one-class partition. Give the classes
canonical labels `0,1,...,m-1` by first appearance in the slot word `L`.
Use vertices

```
r=0;   x_i=i (1<=i<=k);   y_j=k+1+j (0<=j<m).
```

The **actual core** `Q` has the clique on the `x_i`, all edges `r y_j`,
and the spokes from `x_i` to the classes in slots `2i-2` and `2i-1`.
It may also contain **any subset** of the boundary-cycle edges between
consecutive distinct classes. For `m=2` this is one optional edge, and
for `m=1` there is none.

The **filled core** `Q+` adds every boundary-cycle edge and every edge
`r x_i`. These additions are not part of the metric. The fan elimination
leaves a subgraph of `Q+`, so decomposing `Q+` suffices.

**Finite core lemma.** Every `Q+` in this list has a tree decomposition
with bags of size at most six, each covered by two paths of at most two
edges that are shortest in `Q`. Moreover, each boundary edge `ab` has a
bag containing `{r,a,b}`; each boundary vertex `a` has a bag containing
`{r,a}`.

The exact list and verification are:

| Active clique order | Cyclic interval partitions | Actual edge patterns |
| --- | ---: | ---: |
| 1 | 2 | 3 |
| 2 | 12 | 61 |
| 3 | 58 | 687 |
| Total | 72 | 751 |

The 148,645-byte [certificate](certificate.jsonl) provides an elimination
order for `Q+` and two explicit paths for every resulting bag.
[verify.py](verify.py) independently enumerates all cyclic interval
partitions by restricted-growth words, checks complete case coverage,
performs the prescribed elimination by mutable sets, and validates the
resulting tree decomposition. It checks every path against exact
Floyd--Warshall distances in `Q`, and checks all interface bags.
The checker does not import or call the certificate generator.

In total it checks **5,972 core bags**, including 432 bags of size six.
Certificate SHA-256:

```
c04c7fc4a8a185b00afe06601b263757a48ac6b879592ce7a9aa3c7f6eb1410b
```

The optional [generator](build_certificate.py) searches elimination
prefixes using bitmask reachability and enumerates interval partitions by
cut sets. Its output is not trusted without checking. Both scripts use
only the Python standard library, exact integers, and graphs of at most
ten vertices for the finite lemma.

The actual core is an induced subgraph of the original graph on its
remaining vertices. Every certified path has at most two edges. Its
shortestness therefore persists in the whole graph: an edge cannot be
shortened, and the endpoints of a certified two-edge path are nonadjacent
in the original graph. Outside vertices cannot supply a path of length
less than two between these endpoints.

## 6. Glue the decompositions and restore the inactive vertices

Combine the core decomposition with the fan elimination bags. This is a
decomposition of the local filled patch, which includes its boundary
cycle and all edges from `r` to its boundary. Consequently every boundary
edge `ab` has a bag containing `{r,a,b}`: these three vertices form a
clique in the auxiliary graph. The elementary clique-in-a-bag property
follows from the Helly property of subtrees of a tree. The checker also
verifies the core interfaces explicitly.

Replace each distinguished-face node in the dissection's weak dual by
this local decomposition, and join the two chosen interface bags for
each shared boundary edge. Replace an ordinary face by its four-vertex
bag. Since the weak dual is a tree, replacing its nodes by trees and
joining along its edges again gives a tree. Vertex occurrences remain
connected: at every common interface, the shared vertices `r,a,b` are
present in both attachment bags. This also covers every original edge.
One- and two-neighbor patches attach by a single tree edge at their
designated interfaces.

Restore the inactive vertices of each outside clique by its original
clique bag of order at most four. The active vertices form a clique and
therefore occur together in a bag to which this new leaf bag can attach.
All bags have size at most six and the covers described above use at most
two ambient geodesics of at most two edges each. Section 1 now proves
the weighted half-balance assertion for the connected component of `r`.

Every other connected component of `G` is a clique of order at most four.
If any such component has more than half the total mass, delete it using
two edges or smaller paths. There can be at most one such component.
Otherwise apply the connected argument to the component of `r`; all other
components already satisfy the required bound. Tree decompositions for
the separate clique components can also be joined by arbitrary tree
edges, proving the treewidth assertion for disconnected graphs.

## 7. What this adds, and what remains

A graph is a disjoint union of cliques exactly when it has no induced
three-vertex path. Thus any counterexample to Problem 31 must satisfy

```
for every r, G[V(G)-N[r]] contains an induced three-vertex path.
```

In particular its maximum degree is at most `n-4`. This strengthens the
previous requirement of an edge among every vertex's nonneighbors.
It leaves the case of a three-vertex **path** outside one closed
neighborhood untreated. Neither arbitrary diameter-two graphs nor
arbitrary edge metrics have been resolved.

The width-five bound is attained. Take a nine-cycle `1,...,9`, a vertex
`0` adjacent to the whole cycle, and a triangle on `10,11,12`. Join `10`
to `9,1,2,3`, `11` to `3,4,5,6`, and `12` to `6,7,8,9`. Draw the triangle
inside the nine-cycle with these three fans, and `0` on the other side.
This is the first order-13 exceptional triangulation in the team's
[order-14 proof](../planar_two_geodesic_triangulation14/README.md),
graph6 `L|eKKE@oJ_bp?~`. Its nonneighbors of `0` are a triangle.

The only vertex sets that can occur as prefixes of an elimination with
bags of size at most five are the 64 subsets of `{1,2,4,5,7,8}`. This is
checked exactly in `verify.py`. After those six fan vertices are removed,
the filled graph is a universal vertex joined to an octahedral graph,
with minimum degree five. No width-four elimination can finish. Together
with the theorem's decomposition this gives treewidth exactly five.
This lower-bound check concerns decomposition width, not a new census of
the already settled order-13 separator question.

The six-vertex wheel from the preceding note still obstructs the naive
operation of putting an entire edge patch in one bag. The finite lemma
instead decomposes the patch, so it does not assume that every possible
six-vertex bag is coverable.

[Diot and Gavoille, *Path Separability of Graphs*
(2010)](https://emilie-diot.eu/Article/DG10a) provide the weighted-centroid
framework, the general treewidth bound, and earlier positive classes.
The treewidth bound alone would give three paths at width five. The
contribution here is the two-geodesic cover of the decomposed clique
patches. Targeted primary-literature searches did not identify this exact
extension; that is not a priority claim.

## 8. Reproduction and limits of the computation

From the repository root, with Python 3.11 or later:

```sh
python3 graph_theory/planar_two_geodesic_cluster_non_neighbors/verify.py --check
```

To regenerate the certificate before verifying it:

```sh
python3 graph_theory/planar_two_geodesic_cluster_non_neighbors/build_certificate.py
python3 graph_theory/planar_two_geodesic_cluster_non_neighbors/verify.py --check
```

[expected.json](expected.json) records `PASS`, all 751 cores and 5,972 bag
covers, five expanded fixtures with 137 additional bag covers, 149 mass
assignments, the width-four obstruction, and six rejected invalid
controls. The expanded fixtures include long fans, deleted boundary
edges, two patches glued along an interface, and an inactive fourth
clique vertex. These fixtures test implementation details; they are not
the proof of the unbounded structural reduction.

The trust boundary is the written planar patch and fan-order arguments,
the elementary weighted-centroid theorem, the complete small certificate,
and the exact checker. No external solver, planar graph enumerator,
floating-point calculation, or omitted search transcript is a premise.
