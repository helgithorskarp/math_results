# Half balance with light attachments after a first geodesic

All graphs are finite, connected, simple, undirected, and planar. Edge
lengths are positive; vertex masses are nonnegative. Every geodesic is
shortest in the original graph. This note extends the team's
[interval and facial support theorem](../planar_two_geodesic_interval_sweep/README.md)
to positive mass outside the support. It does not settle the unrestricted
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Transfer theorem

Let S be either a geodesic interval I(s,t), or a facial interval union
J(r,F), in the notation of the linked theorem. Let P be, respectively,
a prescribed s-t geodesic or a prescribed r-to-F geodesic. In particular,
V(P) is a subset of S. For every positive-mass component K of G-S assume:

1. Its original mass w(K) is at most W/2, where W=w(G).
2. After deleting P, K has at most one neighbor in S-P.

**Theorem.** There is a second ambient geodesic Q of the same terminal
type, contained in S, such that P union Q half-balances G.

Zero-mass outside components may have arbitrary boundaries and remain
in the graph. The boundary condition is checked after deleting the first
path. K may have many neighbors on P, and its internal graph need not be a tree or
have bounded treewidth. Neither the total mass outside S nor the number
of outside components is bounded. The conclusion concerns their
individual masses and surviving boundaries.

More precisely, let D be the total mass of components K with no neighbor
in S-P, and put B=max_K w(K), taking B=0 if there are none. Then Q can be
chosen so every remaining component has mass at most

    max( (W - w(P) - D)/2, B ).

### Proof

Set every mass on P to zero. Keep the original masses on S-P. For each
positive-mass outside component with a unique surviving neighbor a,
move all of its mass to a. Give all outside vertices mass zero; discard the masses of
components with no surviving neighbor. The resulting nonnegative mass
function w' is supported on S and has total

    M = W - w(P) - D.

Apply the interval or facial support theorem in the **unchanged graph
and metric**, with the same prescribed P and masses w'. It gives a
geodesic Q in S for which every residual component has w'-mass at most
M/2. No edge is added, deleted, shortened, or contracted in this step.

Consider a component R of G-(P union Q) meeting S. Any positive-mass
outside K meeting R lies entirely in R, because neither path enters K.
Its unique surviving support neighbor a is in R; otherwise K cannot connect to S
after deleting P union Q. Thus its entire original mass was transferred
to a vertex of R. It follows that w(R)=w'(R), hence w(R)<=M/2.

A residual component not meeting S is exactly one of the original
outside components K: its boundary was deleted, and the paths removed
none of its vertices. Its mass is at most B. This proves the sharper
bound, and M<=W together with B<=W/2 proves half balance. The zero-total
case is included.

Moving mass to a cut vertex is standard; for example,
[Diot--Gavoille, Proposition 5](https://emilie-diot.eu/Article/DG10a)
use it in their block reduction. Here deleting the prescribed path
creates the required boundary condition, allowing the existing sweep
theorem to apply without changing the ambient metric. This is not
a new path-order theorem. In particular, it makes no assumption that
mass can be assigned to one of two *surviving* boundary vertices.

## A cyclic-neighborhood consequence

Here the graph has unit edge lengths. Fix r such that C=G-N[r] is one
nonempty chordless cycle. Write

    A = {a in N(r) : a has a neighbor in C}.

For a component K of G[N(r)-A], let Y(K)=N(K) intersect A. These are its
active boundary vertices. Planarity gives |Y(K)|<=2: if three existed,
contracting connected K and C would give a K_(3,3) minor with opposite
parts {r,K,C} and those three vertices. This is the
[reviewed peripheral reduction](../planar_two_geodesic_prescribed_attachment/README.md).

**Corollary.** Suppose some a in A belongs to every two-element set
Y(K). Then two ambient geodesics half-balance G for **every** nonnegative
vertex-mass assignment.

In particular, the conclusion holds if there is at most one peripheral
component, at most one two-boundary component, or all two-boundary
components use a common active boundary vertex. Components with zero or
one active boundary vertex are unrestricted in number and size.
For a specified mass assignment, it suffices that the common vertex
meet the two-element boundaries of positive-mass components.

### Proof of the corollary

If any peripheral K has mass at least W/2, use the previously proved
heavy-peripheral reduction, including the equality case established in
its [independent review](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md).
For completeness, the boundary is contained in {r} union Y(K), of size
at most three. At equality, deleting this boundary suffices, and two
ambient geodesics cover it. For strict inequality, completing the
boundary to a clique gives a planar torso with universal vertex r and
treewidth at most three. Join its decomposition to one outside bag at
the boundary clique. Since K has more than half the mass, a weighted
centroid bag is local and has at most four vertices. Two ambient
geodesics cover it. These paths may differ from the paths used below.

Otherwise every K is strictly light. Choose a C-neighbor c of a, and
prescribe P=(r,a,c). This is an ambient geodesic of length two.

The cycle C bounds a face on the side opposite r: all vertices outside
C are adjacent to r and hence lie on its side, and C has no chord.
Moreover J(r,C)={r} union A union C. Indeed every active neighbor lies
on a two-edge r-to-C geodesic; every C vertex is a permitted terminal.
A shortest r-to-C path cannot use an inactive neighbor of r: going
through it before the last neighbor of r on that path would be longer
than using the direct root edge.

Every outside component of this J is a peripheral K. Deleting P removes
r and a. The common-boundary hypothesis leaves each K with at most one
neighbor in J-P. The transfer theorem now gives a second r-to-C geodesic
Q and exact half balance.

Thus the first path can absorb an arbitrary single peripheral component
when that component is light; the local torso argument handles it when
heavy. This proves the unrestricted, all-mass assertion for this class.
It does **not** complete an arbitrarily prescribed path in the heavy
case. The earlier 43-vertex prescribed-path obstruction is consistent
with this corollary.

### Another small boundary reduction

The same cyclic-neighborhood problem has a positive answer whenever
|A|<=4, with no common-boundary assumption. If w(C)>=W/2, its facial
boundary is a half separator, so
[Diot--Gavoille, Theorem 1](https://emilie-diot.eu/Article/DG10a)
gives two ambient geodesics. A peripheral component of mass at least
W/2 is handled as above. In the remaining case delete {r} union A:
the components are C and the peripheral components, each light.

For |A|<=3, this boundary has at most four vertices and two geodesics
cover it. For |A|=4, two vertices a,b of A are nonadjacent, since
otherwise {r} union A induces a forbidden planar K5. The path (a,r,b)
is geodesic, and a shortest path joining the other two active vertices
covers the rest of the boundary.

Consequently, any counterexample within the single-cycle class must
have at least five active neighbors, strictly light C and peripheral
components, and no active vertex common to all two-boundary components.
These necessary conditions do not establish that a counterexample exists.

## Checks, strictness, and limits

The standalone [checker](verify.py) uses exact integer distances,
explicit spherical embeddings, original-graph residual components, and
the mass transfer itself. It tests unit annuli with one-boundary and
common-boundary cone attachments, heavy and equality cases, and
nonuniform positive edge metrics on an interval core with light
attachments. Its local bags are checked as tree decompositions before
they are used for a heavy-component witness. The code imports no earlier
research checker and uses only the Python standard library.

A 46-vertex unit fixture has three one-boundary peripheral components
of order 11. The checker compares the transfer against every interval
and every rooted facial union in the supplied embedding under uniform
mass. Neither full support nor the earlier error condition E<=w(P)
applies in those checks, while transfer gives exact half balance. This
is an embedding-specific facial comparison. The same fixture has a
13-vertex subgraph of minimum degree four, excluding treewidth at most
three; has no dominating edge; and fails the earlier forest-or-clique
nonneighbor hypothesis at every root. No claim about all planar
embeddings or historical priority follows.

Run from the repository root with Python 3.11 or later:

    PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_light_attachment_transfer/verify.py --check

The exact output is in [expected.json](expected.json): 5,267 transfer
checks, 160 heavy-component checks, 45 prescribed paths, 14 local
decompositions, six unit fixtures, and two nonuniform metric fixtures.
The theorem and
corollaries rely on their written proofs and the previously reviewed
interval and peripheral lemmas, not on sampled masses or a graph census.
These are regressions, not an independent review or formal proof.

Exploration of the remaining light, two-boundary case found no failed
completion among sampled masses, including examples with missing
boundary edges. Those experiments are not a proof and are not a premise
of this note. In particular, no conclusion is asserted for arbitrary
collections of two-boundary attachments, for arbitrary unicyclic C with
trees attached, or for arbitrary edge metrics under only the unit
cyclic-neighborhood hypotheses.
