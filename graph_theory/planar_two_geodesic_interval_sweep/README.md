# Two-geodesic half balance from a planar interval sweep

All graphs are finite, connected, simple, undirected, and planar. Edge
lengths are strictly positive real numbers; vertex masses are arbitrary
nonnegative real numbers. Distances and geodesics always refer to the
original edge metric. Deleting a path means deleting its vertices.

This note supplies a mass-dependent proof route for [Barbados 2026
Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
The metric and support hypotheses below are essential restrictions; no
general planar half-separator theorem is asserted.

## Interval theorem

For vertices s,t, write

    I(s,t) = {v : d(s,v) + d(v,t) = d(s,t)}.

**Theorem 1.** Suppose every positive-mass vertex belongs to I(s,t). For
every prescribed s-t geodesic P there is an s-t geodesic Q such that every
component of G minus (P union Q) has mass at most half the total mass.
In fact, the upper bound can be half the mass outside P. The two paths
may coincide and may have common subpaths.

The case s=t is immediate: all mass is at s. Below assume s is distinct
from t. Neither uniqueness of shortest paths nor a particular embedding
of s and t is required. Vertices outside I(s,t), and all their incident
edges, remain in G; their masses must be zero.

### A plane directed-path sweep

We use the following elementary plane-st sweep fact. Let D be an acyclic
plane digraph with a single source s and a single sink t, both on the
outer face. Suppose its outer boundary consists of a left and a right
directed s-t path. There is a sequence Q_0,...,Q_m of directed s-t paths
from the left boundary to the right boundary, each obtained from the
previous one by moving across one bounded face. If L_i is the set of
vertices strictly on the left of Q_i, then

    L_i is a subset of L_(i+1),
    L_(i+1) minus L_i is a subset of V(Q_i).

Regions containing additional zero-mass vertices and edges may be drawn
inside the faces of D without changing the corresponding mass inequality.

Here is the usual combinatorial explanation of the sweep. In a plane
st-digraph the incoming edges at each vertex are consecutive, as are the
outgoing edges; every bounded face has two directed boundary paths with
the same ends. Split the outer dual vertex into its left and right sides,
and orient each dual edge from the left of its primal directed edge to
its right. This split dual is acyclic. A directed dual cycle would enclose
a region whose crossing primal edges all point the same way. The region
would then contain a source or sink of the primal DAG, impossible because
s and t lie on the outer face. The consecutive-edge and two-boundary-path
properties are the standard plane-st properties, obtained by the same
Jordan-curve argument. They ensure that processing the bounded faces in
a topological order of the split dual replaces the entire left boundary
of the next face in the current frontier by its right boundary. The
frontier stays a directed s-t path. A vertex newly left behind was on
the old frontier; the open face has no vertices of D. This proves the
displayed properties. Parallel boundary edges, including an outer digon,
cause no change in this argument.

This is standard planar path-order machinery, not a new path-lattice
claim; see [Matuschke and Peis, *Lattices and maximum flow algorithms in
planar graphs*, Section 2](https://arxiv.org/pdf/1211.2189) for the
left/right order in the st-planar setting. We spelled out the particular
face sweep used here to make its weight transfer explicit.

**Sweep balance lemma.** Give the vertices nonnegative masses of total M,
allowing zero-mass material inside the faces. Some Q_i leaves mass at most
M/2 on each side.

Indeed, the initial left side and final right side are empty. If the
final left side has mass at most M/2, the final path works. Otherwise
take the first step with w(L_(i+1)) > M/2. Its predecessor has
w(L_i) <= M/2. If its right side also had mass greater than M/2, then

    w(L_(i+1)) <= w(L_i) + w(Q_i)
               = M - w(R_i) < M/2,

a contradiction. Thus Q_i works. Removing the path separates the two
sides even when the extra zero-mass vertices and edges inside the faces
are retained. This is exact half balance; there is no face-weight error
or 2/3 relaxation.

### Proof of Theorem 1

Let H be the union of all s-t geodesics. Orient its edges in increasing
order of d(s,v). Positive lengths make H a DAG. Every vertex and edge of
H lies on an oriented s-t path; every such path has length d(s,t) by
telescoping distance increments. Its vertex set is I(s,t).

Embed G on the sphere and cut it open along the prescribed path P. Each
internal vertex and edge of P has a left and a right copy; s and t remain
the common endpoints. The result is a disk with two copies of P on its
boundary. In the lifted H, every vertex is on a directed s-t path. For a
vertex off P, take an original geodesic through it and the segment between
the last preceding and first following intersection with P. Its interior
avoids P. Join this lifted segment to the appropriate boundary copies of
P before and after it. The resulting path is directed. Boundary-copy
vertices are already on one of the two boundary paths.

Thus the lifted H is a plane st-digraph, with the two copies of P as its
outer boundary. In particular its source and sink are unique; no hidden
source is created by cutting at a repeated contact with P. Its underlying
graph is biconnected: an interior component cut off at one vertex could
not contain a vertex of a simple directed s-t path, while the two outer
boundary paths form a cycle. The outer-digon case is allowed.

Set the masses of both copies of P to zero and leave all other masses
unchanged. Every original vertex outside H has mass zero and sits in a
face of H. Apply the sweep balance lemma to the lifted H with this
zero-mass material retained. Its total mass is M=w(V(G) minus V(P)).
We obtain a directed path Q' leaving at most M/2 on either side.

Project Q' back to G. Distance from s strictly increases along every
edge, so Q' cannot visit both copies of the same original vertex. Its
projection Q is a simple s-t path of length d(s,t), hence an ambient
geodesic. Every component of G minus (P union Q) lies on one side of the
cut-open path Q': it cannot cross either deleted path. Each component
therefore has mass at most M/2, which is at most w(G)/2. This proves the
theorem. Notice that shortestness is checked in G, not after deleting P.

## A facial terminal criterion

Fix a vertex r and one face F of a plane embedding. Let V(F) be the set
of vertices incident to that face, allowing repeated vertices in its
boundary walk. Define the set of vertices on shortest paths from r to F:

    J(r,F) = union over z in V(F) of I(r,z).

**Theorem 2.** If every positive-mass vertex belongs to J(r,F), two ambient
geodesics from r to vertices of F half-balance G. Any one r-to-F geodesic
may be prescribed as the first path. Again the residual bound can be
half the mass outside that first path.

Choose a real number A larger than max_v d(r,v). Put a new zero-mass
vertex t inside F and join it to every z in V(F), with edge length
A-d(r,z)>0. This is a planar augmentation; repeated facial occurrences
can first be joined by parallel edges and redundant copies removed.

The potential phi(v)=d(r,v), phi(t)=A is 1-Lipschitz on every edge with
respect to its length. Consequently d(r,t)>=A, while every shortest
r-z path followed by zt attains A. Every r-to-F geodesic extends to an
r-t geodesic. Conversely, an r-t geodesic uses exactly one new edge, its
last edge zt. Its prefix is an original r-z geodesic, since its length is
d(r,z). The same potential shows that original distances from r have
not decreased. Each vertex of J(r,F) belongs to the augmented I(r,t).

Extend the prescribed first path by its final new edge, apply Theorem 1,
and remove the final new edge from each of the two resulting paths.
Their prefixes are geodesics in the original G. Deleting them from G
leaves the same original components as deleting both augmented paths,
including t, from the augmentation. This proves Theorem 2.

If r belongs to F and the prescribed path is the singleton r, this gives
one r-to-F geodesic as a half separator under the same support condition.

### Application to a cyclic patch

Suppose the vertices of a unit plane graph are r, a set B, and the
vertices of a facial chordless cycle C; r is adjacent to all of B and to
none of C, and every vertex of B has a neighbor on C. Then J(r,C) is
the whole graph: a spoke r-b-c has length two and is shortest, and each
vertex of C is itself a permitted terminal. Theorem 2 gives two rooted
geodesics that half-balance every vertex-mass assignment.

The same argument permits arbitrary positive lengths on edges within B
and on C when all r-B and B-C edges have length one. Ring sizes, numbers
of spokes, and gaps of inactive vertices on C need not be uniform.
Noncrossing spoke arrangements may have vertices incident to many spokes.
This supplies a direct separator proof after the invariant of retaining
r in every decomposition bag failed in the
[annulus obstruction](../planar_two_geodesic_rooted_decomposition_barrier/README.md).
The regular column-median cases were already covered by the
[capped-mesh result](../planar_geodesic_mesh_obstructions/PROOF.md).

This patch statement does not handle arbitrary extra branches attached
outside the patch, arbitrary unicyclic nonneighbors, or arbitrary metrics
on a graph that merely satisfies the unit hypothesis. Such extensions
require additional arguments. In general the metric support condition
must be checked rather than inferred from planarity.

## Why this goes beyond two-geodesic bag decompositions

The unit icosahedron has I(s,t)=V(G) for antipodal vertices s,t, so
Theorem 1 gives half separators for all vertex masses. Nevertheless it
has **no tree decomposition whose every bag is covered by two ambient
geodesics**, even with no distinguished root and no width restriction.

Every closed vertex neighborhood in the icosahedron induces the
six-vertex wheel. This diameter-two set cannot be partitioned into two
induced three-vertex paths: the path through the hub leaves an edge and
an isolated rim vertex. Any ambient geodesic meets the set in at most
three vertices, and three such vertices must form a consecutive induced
path. Therefore no closed neighborhood is covered by two ambient
geodesics. After contained leaf bags are pruned, an exclusive vertex of
a leaf bag has its full closed neighborhood in that bag. This contradicts
a two-geodesic cover; a single bag containing all vertices fails as well.
The same leaf-bag argument was used in the earlier rooted obstruction.

This explains why the proof here chooses its second path after the
masses are known. The checker also confirms that one geodesic cannot
half-balance the uniformly weighted icosahedron, so the number two is
necessary within the interval class.

## Prior work, scope, and reproduction

[Diot and Gavoille, *Path Separability of Graphs*, 2010, Theorem 1](https://emilie-diot.eu/Article/DG10a)
give two ambient paths when a facial boundary is already a half separator.
The hypotheses here concern metric intervals and mass support instead.
For example, the uniformly weighted icosahedron has only triangular
faces and no facial half separator; it satisfies the interval hypothesis.
The planar st-path order underlying our proof is standard. A targeted
primary-source search did not locate the exact prescribed-first-path
support formulation; this is not a priority claim.

The written sweep and augmentation proofs establish the all-order
statements. The finite standard-library checker is regression evidence
and includes independently recomputed distances, all prescribed-path
choices, full residual components (including zero-mass vertices outside
the interval), and hypothesis controls. No graph census or solver is a
proof premise. The proof's topological trust boundary is the stated plane
st sweep and cut-open construction; no formal proof is claimed.

Run from the repository root with Python 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_interval_sweep/verify.py --check
```

The exact output is recorded in `expected.json`. See the checker for the
deterministic fixture definitions and mass seeds. It checks 18 interval
fixtures and 28 facial fixtures, 785 original geodesics, 28 artificial-sink
augmentations, 9,567 path pairs, and 217,722 prescribed-path/mass cases
across 21,548 mass assignments. Eight zero-mass vertices outside the
relevant support sets are retained in the component calculations. All
binary mass assignments are included for the specified small fixtures;
the remaining assignments are deterministic integer and rational tests.

The controls check all 162 geodesics of the unit icosahedron for failure
of one-path half balance, its 12 obstructed closed neighborhoods, and
failure of all 666 prescribed-terminal path pairs in the NONPLANAR capped
K_(6,6). Giving a vertex outside the interval all the mass also makes
every restricted pair fail, illustrating the support hypothesis. None of
these finite observations is a counterexample to Problem 31. The general
question remains open.
