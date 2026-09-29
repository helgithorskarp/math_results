# A ninety-dimensional price box on a five-connected planar core

An explicit 32-vertex planar graph has a half-balanced separator consisting
of at most two ambient shortest paths for **every nonnegative real vertex
mass** throughout a closed, independently variable **90-edge price box**.
The core is obtained by adding a center inside each pentagonal face of a
dodecahedron and joining it to that face's five vertices. It has 90 edges,
60 triangular faces and vertex connectivity exactly five.

This closes a construction region on a different core from the previous
icosahedron and its triangular face insertions. It is a conditional positive
result bearing on [Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf),
not a counterexample or a resolution. The underlying graph is the familiar
pentakis-dodecahedral graph; no novelty is claimed for that graph.

## Exact statement

The [1,790-byte certificate](certificate.json) gives twelve cyclically ordered
pentagons on vertices 0,...,19. For pentagon number i, insert vertex 20+i
and join it to the five boundary vertices, retaining all boundary edges.
It also lists an integer center c(e) for each of the resulting 90 edges.
The centers belong to `{7,8,9,10,11,13,14}`.

Choose any common scale lambda>0. Independently for **every** edge choose

```
lambda*(c(e)-1) <= length(e) <= lambda*(c(e)+1).          (1)
```

There are no equations coupling these choices. This is a full-dimensional
box in all ninety edge coordinates; its unscaled side lengths are two.
Every edge is positive, with unscaled lower bound at least six. The
half-width is at least one fourteenth of its own center in every coordinate.

For every nonnegative real mass w on all 32 vertices, of total W, there
exist at most two shortest paths **in this original weighted graph** whose
union leaves every connected component with mass at most W/2.

The certificate has two cases. If at most four vertices carry mass at least
W/2, pair those vertices and take ambient shortest paths covering them.
Otherwise, one of the following three **alternative pairs** works:

| Pair | First path | Second path |
|---|---|---|
| 1 | 24,6,23,8,9,29 | 4,25,19,0,21 |
| 2 | 9,29,11,30,17 | 26,15,14,28 |
| 3 | 7,8,9,10,22,18 | 19,25,4,5,27 |

The three prescribed pairs alone do **not** handle every mass: none contains
vertex 1, so a mass concentrated there defeats all three. The elementary
four-vertex case is essential to the stated proof. At most two paths are
used in either case; the six prescribed paths are not all deleted together.

## Why all ninety prices may vary independently

It suffices to take lambda=1. For a prescribed path P, define its adverse
corner by giving edges of P length c(e)+1 and all other edges length c(e)-1.
The certificate includes one integer potential pi on the 32 vertices for
each of the six such corners. It satisfies

```
|pi(u)-pi(v)| <= adverse_length(uv)   for every edge uv,
pi(last(P))-pi(first(P)) = adverse_length(P).
```

These inequalities prove that P is shortest at its adverse corner. There
are 6*90=540 edge inequalities. The six certified lengths there are
`40,37,32,25,41,39`.

For any competing simple path Q with the same endpoints, cancel its edges
shared with P:

```
length(Q)-length(P)
  = sum_{e in Q\P} length(e) - sum_{e in P\Q} length(e).
```

Over (1), this difference is minimized at P's adverse corner. It is
nonnegative there and hence throughout the entire real box. Positive
lengths allow every shortest-path comparison to be reduced to simple
paths. Thus all six paths stay geodesic simultaneously throughout (1),
including boundary points with ties. Common scaling changes neither
shortestness nor vertex components.

The six corners are six different metrics used to certify six fixed
paths. No claim that they are one common corner is needed, and there is
no enumeration of the 2^90 corners.

## Half-balance for every mass

For the three pairs, the component orders after deletion are respectively

```
(4,17),       (4,19),       (9,12).
```

Write A for the 17-vertex component after pair 1 and B for the 19-vertex
component after pair 2. The two components C,D after pair 3 are

```
A = {5,7,10,11,12,13,14,15,16,17,18,22,26,27,28,30,31}
B = {0,1,2,3,4,5,6,7,8,10,18,19,20,21,22,23,24,25,27}
C = {0,1,2,3,6,20,21,23,24}
D = {11,12,13,14,15,16,17,26,28,29,30,31}.
```

Direct component checks give `C intersect A = empty` and
`D intersect B = empty`.

If at most four vertices have total mass at least W/2, two geodesics can
cover them: pair up their vertices, allowing singleton paths. Their union
removes at least W/2, so every remaining component has mass at most W/2.
For W=0, any singleton path suffices.

In the remaining case, every component of at most four vertices has mass
strictly below W/2. If pair 1 fails, A must have mass greater than W/2;
if pair 2 fails, B must have mass greater than W/2. Then C and D each
have mass strictly below W/2, by the displayed disjointness and
nonnegativity. Pair 3 succeeds. This proves the statement for arbitrary
real masses, with no finite sampling or solver premise.

This is an elementary three-pair obstruction to a mass counterexample,
related to the team's [general three-pair transfer principle](../planar_two_geodesic_face_patch_transfer/README.md).
The proof above is self-contained and includes its own four-vertex case.

## Topology and relation to existing classes

The cyclic pentagons give a direct sphere embedding. Coning each face
produces 60 oriented triangles. The checker verifies that every edge has
two opposite directed face incidences, every vertex link is one cycle,
the graph is connected, and V-E+F=2. These certify a simple planar
triangulation. Vertices 0,...,19 have degree six; vertices 20,...,31 have
degree five.

Deleting any four vertices leaves the graph connected: the main checker
exhausts all 35,960 such sets. Smaller deletions follow by restoring
vertices, using minimum degree five. The separate audit instead finds
five internally vertex-disjoint paths for every nonadjacent vertex pair,
using an integer flow computation on split vertices. There are 406 pairs.
Menger's theorem gives connectivity at least five, and the degree-five
vertices give the reverse bound.

In particular this graph cannot be an icosahedral core with nonempty
attachments whose boundaries have at most three vertices: such an
attachment would give a vertex cut of size at most three. The same
observation explains the construction pivot away from triangular caps.

For uniform vertex mass the graph is not face-separable. In every plane
embedding, a simple planar graph with E=3V-6 has triangular faces; deleting
any face leaves a connected 29-vertex graph, larger than half of 32.
Thus the sufficient face-separator condition in
[Diot and Gavoille, *Path Separability of Graphs*, Section 3](https://emilie-diot.eu/Article/DG10a)
does not explain this instance. This is not a separation from every
previous sufficient condition, nor a historical-priority claim.

## Reproduction and trust boundary

From the repository root, with Python 3.11+ and assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_pentagonal_core_price_box/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_pentagonal_core_price_box/audit.py
```

Both print JSON with `status: PASS`; [expected.json](expected.json) records
the complete outputs. Recorded interpreter: Python 3.11.2. Both checkers
use only the standard library. The certificate SHA-256 is
`f2bb6517f68e6554bd7648a4f1e41ef5af47c5e7b7428fe3efb97b0e95ecd4c1`.

The main checker verifies the 540 potential inequalities, component
relations, sphere embedding and four-vertex-deletion connectivity. The
separate auditor imports no target code: it uses full-graph Floyd distances
at the six adverse corners, set-based component searches and split-vertex
flows instead of potential verification and deletion enumeration. It also
checks the literal mass-at-vertex-1 failure of the prescribed menu alone.
This is separate verification by the same researcher, not independent
peer review or proof-assistant formalization.

Exact SAT/linear optimization discovered the paths and box; those solvers
are unnecessary to verify the result. No optimum, maximal box, minimal
graph or complete classification of its metrics is claimed. The continuum
and all-mass conclusions rest on the written arguments above plus the
finite integer checks, not numerical tolerances or random trials.

The theorem concerns masses on the 32 original vertices. It does not
assert the all-mass property for unit subdivisions: added edge-interior
mass and new path endpoints require further analysis, as the team's
[sparse-subdivision test](../planar_two_geodesic_sparse_subdivision_probe/README.md)
illustrates. Nor is this an all-metric theorem for the underlying graph,
an arbitrary-face-patch extension, or an unrestricted answer to Problem 31.

The official problem statement and original path-separability paper were
refreshed on 29 September 2026. The announced Codsi workshop disproof still
has not been matched here to an exact statement and witness. We make no
claim that the unrestricted problem remains open.
