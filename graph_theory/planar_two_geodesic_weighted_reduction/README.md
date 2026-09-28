# Weighted reductions for the two-geodesic half-separator problem

**Status:** proved reductions, not a solution of the separator problem. No
counterexample is supplied. No priority or paper-worthiness claim is made.

Let a geodesic mean a simple shortest path in the **original** graph, including
a path with one vertex. A half-separator is a vertex set whose deletion leaves
each component with at most half the total vertex mass. All graphs are finite
and simple; all paths in a separator are simultaneously geodesic before any
deletion.

## The reduction

The following assertions are equivalent.

1. Every unweighted planar graph has a half-separator that is the union of at
   most two geodesics, with vertices counted uniformly.
2. Every planar graph with nonnegative real vertex masses and nonnegative real
   edge lengths has such a half-separator, where balance is measured by vertex
   mass and shortestness by edge length.
3. Every planar triangulation with positive integer vertex masses and positive
   integer edge lengths, and with a unique geodesic between every two vertices,
   has such a half-separator.

Here a triangulation is a simple maximal planar graph on at least three
vertices. For graphs with zero-length edges we still require shortest paths to
be simple. The statement concerns existence of one separator; quantifying over
all planar graphs automatically includes all their induced subgraphs.

Consequently a weighted obstruction, including one found by choosing a generic
metric on a triangulation, really would refute the original unweighted question.
The reduction is constructive for integer data. Ordinary edge subdivision alone
does not justify this implication: a path can end inside a subdivided edge and
cut it without deleting either original endpoint.

## An explicit bound

More generally, fix an integer `k >= 1`. Suppose a planar graph `G`, with
nonnegative integer vertex masses `a(v)` of positive total `A` and integer edge
lengths `L(e) >= 2`, has no half-separator consisting of at most `k` geodesics.
Put

```
B = |V(G)| + (k + 1) * sum_e (L(e) - 1)
M = B + 1
N = B + M * A.
```

Replace each edge `uv` by `k+1` internally vertex-disjoint `u`--`v` paths, each
of `L(uv)` unit edges. Their internal vertices are new and are distinct for
different edges. Then attach `M*a(v)` new pendant vertices to each original
vertex `v`. The resulting unweighted simple planar graph has exactly `N`
vertices and has no half-separator consisting of at most `k` geodesics.

For Problem 31 use `k=2`, hence three replacement paths per edge. If the input
has positive integer lengths that include 1, first multiply every length by 2;
this leaves its geodesics unchanged.

## Proof of the explicit construction

### 1. Protecting edges during metric simulation

Let `J` be the graph after the parallel subdivisions and before adding leaves.
Its order is `B`. Give an original vertex `v` mass `a(v)` and each other vertex
mass zero. Distances in `J` between original vertices equal distances in the
edge-length graph `G`: a simple path between original vertices traverses entire
replacement paths, and conversely each path of `G` can be lifted to `J` with the
same length.

For any geodesic `Q` of `J`, list its original vertices in path order. This list
is either empty or the vertex list of a geodesic `P` in `G`. Indeed, trim `Q`
before its first and after its last original vertex. The trimmed subpath is
shortest; the distance identity just proved gives shortestness of its
projection. A list with one vertex is an allowed geodesic.

Take at most `k` geodesics `Q_i` in `J` and let `S` be the union of their
nonempty projections. For an edge `uv` of `G-S`, both `u` and `v` avoid every
`Q_i`. If a `Q_i` meets the interior of one of the replacement paths for `uv`,
it must lie entirely in that interior: the only exits are `u` and `v`. Thus
each `Q_i` can meet at most one of the `k+1` replacement paths for this edge.
At least one remains untouched. It follows that all original vertices in any
component `C` of `G-S` remain connected in `J - union_i V(Q_i)`.

Since `G` is an obstruction, some such `C` satisfies `2*a(C) > A`. Its original
vertices lie in one remaining component `D` of `J`. In particular the metric
simulation preserves the obstruction when subdivision vertices have mass zero.
This argument allows paths entirely inside one replacement path, paths with
one original vertex, repeated choices of paths, and fewer than `k` paths.

### 2. Removing zero vertex masses

On every vertex of `J` put the positive integer mass

```
b(x) = M*a(x) + 1,
```

where `a(x)=0` for new vertices. The total mass is `M*A+B`. For the component
`D` from Step 1, integrality gives `2*a(C) >= A+1`. Hence

```
2*b(D) >= 2*M*a(C) >= M*(A+1) > M*A+B,
```

because `M=B+1`. This proves that `J` with masses `b` is still an obstruction.
No limiting argument or assumption of a uniform positive gap is needed for
this integer construction.

### 3. Exact removal of positive integer vertex masses

We use the following elementary observation. Given any unweighted graph `F`
with positive integer vertex masses `b(x)`, form `F^b` by attaching `b(x)-1`
leaves at each `x`. The original vertex together with its leaves is its
**cluster**, of size `b(x)`. Then `F` has a mass-half-separator consisting of at
most `k` geodesics if and only if `F^b` has a uniform half-separator consisting
of at most `k` geodesics.

The empty graph is immediate. For the forward direction in a nonempty graph,
lift the geodesics unchanged to the core of `F^b`.
They remain shortest because pendant leaves cannot shorten a core path. Each
remaining component that contains a core vertex is exactly the union of the
clusters of a remaining core component. Other remaining components are single
leaves. These have size at most half the total whenever the total is at least
2. If the total is 1, there are no added leaves and the claim is immediate.

For the reverse direction, intersect each geodesic `Q` of `F^b` with the core.
A nonempty intersection is one geodesic of `F`. If the intersection is empty,
`Q` is a singleton leaf; project it to the singleton path at its parent.
Let `S` be the union of these at most `k` projected paths. For every core vertex
outside `S`, its entire cluster avoids all the `Q`: a leaf on a nonsingleton
path forces its parent onto that path, and a singleton leaf has had its parent
added to `S`. Thus every component `C` of `F-S` has all its clusters intact and
connected in `F^b - union V(Q)`. Their total size is exactly `b(C)`. Half-balance
of the latter graph therefore implies `2*b(C) <= sum_x b(x)`.

Apply this observation to `J,b`. Its only added leaves are `M*a(v)` leaves at
original vertices; subdivision vertices have mass 1 and receive none. This is
exactly the claimed graph of order `N`.

Finally, the construction preserves planarity: draw the parallel replacement
paths in a thin neighborhood of each embedded edge, and insert leaves locally
at their parents. It is simple because every replacement path has at least two
edges and uses distinct new internal vertices. This completes the proof.

## From real data to integer data

Suppose a weighted finite graph is an obstruction. There are finitely many
simple paths and finitely many families of at most `k` such paths.

First perturb the edge lengths to positive rational numbers so slightly that
no formerly nonshortest simple path becomes shortest. To see this, for each
formerly nonshortest path compare its length with one fixed shortest path with
the same endpoints. Each comparison has a strict positive gap, and there are
only finitely many comparisons; all these inequalities persist in a sufficiently
small neighborhood. When no such comparisons exist the condition is vacuous.
Positive rational vectors are available arbitrarily close even to vectors with
zero coordinates. We may additionally avoid the finitely many proper
hyperplanes on which two distinct simple paths with the same endpoints have
equal length. The new metric therefore has unique geodesics, all of which were
geodesics in the original metric.

For every family of at most `k` original geodesics, select one component whose
mass is strictly greater than half the total. These finitely many strict linear
inequalities in the vertex masses persist under a sufficiently small positive
rational perturbation. They in particular persist for the smaller family of
geodesics of the perturbed metric. Thus an obstruction with positive rational
lengths, unique geodesics, and positive rational masses results. Clear the two
sets of denominators independently, and double the resulting integer lengths
if necessary. The explicit construction now supplies an unweighted obstruction.

This is a finiteness argument for existence, not a claimed efficient procedure
for finding rational data from arbitrary noncomputable real input.

## Reduction to triangulations

A disconnected obstruction has a component with more than half its total mass.
That component must itself be an obstruction: a separator balancing it relative
to its own mass would balance the entire graph. Hence restrict to a connected
obstruction, and apply the preceding rational perturbation.

Extend its planar embedding to a maximal simple planar graph on the same
vertices. Give every added edge a positive integer length greater than the sum
of all the old edge lengths. No shortest path uses any added edge, since the
old graph is connected and already contains a shorter path between every pair
of vertices. Geodesics, and their uniqueness, are unchanged. Adding edges can
only merge components after deleting a given path union, so failure of
half-balance persists. Connected graphs on at most two vertices cannot be
obstructions, and thus there is no small-order exception to address here.

Assertion 2 implies assertions 1 and 3 immediately. The explicit construction
and rational perturbation show that a failure of assertion 2 implies a failure
of assertion 1. The preceding augmentation shows that a failure of assertion 2
implies a failure of assertion 3. This proves all the equivalences.

## Literature and scope

- [Codsi, Problem 31 in the Barbados 2026 list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf)
  asks the uniform unweighted two-path half-balance question. Two-path
  two-thirds balance does not answer it.
- [Diot and Gavoille, On the Path Separability of Planar Graphs (2009)](https://dept-info.labri.fr/~gavoille/article/DG09a)
  formulate the older weighted two-path question and establish the face-separable
  case.
- [Diot and Gavoille, Path Separability of Graphs, full version (2010)](https://emilie-diot.eu/Article/DG10a)
  define **strong** path separability by ambient geodesics and distinguish it
  from sequential path separability. Proposition 1 already covers treewidth at
  most three and gives three paths for planar graphs. Proposition 5 reduces the
  all-weight strong property to blocks, and Theorem 2 makes that property
  minor-closed. Those results are prior work, not claims of this note.

The reduction isolates a safe way to transfer metrics and masses into the exact
unweighted problem. It establishes no new two-path positive graph class, no
counterexample, and no improved balance constant. A targeted search of these
primary sources and the associated literature did not locate this precise
parallel-subdivision transfer, but that is not a claim of originality.

## Reproducible finite checks

The proof above is the evidence for the universal statements. `verify.py` is a
small exact regression check of its two transfer mechanisms, not a proof by
enumeration and not a search for a planar counterexample.

Run with Python 3.11 or later, standard library only:

```sh
python3 graph_theory/planar_two_geodesic_weighted_reduction/verify.py
```

The program checks all geodesics and all 361,285 pairs in its stated small metric
fixtures, checking projections and survival of each undeleted core component.
It also checks the exact pendant-leaf equivalence on small fixtures and a
one-path obstruction lift. A deliberately insufficient single-subdivision
example must be rejected. The one-path lift uses the nonplanar graph `K5` as a
negative control, not as evidence against the planar question: all 24,670 path
masks in its 155-vertex lift leave a component of at least 97 vertices.
Expected compact results are in `expected.json`. Tested with Python 3.11.2.
No external enumeration, floating point, randomized choices, solver, or
planarity library is trusted. Planarity of the general construction follows
from the embedding argument, not from the program.

The source has not been proof-assistant formalized. Independent review is
separate from these author-run checks.
