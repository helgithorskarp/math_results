# A finite separator certificate for all vertex masses

## Result and boundary

The explicitly edge-weighted planar triangulation G below has 50 vertices
and 144 edges, with integer edge lengths from 1 through 19. For **every**
assignment of nonnegative real vertex masses, one of the 14 prescribed
geodesic pairs in `certificate.json` is a half-balanced vertex separator.
Every path is shortest in G before deletion.

In fact, one of those pairs meets every member of any given pairwise
intersecting family of connected vertex sets of G. Here *intersecting*
means sharing a vertex, not merely having an edge between two sets.

The longest geodesic has 11 vertices, even when ties are included. Therefore
four geodesics cover at most 44 of G's 50 vertices. This example lies beyond
the elementary sufficient condition of covering the whole graph by four
geodesics: if four cover V, their division into two pairs ensures that one
pair removes at least half of any assigned mass.

This is an exact finite certificate and a construction-search exclusion.
It does not prove the assertion for every edge metric on this graph, for
other graph orders, or for all planar graphs. It is not a counterexample to
Barbados Problem 31. No literature priority claim is made.

## Exact graph and metric

Let V={0,...,49}. Vertex 0 is an apex outside a 7-by-7 square grid. Grid
vertex (i,j), with 0<=i,j<=6, has label 1+7i+j. Add the grid edges between
orthogonally adjacent pairs and the diagonal (i,j)(i+1,j+1) in each square.
Join 0 to every boundary vertex of the grid.

There are 84 grid edges, 36 diagonals, and 24 apex edges. This is a simple
planar graph: use the indicated diagonal in each grid square and draw the
apex spokes through the grid's outer face. Every face on the sphere is a
triangle. The count 144=3*50-6 agrees with the explicit triangulation.

For every edge with ordered labels a<b, define

    length(a,b) = 1 + H(a,b) mod 19,

where H(a,b) is the unsigned big-endian integer represented by the first
four bytes of SHA256 of the ASCII string `1:a:b`, with decimal labels and
no spaces or final newline. SHA256 is only a deterministic specification
of 144 small integers; no cryptographic assumption is used.

The certificate contains only the ordered vertex lists of its path pairs.
It does not supply trusted distances, components, or solver assertions.
The checker reconstructs the graph, its lengths, and all those facts.

## General certificate principle

Let G be any finite graph with a shortest-path metric, and let S_0,...,S_t
be vertex sets, each covered by at most two specified ambient geodesics.
For each i let C_i be the family of vertex sets of components of G-S_i.
Suppose the following procedure terminates in a contradiction:

1. Start with an empty list F of forced sets.
2. At step i discard every member C of C_i disjoint from a member of F.
3. If exactly one member remains, append it to F and continue.
4. If no member remains, the certificate closes successfully.

If a step has more than one remaining member, this linear certificate does
not justify continuing; branching or a different order would be needed.

**Lemma.** If the certificate closes, every pairwise intersecting family B
of nonempty connected vertex sets is met by one of S_0,...,S_t. Consequently
every nonnegative vertex mass assignment has a half separator among them.

**Proof.** Suppose no S_i meets every member of B. For each i choose a
member B_i of B disjoint from S_i. Connectivity puts B_i inside one
component C_i^* of G-S_i. Because the B_i intersect pairwise, their
containing sets C_i^* also intersect pairwise.

Inductively every forced set produced by the procedure must be the selected
component at its step: previously forced sets are selected components, so
any component disjoint from one of them is impossible, and the sole
remaining option is necessary. A step with no remaining option contradicts
the existence of the selections C_i^*. This proves the first assertion.

For vertex masses of positive total W, take B to be all connected vertex
sets with mass greater than W/2. Any two members intersect, by nonnegativity
and additivity of the masses. A set S_i meeting all of them leaves no
component heavier than W/2. If B is empty, every S_i suffices. If W=0,
half balance is automatic. This proves the mass assertion.

Equivalently, one can assume every S_i fails half balance and successively
force its unique component of mass greater than W/2. Two such components
cannot be disjoint, and the same certificate gives the contradiction.

## Application to G

`certificate.json` gives 14 pairs using 22 distinct paths. The checker
establishes that each displayed path is an ambient geodesic and recomputes
the connected components of its vertex deletion. The linear certificate
then has 13 forcing steps followed by an empty set of options:

| Step | Orders of components after deletion | Forced component order |
|---:|:---|---:|
| 0 | 46 | 46 |
| 1 | 2, 37 | 37 |
| 2 | 47 | 47 |
| 3 | 41 | 41 |
| 4 | 3, 36 | 36 |
| 5 | 2, 5, 29 | 29 |
| 6 | 40 | 40 |
| 7 | 2, 35 | 35 |
| 8 | 9, 11, 13 | 13 |
| 9 | 48 | 48 |
| 10 | 2, 15, 19 | 15 |
| 11 | 13, 25 | 13 |
| 12 | 3, 6, 28 | 3 |
| 13 | 1, 42 | none |

The table alone does not certify intersections. The checker compares the
actual vertex sets, which it computes directly from the path lists.

All-pairs shortest distances are computed by exact Floyd-Warshall. For
each source s, orient an edge vw forward exactly when
d(s,v)+length(vw)=d(s,w). Positive lengths make this orientation acyclic,
and every shortest path starting at s follows it. Conversely every path
from s in this directed graph is shortest to its endpoint, by telescoping.
Longest-path dynamic programming in these directed acyclic graphs therefore
counts the largest number of vertices on **any** geodesic, including all
ties. The maximum is 11. One witness is

    5, 6, 13, 12, 19, 26, 18, 25, 32, 31, 39.

Thus four-path covering cannot explain the universal mass conclusion.

## Provenance and trust

The construction lane first tested nonuniform edge metrics using an exact
SMT search over masses w(v)>=0, sum w(v)=1. A balanced pair found for a
candidate mass vector gives the necessary obstruction clause
`OR_C (2*sum_{v in C} w(v)>1)`. The exploratory search used Z3 4.15.4 and
Dijkstra paths with a positive power-of-two perturbation of the edge
lengths to ensure uniqueness. A selected inconsistent separator core
admitted the simple intersection certificate above.

The perturbation was then removed. All displayed paths remain shortest
for the small integer lengths specified here, as the separate checker
verifies. The discovery solver, its UNSAT answer, its proof trace, and
completeness of its path search are **not** premises of this certificate.

The trusted computational boundary is the published standard-library
Python checker, exact integer arithmetic, the deterministic SHA256 edge
assignment, and ordinary Python execution. The checker uses Floyd-Warshall
and direct set traversal rather than importing the search's Dijkstra and
bit-mask component code. It rejects truncated certificates, repeated
non-closing cuts, a nonedge, a nonsimple path, an existing-edge walk that is
not shortest, and a wrong metric identifier. This is not a formal proof
assistant verification or an independent peer review.

The motivating problem is [Codsi's Barbados 2026 Problem
31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). The
standing team's [weighted reduction](../planar_two_geodesic_weighted_reduction/README.md)
justifies investigating weighted constructions for that problem; it is not
needed to validate this positive certificate. For the distinction between
ambient and sequential shortest-path separators, see Diot and Gavoille,
[*Path Separability of Graphs*, HAL v3, 2010](https://emilie-diot.eu/Article/DG10a).
