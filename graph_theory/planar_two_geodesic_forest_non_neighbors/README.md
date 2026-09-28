# Two geodesics when the nonneighbors induce a forest

**Theorem.** Let `G` be a finite simple planar graph with unit edge lengths.
Suppose some vertex `r` satisfies

```
G[V(G) - N[r]] is a forest.
```

For every assignment of nonnegative real vertex masses, there are at most
two paths, both shortest in the **original** graph, whose union is a
half-balanced separator. Singleton paths are allowed. The proof gives a
tree decomposition of width at most four in which every bag is contained
in the union of two ambient geodesics.

The outside forest may have arbitrarily large components, arbitrary
branching, and vertices arbitrarily far from `r`. The paths can be long;
there is no assertion that two paths of at most two edges suffice.
The theorem is proved structurally below. The exact checker supplies
regression evidence, not a finite premise for the all-order statement.

Combining the local construction with the independently reviewed
[clique-patch theorem](../planar_two_geodesic_cluster_non_neighbors/README.md)
gives the following extension:

**Corollary.** The same half-balance conclusion holds if every component
of `G-N[r]` is either a tree or a clique. Here the decomposition has width
at most five, and the clique part retains the finite-certificate dependency
of that earlier theorem.

Thus a counterexample to [Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf)
must, for every vertex `r`, have a component of its nonneighbors that
contains a cycle and is not a clique. In particular its maximum degree is
at most `n-5`: every connected graph on at most three vertices is a tree
or a clique. The unrestricted planar question remains open.

## 1. Why treewidth does not finish the argument

Chaplick, Da Lozzo, Di Giacomo, Liotta, and Montecchiani prove that a
cycle-tree has treewidth at most three in the proof of Theorem 2.2 of
[*Planar Drawings with Few Slopes of Halin Graphs and Nested Pseudotrees*,
Algorithmica 86 (2024)](https://doi.org/10.1007/s00453-024-01230-7).
Adding `r` suggests five-vertex bags. This does not by itself give two
shortest paths. A five-element set can contain no three vertices on one
geodesic, even in a small planar graph. For example, take a `K4` on
`r,w,z,a` and attach the triangle `a,u,v`. No geodesic contains three of
`{r,w,z,u,v}`. This obstructs that particular bag cover, not half balance
for the graph.

The needed additional fact is the shape of the bags and their relation
to the original tree cuts. Each five-vertex bag below is one of

```
{r,x,a,t,b}          (one tree vertex and three boundary vertices),
{r,u,v,w,z}          (an original tree edge uv and two cut endpoints).
```

A missing boundary edge gives an induced three-vertex path through `r`.
When that edge is present, a small separating set forces a shortest path
to `r` to contain three bag vertices. Pairing the remaining two vertices
then gives the second geodesic. No added edge is used as a metric edge.

## 2. From outside components to polygonal patches

Assume first that `G` is connected. Put `B=N(r)`, and let `C` be one tree
component of `G-N[r]`. Write `Y=N(C)`, so `Y` is a nonempty subset of `B`.
All edges from `C` to the rest of the graph end in `Y`.

We use the following elementary planar patch construction, also used in
the [independent-nonneighbor proof](../planar_two_geodesic_independent_non_neighbors/README.md).
Contract every connected outside component to a center. The centers are
independent. Replace a center with at least three distinct neighbors by
the polygon through its neighbors in their cyclic order. A center with
two distinct neighbors gives a fill edge, and one with one neighbor gives
a vertex attachment. Keep `r` and all its incident edges throughout.

There may initially be parallel spokes or parallel replacement edges.
A region away from `r` between parallel `ab` edges contains no third
vertex of `B`: its edge to `r` would have to cross the boundary. A region
between parallel spokes to a single boundary vertex `a` likewise contains
no other vertex of `B`. Any other outside component trapped there has
neighbor set contained in `{a}` and can be treated as a separate vertex
attachment. Suppressing these parallel regions therefore does not lose
a patch having three distinct neighbors. Parallel polygon edges can be
identified across the empty regions. This is an operation on an auxiliary
embedding, not a change to the original metric.

After suppression, deleting `r` from the auxiliary graph gives an
outerplane graph on `B`. For `|Y|>=3`, the component `C` occupies a
polygonal patch with distinct boundary vertices `Y`. Patches have disjoint
interiors. In particular, **an original edge between two vertices of `Y`
is a boundary edge of this polygon**: it cannot be a chord, since `C` is
connected and has a neighbor at every vertex of `Y`. Equivalently, such
a chord would split the distinguished face after contraction.

Complete the outerplane graph to a polygon dissection, triangulating the
ordinary faces but leaving these patches untriangulated. Its face weak
dual is a tree. A local decomposition of a patch can replace its face
node provided that each boundary edge `ab` has a bag containing
`{r,a,b}`. The local construction below provides exactly these interfaces.
The cases `|B|<=2` use the same vertex and edge interfaces directly and
need no outer polygon.

## 3. The port-order lemma for a tree

For clarity, the relevant topological fact is stated separately.

**Port-order lemma.** Let a plane tree `C` lie in a disk with its spokes
ending at boundary vertices `Y`. Thicken `C` to a small closed disk. Its
boundary traverses every tree edge twice. The spoke sources along this
boundary form the corresponding cyclic corner word; a vertex can occur
several times. Destination ports on the outer boundary follow the same
cyclic order. All ports with a given destination form a cyclic interval.

For an edge `uv` of `C`, the source ports belonging to the two components
of `C-uv` form complementary intervals. Their boundary neighbors lie on
complementary boundary arcs, with possible common endpoints `w,z`.
The two endpoints may coincide, a side can have no spokes, and one side
can contain all destination vertices.

**Proof.** A regular neighborhood of a tree is a disk. Removing the band
around `uv` splits that disk into the regular neighborhoods of the two
trees. Thus the exposed source ports of either tree are consecutive on
the original boundary. The spokes run through an annulus between the
inner disk and the outer boundary without crossing. Cutting the annulus
along a spoke reduces the order assertion to that for disjoint arcs in
a rectangle. Near an outer vertex, replace its incident spoke endpoints
by consecutive nearby ports. Hence destinations at that vertex are
consecutive cyclically. Projecting either source interval onto these
ordered destination groups proves the arc assertion. Empty source blocks
and coincident end groups give precisely the stated degeneracies. `□`

The same statement applies after contracting tree edges: each surviving
inner vertex represents a connected subtree, and its ports are the
original ports of that subtree. A leaf of the contracted tree represents
one whole side of an original tree-edge cut. Its ports consequently form
one interval.

Retain the original cyclic port word as bookkeeping even after deleting
boundary vertices. There is a useful endpoint-persistence observation. If a contracted leaf
interval has endpoints `w,z`, delete only destination vertices **strictly
inside** that interval. No endpoint of a later leaf interval is deleted.
Indeed the already contracted subtrees belonging to a later leaf subtree
are contained in it; all others are disjoint from it. Their source
intervals are accordingly nested or disjoint. A strict interior
destination of a nested interval cannot become an extreme destination of
the larger interval. The geometric cut positions are the two sides of
original tree edges, which have not been contracted at the later cut.
If the complementary subtree has no ports, keep the same cyclic cut when
extending the interval. If first and last destination coincide, retain
that one vertex. These conventions include an interval traversing the
whole boundary.

Consequently the retained endpoints of a current leaf still bound the
neighbor arcs of the two sides of its **original** tree-edge cut, even
when other boundary vertices have already been eliminated.

## 4. A leaf elimination with five-vertex bags

Inside one patch, form an auxiliary graph `F` by adding its complete
boundary cycle and every edge from `r` to `C`. These edges are fill edges
only. The actual graph is still the original induced graph on
`{r} union C union Y`.

Maintain the following invariant during elimination:

* The surviving inner vertices form a tree whose edges are original
  edges between surviving vertices.
* Each inner vertex represents the connected original subtree contracted
  into it. Its current spokes are the original spokes of that subtree to
  the surviving boundary vertices.
* The surviving boundary has its cyclic order and all cycle edges; `r`
  is adjacent to every surviving vertex in the auxiliary graph.

Choose an inner leaf `u`, with inner neighbor `v` if there is one. Take
the endpoints `w,z` of its port interval, keeping only one endpoint if
they coincide. Every boundary vertex strictly inside this interval has
`u` as its only surviving inner neighbor, by the port-order lemma.
Eliminate these interior boundary vertices in order. If `t` is one of
them and `a,b` are its neighboring surviving boundary vertices, its bag
is contained in

```
{r,u,a,t,b}.                                      (A)
```

Completing the remaining neighborhood of `t` to a clique adds only a
boundary edge and already permitted root or spoke edges. Retain the
interval endpoints. Now the bag for eliminating `u` is contained in

```
{r,u,v,w,z}.                                      (B)
```

The fill edges from `v` to `w,z` are exactly the spokes inherited by
contracting `u` into `v`; the edge `wz` becomes a boundary edge. No new
edge between surviving inner vertices is created. This proves the
invariant for the smaller tree. If `u` has no spokes, or only one
destination, the corresponding bag has at most four vertices. The last
inner vertex is treated by the same fan elimination and a final bag of
size at most four. Eliminate the remaining boundary and `r` last.

The bags from this elimination form a tree decomposition of `F` with
bags of size at most five. One explicit parent rule is to attach the bag
for a vertex to the bag for its first later neighbor in the elimination
order. The later neighbors form a clique, so they are all in that parent
bag. This proves edge coverage and connected occurrence sets by
induction. Since `{r,a,b}` is a clique of `F` for every original polygon
boundary edge `ab`, it occurs together in some bag. These are the required
patch interfaces.

The same construction works for one or two boundary vertices, with a
single boundary vertex or edge instead of a cycle. Alternatively, add
`{r} union Y` to every edge bag of the inner tree. This gives bags of at
most five; the two-boundary case has the path cover justified below by
the fact that all paths from `C` to `r` meet `Y`.

## 5. Covering the bags in the ambient metric

All paths in this section are chosen in `G`, including when their
vertices lie outside the bag or the current reduced patch. Such extra
vertices are harmless when the path union is deleted.

A bag of at most four vertices is covered by pairing its vertices and
joining each pair by an ambient shortest path. Consider a bag of size
five.

**Type A.** Write the bag as `{r,x,a,t,b}`. If the three boundary vertices
are not a clique in the original graph, choose two nonadjacent ones.
Together with `r` they form a shortest two-edge path. Join the remaining
boundary vertex to `x` by an ambient shortest path.

Otherwise `a,t,b` form an actual triangle. The no-chord property of the
**original** neighbor polygon forces `Y={a,t,b}`. Every path from `x` to
`r` meets `Y`, so an ambient shortest `x-r` path contains at least three
bag vertices. Join any two remaining bag vertices by a shortest path,
using a singleton if only one remains. This also handles an inactive
inner vertex whose distance to `r` is large.

**Type B.** Write the bag as `{r,u,v,w,z}` with five distinct vertices.
The edge `uv` is an original tree edge. If `wz` is absent from `G`, use
`w-r-z` and the edge `uv`.

If `wz` is present, it is an edge of the **original** neighbor polygon.
The vertices `w,z` are therefore consecutive there. One of the two open
boundary arcs between them contains no original boundary vertex. By
endpoint persistence and the port-order lemma, the corresponding
component of `C-uv` has all its neighbors in `B` contained in `{w,z}`.
Let `x` be its endpoint of `uv`, and `y` the other endpoint. Then

```
{y,w,z} separates x from r in the original graph.
```

An ambient shortest `x-r` path must contain one of `y,w,z`, and hence at
least three bag vertices. Pair the at most two remaining bag vertices.
The same argument covers the case where that side of `C-uv` has no
boundary neighbor. No assumption that a fill spoke is a genuine edge,
or that a reduced-graph geodesic remains shortest, has been made.

For a patch with exactly two neighbors `Y={w,z}`, any bag of size five
has the form `{r,w,z,u,v}`. A shortest path from `u` to `r` must meet
`Y`, so it already covers three bag vertices; pair the rest. A patch
with one neighbor has bags of size at most four.

This proves the required two-geodesic cover of every local bag.

## 6. Gluing, half balance, and the mixed corollary

Give each ordinary triangular face of the outerplane dissection the bag
`{r,a,b,c}`. Replace each tree-patch face by the local decomposition above.
Connect neighboring local trees at bags containing their shared
`{r,a,b}` interface. Single- and two-neighbor patches attach at the
corresponding vertex or edge interface. The face weak dual is a tree,
so these connections make one decomposition tree. Occurrences of a
boundary vertex stay connected across exactly the incident interfaces;
inner vertices occur only in their own local tree. This establishes all
tree-decomposition axioms for `G`.

For any nonnegative vertex masses, assign each vertex's mass to one bag
containing it. Choose a weighted centroid of the decomposition tree.
Every component remaining after deletion of its bag is represented
entirely on one side of the centroid, and therefore has at most half the
total mass. Cover that bag by its two ambient geodesics. Deleting their
union can only shrink or split the remaining components. Zero total mass
is immediate. This is the usual weighted-centroid argument, also used by
[Diot and Gavoille, *Path Separability of Graphs* (2010)](https://emilie-diot.eu/Article/DG10a).

If `G` is disconnected, every component not containing `r` is a tree.
If one has more than half the total mass, a weighted vertex centroid of
that tree is a one-path separator for the whole graph. Otherwise apply
the connected theorem to the component containing `r`; the other
components are already small.

For the mixed corollary, use the reviewed clique-patch decomposition on
each clique component and the present decomposition on each tree
component. They have exactly the same boundary interfaces, so the same
gluing works. Inactive clique vertices are restored in their clique
bags as in the earlier proof. Outside the component of `r`, a heavy
clique has at most four vertices by planarity and can be covered entirely
by two edges or singletons; a heavy tree is handled by its centroid.
This proves the stated corollary, with its explicit dependency on the
751-case clique certificate.

## 7. Strict extension and scope

For an explicit new member beyond the earlier clique-nonneighbor and
adjacent-dominating-pair conditions, take the inner path `1-2-3`, the
cyclic source word `(1,2,3,2)`, and three private consecutive boundary
neighbors per source occurrence. Include the twelve-cycle on the
boundary, all its edges to `r`, and the twelve spokes. This gives a
16-vertex planar graph. Its nonneighbors at `r` induce that path. The
checker confirms that no vertex has clique-component nonneighbors and
no edge is dominating. The minimum degree is four, while the present
decomposition has width four, so its treewidth is exactly four.

The same construction with arbitrarily long inner trees gives an
unbounded family in the theorem. The cycle-tree treewidth bound itself
is prior art; the contribution here is the ambient-geodesic cover of
the root-augmented bags, including their virtual spokes and inactive
inner vertices. Targeted primary-source searches did not locate the
exact separator statement. No literature-priority claim is made.

The proof uses unit lengths when two nonadjacent boundary vertices are
joined through `r`. It makes no claim for arbitrary edge lengths.
Neither this theorem nor its mixed corollary resolves a cyclic nonclique
component outside every closed neighborhood. In particular the
13-vertex triangulation `L|fIID@SJ_aEFx` from the team's finite work has
no root satisfying the mixed condition. Its known positive finite
result is not used in this proof.

## 8. Reproducible evidence and trust boundary

Run from the repository root with Python 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_forest_non_neighbors/verify.py --check
```

The standard-library checker constructs planar fixtures from tree corner
words and cyclic destination intervals. It checks the explicit leaf
elimination and both ambient path-cover cases, including the original
cut condition when a boundary edge is present. A separate elimination-
prefix reachability computation validates each bag; it also checks all
decomposition axioms, boundary interfaces, path adjacency, exact ambient
distances, and selected mass assignments. It includes a glued-patch
fixture and rejected malformed inputs and corrupted witnesses.

The fixture family includes 7,237 three-vertex-path endpoint cores from
the three source patterns listed in the checker, 252 expanded path/star/binary-tree fixtures, and 600 seeded larger port
fixtures. The written proof, including the planar patch and nested-port
arguments, establishes the unbounded theorem. These finite tests do not
exhaust all plane trees or formalize the topology. The new theorem does
not depend on a solver, external graph enumeration, or the exploratory
search programs. Independent review is pending at publication.

Exact expected counts are in [expected.json](expected.json); the
[checker source](verify.py) is the complete reproducible artifact.
