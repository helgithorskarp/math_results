# Two geodesics when the vertices outside a closed neighborhood are independent

**Theorem.** Let `G` be a finite simple planar graph with unit edge lengths.
Suppose there is a vertex `r` such that

```
X = V(G) - N[r]
```

is an independent set. For every assignment of nonnegative real vertex
masses, `G` has a half-balanced separator equal to the union of at most two
paths that are shortest in the original graph. Singleton paths are allowed.

The hypothesis permits arbitrarily many vertices outside `N[r]`. In
particular, the theorem includes every planar bipartite graph of radius at
most two, as well as graphs with a vertex adjacent to all but one of the
other vertices. It extends the planar universal-vertex case to a larger
class. It does **not** settle the assertion for all planar graphs or even
all planar graphs of diameter two. No literature-priority claim is made.

The proof constructs a tree decomposition with bags of size at most five.
Every five-vertex bag has the special form

```
{r, x, a, b, c},   rx not an edge,
                  a,b,c all adjacent to both r and x.
```

It is therefore exactly covered by `r-a-x` and either the edge `bc`, if
present, or the path `b-r-c`. Both are ambient geodesics. This special bag
structure, rather than treewidth four alone, is the useful conclusion.

## 1. A planar completion around the independent vertices

First suppose `G` is connected and put `B=N(r)`, so every neighbor of a
vertex in `X` belongs to `B`. Fix a plane embedding, with the point `r`
in the face that will be designated exterior after `r` is removed.

For each `x` in `X` with degree at least three, list its distinct neighbors
in their cyclic order about `x`. Erase `x` and its incident edges and join
consecutive neighbors around this order. The new edges follow the two old
spokes through their intervening angular sector. They bound a polygonal
face `F_x` whose boundary is exactly the neighbor list of `x`.
For a degree-two vertex with neighbors `a,b`, erase the vertex and replace
its two edges by a fill edge `ab`. Erase degree-one vertices without adding
an edge.

Here is why these operations can be performed simultaneously. The erased
centers are independent, so their incident open edges are distinct. Choose
thin neighborhoods of these open stars with disjoint interiors; near a
shared vertex in `B`, use the separate angular sectors of its incident
edges. The replacement curves stay in these neighborhoods. Consequently
the interiors of the faces `F_x` are disjoint and contain no other surviving
vertex or edge. All edges incident with `r` remain in place.

Temporarily allow parallel replacement edges, including a replacement
parallel to an old edge. They cause no difficulty. For two parallel `ab`
edges, the region between them that excludes `r` contains no vertex of `B`
other than its boundary endpoints: any such vertex would have an edge to
`r` crossing the boundary. Any parallel edges in that region can be
collapsed successively across empty digons. No distinguished face `F_x`
of length at least three lies in such a region, since its boundary would
contain a third vertex of `B`. Thus the parallel edges can be removed while
preserving the distinguished polygonal faces, with their boundaries
identified in the natural way. There are no loops, since all neighbor
lists have distinct entries and the degree-one case adds nothing.

The resulting simple plane graph on `{r} union B` still has `r` adjacent
to every vertex of `B`. Deleting `r` therefore gives an outerplane graph
`H` on `B`: its incident faces merge into a face containing every vertex.
Every `F_x` is a bounded face of `H`, since the local region formerly
occupied by `x` did not contain `r`. Every original edge within `B` and
every fill edge for a degree-two vertex is an edge of `H`.

For `|B|>=3`, complete the outerplane graph to a maximal outerplanar graph
`K` on the same vertex set. This can be done by first adding edges in the
outer face to connect the graph and make its outer boundary a simple cycle,
preserving its existing bounded faces, and then triangulating each bounded
face. In particular, the triangles inside each `F_x` triangulate its own
neighbor polygon; their vertices are all actual neighbors of `x` in `G`.
All these added edges are only used to build a decomposition. They are not
inserted into the metric in which paths are required to be shortest.

## 2. The tree decomposition and its path covers

Use the triangles of `K` as bags and join two bags when their triangles
share an internal polygon diagonal. This weak dual is a tree, and these
bags form a tree decomposition of `K`. The triangles in each triangulated
face `F_x` induce a connected subtree of that tree.

Adjoin `r` to every bag. For each `x` of degree at least three, also adjoin
`x` to every triangle bag inside `F_x`. Distinct distinguished faces have
disjoint interiors, so at most one vertex of `X` is added to any triangle
bag. Every edge from `x` to its neighbor polygon is now covered, and the
bags containing `x` are connected.

For a degree-two vertex `x` with neighbors `a,b`, attach a new leaf bag
`{r,x,a,b}` to a triangle bag containing the fill edge `ab`. For a
degree-one vertex `x` adjacent to `a`, attach `{r,x,a}` to a triangle bag
containing `a`. These attachments preserve the connected occurrence set
of each old vertex. This proves all tree-decomposition axioms for the
original `G`: every vertex and edge is covered, and the bags containing
each vertex form a connected subtree.

Every bag has size at most four, except a triangle inside an `F_x`, whose
bag is precisely `{r,x,a,b,c}` with the properties in the displayed formula.
A bag of size at most four can be covered by at most two ambient geodesics
by pairing its vertices and joining paired endpoints by shortest paths;
a singleton is allowed. Additional vertices on these paths are harmless.
For a five-vertex bag, `r-a-x` has length two and is shortest because `r,x`
are not adjacent. The other two vertices are joined by `bc` if this edge
is present in `G`, and otherwise by `b-r-c`, also a shortest path. Their
union is exactly that bag.

If `|B|<=2`, no outerplanar completion is needed. Start with the bag
`{r} union B` and, for every `x` in `X`, attach the leaf bag
`{r,x} union N(x)`. These bags have size at most four and satisfy the same
axioms. This also handles the graph consisting of `r` alone.

## 3. Half balance, masses, and disconnected graphs

For completeness, any finite tree decomposition has a half-balanced bag
for arbitrary nonnegative vertex masses. Assign each graph vertex to one
bag containing it, and put its mass at that tree node. Choose a weighted
centroid of the tree. After deleting its bag, every remaining graph
component is represented entirely on one side of the centroid: the bags
containing a surviving vertex form a connected subtree avoiding the
centroid, and adjacent surviving vertices occur together in a bag. Its
mass is consequently at most the mass assigned to that side, which is at
most half the total. Zero total mass is immediate.

Cover the centroid bag by the two paths above. Deleting a superset of a
half-balanced separator can only shrink or split its remaining components.
This proves the theorem for connected graphs.

Under the stated hypothesis, every component not containing `r` consists
of an isolated vertex: all its vertices belong to the independent set `X`.
If some isolated vertex has more than half the total mass, delete it as a
singleton path. Otherwise apply the connected theorem to the component
of `r`. Its remaining components have mass at most half the mass of that
component, and hence at most half the original total; the other isolated
vertices were already small. This proves the full statement.

## 4. Scope and relation to prior cases

The treewidth upper bound is four, and it can be attained. The graph formed
by a cycle of length `m>=4` and two nonadjacent vertices joined to every
cycle vertex satisfies the hypothesis and has minimum degree four.
Treewidth is at least minimum degree (take an inclusion-minimal leaf bag
in a width-`k` decomposition to obtain a vertex of degree at most `k`).
Together with the constructed decomposition, this proves its treewidth
is exactly four. Thus the theorem is not only the known treewidth-at-most-
three bound. Some members, including these cycle examples, were already
covered by earlier positive families; no novelty is claimed for those
individual examples.

Even the bipartite radius-two corollary includes treewidth-four graphs:
subdivide each cycle edge of the preceding example once, leaving the spokes
unchanged. The two poles and subdivision vertices form one bipartition
class, and the old cycle vertices form the other. A pole still has
eccentricity two, and contracting the subdivided cycle edges recovers the
treewidth-four graph. The bags above still give the matching upper bound.

The known bounds from [Diot and Gavoille, *Path Separability of Graphs*
(2010)](https://emilie-diot.eu/Article/DG10a) include two paths for treewidth
at most three and for face-separable graphs. The team's
[universal-vertex lemma](../planar_geodesic_universal_vertex_treewidth/PROOF.md)
uses the same weighted-centroid argument with four-vertex bags. The present
extension uses the independent centers to control the five-vertex bags.
The automatic shortestness of induced three-vertex paths also underlies the
[order-12 packing proof](../planar_two_geodesic_packing/README.md).

This is a theorem for unit edge lengths and all vertex masses. Arbitrary
edge lengths can make `r-a-x` nonshortest, so no such metric extension is
asserted. It is a separator theorem for the whole graph under the given
hypothesis; no assertion about all induced subgraphs after removing `r`
is needed. [Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf)
remains open.

## 5. A companion case: an adjacent dominating pair

The same bag-cover principle also proves the following statement. If a
planar graph has an edge `uv` such that every other vertex is adjacent to
`u` or `v`, then two ambient geodesics half-balance every nonnegative
vertex mass assignment.

Contract `uv` to a universal vertex. The graph left after deleting that
vertex is exactly `G-{u,v}` and is outerplanar, so it has a tree
decomposition with bags of size at most three. Adjoin `u,v` to every bag.
Every resulting bag has at most five vertices. Its induced graph is
connected because `uv` is an edge and `u,v` dominate it. A five-vertex
bag cannot induce `K5` by planarity. Every connected noncomplete graph
contains an induced three-vertex path: take the first three vertices of
a shortest path between two nonadjacent vertices. That induced path is
an ambient geodesic of length two. A shortest path between the two
remaining bag vertices gives the second path. Smaller bags are handled
by pairing endpoints, and a weighted centroid completes the proof.

This short companion argument requires neither diameter two nor a
universal vertex. For a possible counterexample to Problem 31, these
results give two necessary conditions: every vertex has an edge among
its nonneighbors, and no edge has endpoints dominating the graph. In
particular its maximum degree is at most `n-3`. These restrictions can
be used with the earlier diameter filter. They do not exclude all
diameter-two planar graphs.

The bag argument does not extend automatically from independent `X` to a
matching. For example, take a five-cycle with a universal hub, and choose
`r` on the cycle. Its two nonneighbors form an edge. The six-vertex bag
consisting of the whole graph cannot be covered by two geodesics. Each
geodesic has at most three vertices, so a cover would require two disjoint
induced three-vertex paths. The one containing the hub uses two nonadjacent
cycle vertices; the other three cycle vertices induce an edge and an
isolated vertex, not a path. This only obstructs that bag-cover step: the
wheel itself has a half-separator and is already covered by the universal-
vertex case.

## 6. Reproducible checks

The universal theorem rests on the written proof, including the planar
completion in Section 1. The standard-library checker `verify.py` uses
explicit polygon dissections with independent face centers, leaves and
degree-two vertices, including deleted base edges and repeated two-neighbor
sets. Two further fixtures have a dominating edge but no universal vertex.
It builds decomposition certificates and checks their axioms, every
bag's path cover against original-graph distances, and half balance under
integer mass fixtures. These are exact regression checks, not a census of
all graphs satisfying the theorem and not independent peer review.

Run from the repository root with Python 3.11 or later:

```sh
python3 graph_theory/planar_two_geodesic_independent_non_neighbors/verify.py --check
```

Expected output and the number of checks are recorded in `expected.json`.
With Python 3.11.2 the result is `PASS`: 81 fixtures, 1,450 bag covers,
2,384 connected-graph mass assignments, four disconnected mass checks,
and five rejected invalid controls. Of the checked bags, the exact number
with five vertices is also recorded in the expected output.
The checker has no dependency on the exploratory planarity library, a
solver, a graph generator, or an omitted large artifact.
