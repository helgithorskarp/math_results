# A rooted-decomposition obstruction inside positive planar annuli

This note records a limitation of a proof method for [Barbados 2026
Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
It gives **no counterexample to the separator question** and no new positive
separator class. All graphs below are finite, simple, undirected, and have
unit edge lengths. A geodesic is a shortest path in the original graph;
singleton paths are allowed. A bag is *covered* by two geodesics when it is
contained in their vertex union; the paths may use vertices outside the bag.

## The obstruction

For an integer k >= 4, let A_k have vertices

    r, b_0,...,b_(k-1), c_0,...,c_(k-1)

and edges, with indices modulo k,

    r b_i, b_i b_(i+1), c_i c_(i+1), b_i c_i, b_i c_(i+1).

Draw the b-cycle outside the c-cycle, triangulate each annular quadrilateral
using b_i c_(i+1), and place r on the other side of the b-cycle with a fan
to all b_i. This is a planar graph with 2k+1 vertices and 5k edges. The
vertices outside the closed neighborhood N[r] induce exactly C_k.

**Proposition.** No tree decomposition of A_k can have both properties:

1. r belongs to every bag;
2. every bag is covered by at most two ambient A_k-geodesics.

This holds with **no restriction on bag size or decomposition width**.
Nevertheless, for every nonnegative real vertex-mass assignment on A_k,
there is a half-balanced separator equal to the union of at most two
geodesics, both starting at r. Thus even this stronger positive separator
property does not supply a decomposition with properties 1 and 2.

### Two local obstructions

Let H be an induced six-vertex subgraph of a unit graph G, with diameter
two. A G-geodesic contains at most three vertices of H: four such vertices
would make its subpath between the first and last have length at least
three, contradicting their distance at most two. If it contains three,
they occur consecutively and induce a three-vertex path in H. It follows
that two G-geodesics cover H only if its vertices can be partitioned into
two induced three-vertex paths. Conversely, such a partition itself gives
two G-geodesics, since a nonedge of an induced subgraph remains a nonedge
in G. This criterion allows the covering paths to leave H.

Two diameter-two graphs fail the criterion:

* **The six-vertex wheel:** a five-cycle with a universal hub. In any
  partition into two three-vertex paths, the path containing the hub must
  use two nonadjacent cycle vertices. The other three cycle vertices
  induce an edge and an isolated vertex.
* **The three-sun:** a triangle a,b,c with independent vertices x,y,z,
  adjacent respectively to {a,b}, {b,c}, {c,a}. A three-vertex path using
  one triangle vertex and two independent vertices leaves a triangle.
  One using two triangle vertices and one independent vertex leaves an
  edge and an isolated vertex. The other possible distributions do not
  give a three-vertex path.

Consequently, neither vertex set can be covered by two ambient geodesics
in any unit graph in which it appears as an induced subgraph.

### Every possible leaf bag is obstructed

For each i, the six vertices

    N_A[b_i] = {b_i, r, b_(i-1), b_(i+1), c_i, c_(i+1)}

induce a wheel, with hub b_i and rim

    r, b_(i-1), c_i, c_(i+1), b_(i+1), r.

For each i, the six vertices

    {r} union N_A[c_i] = {r, c_i, c_(i-1), c_(i+1), b_(i-1), b_i}

induce a three-sun: the central triangle is c_i,b_(i-1),b_i; its three
independent vertices are c_(i-1),c_(i+1),r. The condition k >= 4 excludes
additional edges between the two displayed predecessor/successor vertices.

Suppose a finite tree decomposition with properties 1 and 2 exists.
Repeatedly remove a leaf bag contained in its neighboring bag; this
preserves all decomposition axioms and both properties. If only one bag
remains, it contains all vertices, hence contains an obstructed wheel.
Otherwise take a leaf bag X with neighbor Y, and a vertex v in X minus Y.
The connected-occurrence axiom implies that v appears in no other bag.
Every neighbor of v must therefore be in X. Since r lies in every bag,
v is not r and X contains {r} union N_A[v]. The displayed wheel or
three-sun then prevents a two-geodesic cover of X. This contradiction
proves the negative assertion.

Equivalently, completing all edges r c_i for decomposition purposes leaves
no possible first elimination bag covered by two geodesics of A_k. Those
completion edges are **never** added to the ambient metric.

### The half separators still exist for every vertex mass

This is the familiar cyclic column-median argument from the earlier
[capped-mesh result](../planar_geodesic_mesh_obstructions/PROOF.md), included
to delimit the obstruction. Let mu_i be the sum of the masses at b_i and
c_i, and put M = sum mu_i. Each path

    P_i = r, b_i, c_i

is an ambient geodesic, because r and c_i are distinct nonadjacent
vertices. Prescribe the first column as 0. If M = 0 or mu_0 >= M/2, delete
P_0. The remaining total mass is at most M/2. Otherwise choose the first
j >= 1 for which mu_0+...+mu_j >= M/2, and delete P_0 union P_j. The
columns strictly between 0 and j have total mass less than M/2; the other
open column interval has total mass at most M/2. Every edge remaining
after r is deleted joins the same or cyclically adjacent columns, so no
component crosses the two deleted columns. The mass at r is deleted and
M is at most the original total mass. Both cases prove exact half balance.
This argument includes zero masses and makes no integrality assumption.

## Consequence for the structural route

The reviewed [forest-nonneighbor theorem](../planar_two_geodesic_forest_non_neighbors/README.md)
uses a tree decomposition with r in every bag and two ambient geodesics
covering each bag. Its [independent review](../planar_two_geodesic_forest_non_neighbors_review1/REVIEW.md)
suggests treating cyclic nonclique components next. The proposition above
shows that this particular decomposition invariant cannot extend even
to all graphs in which the nonneighbors of r induce a single chordless
cycle. A successful extension must at least allow bags to omit r, use
mass-dependent separators directly, or change the invariant.

The obstruction does not exclude decompositions whose bags may omit r.
As a concrete control, `orders.json` gives such two-geodesic-covered
decompositions for A_k, 4 <= k <= 12; `verify.py` independently checks the
resulting bags, paths, edges, and connected vertex occurrences. These
finite witnesses are not an all-k claim. Nor does the obstruction rule
out choosing a different distinguished vertex. The two-geodesic half
question for arbitrary planar graphs remains open.

This is a method-obstruction finding, not a claimed new paper-worthy
positive separator theorem. No priority claim is made. The all-order
negative and positive statements above have elementary written proofs;
the checks below are reproducibility evidence rather than proof premises.

## Reproduction

From the repository root, using Python 3.11 or later and only its standard
library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_rooted_decomposition_barrier/verify.py --check
```

The checker builds the graphs and their spherical face systems for
4 <= k <= 40, checks both neighborhood types and their ambient distances,
and exhausts all geodesic pairs in each of the two six-vertex obstructions.
For 4 <= k <= 12 it additionally enumerates all ambient geodesics and
directly checks the failure of every root-augmented neighborhood cover.
It validates every unrestricted decomposition in `orders.json` and checks
the median separators on exact integer and rational masses, including all
binary mass assignments for k = 4,5. Two malformed path witnesses are
rejected. The compact deterministic output is in `expected.json`.

The witness labels in `orders.json` are r = 0, b_i = 1+i, and
c_i = 1+k+i. Each list is an elimination order; later neighbors are filled
to a clique solely to construct the bags. The output records 37 spherical
embeddings, 1,628 blocked neighborhoods, 144 direct ambient-pair checks,
nine unrestricted decompositions with 153 bags and 306 checked covering
paths, 5,039 mass checks, and two rejected malformed paths.

No external solver, graph census, private discovery-search code, or large
certificate is required. Discovery Net commitment and source publication
do not themselves constitute independent mathematical review.
