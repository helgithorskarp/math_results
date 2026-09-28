# Rerooting a geodesic core with two attachment-boundary covers

All graphs are finite, simple, connected, undirected, and planar. Edge
lengths are positive and vertex masses are nonnegative. Every shortest
path below is measured in the original graph. The result gives an
all-order gluing class for exact half balance, including two disjoint
attachment boundaries. It does not settle unrestricted
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Transfer from a subset of the geodesic union

Write I(s,t) for the union of all s-t geodesics, and J(a,F) for the union
of all a-to-F geodesics, with F the boundary of a face. The
[reviewed interval/facial sweep](../planar_two_geodesic_interval_sweep/README.md)
says that masses supported on either union can be half-balanced by a
prescribed corresponding geodesic P and a second such geodesic Q.

**Lemma.** Let S be any vertex subset of I(s,t), or of J(a,F), and let
P be a prescribed geodesic of the corresponding terminal type. For
every positive-mass component K of G-(S union V(P)), suppose

* w(K)<=W/2, where W=w(G); and
* K has at most one neighbor in S-V(P).

Then P can be completed to an exact half separator by a second ambient
geodesic Q of that terminal type. Neither P nor Q is required to stay
in S. Zero-mass components may have arbitrary boundaries.

More precisely, let D be the mass of components K having no surviving
S-neighbor, and let B=max_K w(K), with maximum zero for an empty family.
Every residual component can be made to have mass at most

    max((W-w(P)-D)/2, B).

**Proof.** Zero the masses on P and keep those on S-P. Transfer the
whole mass of each positive K with a surviving neighbor to that unique
neighbor; discard the masses of components with none. Set all remaining
outside masses to zero. The proxy mass w' is supported on S, vanishes
on P, and has total M=W-w(P)-D. The existing sweep, applied in the
unchanged graph, supplies Q with residual proxy masses at most M/2.

Let R be a residual component meeting S. If a positive K meets R, a
path inside R from K to S must use K's unique surviving S-neighbor x.
Thus x belongs to R. The surviving part of K in R weighs at most its
whole mass, all of which was moved to x. Hence w(R)<=w'(R)<=M/2.
This remains true if Q splits K or removes x: in the latter case no
piece of K can meet a residual component containing S. A residual
component disjoint from S is contained in one K and has mass at most B.
Zero-mass outside components remain in the graph throughout, so any
connections they make are already included in the proxy component
test. This proves the bound and the lemma.

This extends the earlier
[exact-union transfer](../planar_two_geodesic_light_attachment_transfer/README.md),
whose second path could not enter an outside component. Moving mass to
a cut vertex is standard, for example
[Diot--Gavoille, Proposition 5](https://emilie-diot.eu/Article/DG10a).
The change here separates the chosen support core from the larger
metric union; it is not a new path-order theorem.

## An annular core with local attachments

For k>=5, form H from vertices r, a_0,...,a_(k-1), and
c_0,...,c_(k-1), with subscripts modulo k. The edges are

    r a_i,  a_i a_(i+1),  a_i c_i,  a_i c_(i+1),  c_i c_(i+1).

The first four types have a common length lambda>0. Each inner-rim
edge c_i c_(i+1) may have length at least lambda, or may instead be a
path with new internal vertices and positive edge lengths of total at
least lambda. Let C be the resulting inner cycle, including subdivision
vertices, and use the standard annular embedding with C facial.

Extend H to a plane graph G, keeping C facial. Its components K outside
H have boundary T(K)=N(K) intersect V(H) contained in either

    {r},  {r,a_i},  or {r,a_i,a_(i+1)}.

These containing sets are cliques of H. Assume H is **isometric** in G:
distances between all H-vertices are unchanged. A useful sufficient
condition is that every new edge have length at least lambda/2.
Indeed, an excursion through an attachment between distinct boundary
vertices uses at least two new edges, costs at least lambda, and can
be replaced by their existing length-lambda clique edge. Excursions
returning to the same vertex can be removed.

Let E be the set of cycle edges a_i a_(i+1) that occur as the two active
boundary vertices of some positive-mass K. Repeated components with
the same boundary create only one edge of E.

**Theorem, light version.** If every positive-mass K has w(K)<=W/2,
and the edge set E has a vertex cover of size at most two, then G has
an exact half separator consisting of two ambient geodesics.

**Theorem, all-mass version.** Suppose, in addition, each attachment
torso G[K union T(K)] has treewidth at most three. If the two-vertex
cover condition holds for the boundaries of all attachments, then the
conclusion holds for every nonnegative real vertex-mass assignment.

There is no bound on attachment order or number. In particular this
handles any two distinct two-boundary sectors, whether disjoint or not,
arbitrarily many attachments in those sectors, and arbitrary numbers
of one-boundary attachments. More generally the occupied sectors may
be any subgraph of the active cycle with vertex-cover number at most
two. The light version imposes no treewidth condition on attachments.
Isometry and the facial embedding are hypotheses, not conclusions for
arbitrary weighted planar clique sums.

### Core distance lemma

For every active a, all of H is contained in J_G(a,C). For every active
b nonadjacent to a in the active cycle, some original c adjacent to b
satisfies

    P=(a,r,b,c),   length(P)=d_G(a,c)=3 lambda.

To check this, first take lambda=1 with every rim edge of length one.
By symmetry let a=a_0. Its C-neighbors are c_0,c_1, and the original
C-vertices at distance at most two are exactly
{c_(k-1),c_0,c_1,c_2}. For b=a_j nonadjacent to a_0, one of c_j,c_(j+1)
is outside this set when k>=5. The route through r and b gives distance
three to that vertex. Every nonadjacent b therefore lies on an a-to-C
geodesic, as does r. The adjacent vertices a_1 and a_(k-1) lie on the
two-edge geodesics to c_2 and c_(k-1), respectively. Finally every
C-vertex belongs to J because it is an allowed terminal.

Increasing rim lengths or subdividing a rim edge to a path of total
length at least one cannot decrease distances between original core
vertices. All the displayed witnessing paths avoid rim edges, so they
stay geodesic. The new rim vertices are still facial terminals.
Scaling by lambda and the assumed isometry transfer these statements
to G, including attachments that create additional tied geodesics.

### Proof of the light version

The cover of E can be chosen to consist of two nonadjacent active
vertices a,b. A cover of size zero or one can be extended this way.
If a size-two cover consists of adjacent a_i,a_(i+1), then E is
contained in the three cycle edges incident with that pair. Replace
the cover by {a_(i-1),a_(i+1)}; it covers those same three edges and is
nonadjacent for k>=5.

Use the distance lemma to prescribe P=(a,r,b,c), rooted at a, and set
S=V(H). Every positive outside component has at most one neighbor in
S-P: r is removed, and the cover meets every two-element active
boundary. Also S is contained in J_G(a,C). The subset-transfer lemma
gives a second a-to-C geodesic Q and the desired half balance.

### Heavy attachments and the all-mass version

If some K has mass greater than W/2, take a width-three tree
decomposition of its torso. Its boundary T(K), being a clique of size
at most three, is contained in a bag. Join that bag to a single outside
bag V(G)-K. This is a tree decomposition of G, with every local bag of
size at most four and the outside bag a leaf.

Assign each vertex's mass to one containing bag, assigning outside
vertices to the outside bag. The component beyond that leaf contains
all the mass of K, which exceeds W/2. Thus a weighted centroid bag is
local. Its at most four vertices form a half separator. Pairing them
and joining each pair by an ambient geodesic gives two paths covering
the bag, and deleting extra vertices preserves the half bound.

If no K is heavy, the light version applies. This is the same local
centroid mechanism as the
[reviewed heavy-peripheral reduction](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md),
stated directly for width-three torsos. For the original unit
cyclic-neighborhood setting, a peripheral torso with universal r has
treewidth at most three: deleting r gives an outerplanar graph.

## Reproduction and scope

Run with Python 3.11 or later from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_rerooted_attachments/verify.py --check

The [checker](verify.py) imports graph construction, elementary graph
utilities, and sample-mass generation from the previous transfer artifact;
it is a regression check, not an independent review. Its exact results are in
[expected.json](expected.json). It checks spherical embeddings, original
metric distances and paths, core isometry, subset support, mass transfer
with paths entering attachments, and the local decompositions used for
heavy cases. The all-order and real-mass quantifiers rely on the written
proof, not on finite tests or a solver.

A 51-vertex fixture has two disjoint two-boundary pockets, core edge
length two, and new pocket edges of length one. Its chosen core has
19 vertices, while J(a,C) has 22. For the displayed prescribed P, the
old exact-union transfer has two positive outside components with two
surviving J-neighbors each. The whole pockets instead have one surviving
core neighbor each, so the subset lemma applies. This is strictness of
the sufficient condition for that P, not a claim that no other earlier
theorem or root can handle the graph.

For unit edges, the theorem is an all-order positive class for Problem
31, extending the previous common-active-boundary corollary to a
two-vertex cover on these annular cores. It does not cover an arbitrary
collection of occupied sectors, arbitrary cyclic neighborhoods, or
arbitrary edge lengths that shorten the core. No historical priority
claim is made.
