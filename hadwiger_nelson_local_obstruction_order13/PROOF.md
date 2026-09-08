# Proof of the local planar obstruction gate

## Two necessary conditions

Let `G` have an injective realization in the Euclidean plane in which every
edge has length one.  It need not be an induced or strict unit-distance graph.

First, `G` contains no `K2,3`.  The two vertices in the part of size two are
distinct circle centres, while the three vertices in the other part would be
three distinct intersections of their unit circles.  Two distinct circles
have at most two common points.

Second, the graph induced by every open neighbourhood `N(v)` is bipartite.
All neighbours of `v` lie on the unit circle centred at `v`.  If two of them
are adjacent, their central angle is `pi/3` or `-pi/3` modulo `2*pi`.  On a
cycle in `G[N(v)]`, divide every signed central-angle change by `pi/3`.  The
sum is zero modulo six, while every summand is `+1` or `-1`.  An odd number
of odd summands cannot be divisible by six.  Thus `G[N(v)]` has no odd cycle.
This condition includes the familiar impossibility of a planar unit `K4`.

## Reduction to edge-critical graphs

Suppose a graph `G` on at most 13 vertices is not four-colourable.  Repeatedly
delete edges while preserving non-four-colourability, then remove isolated
vertices.  The resulting graph `H` has chromatic number exactly five and
deleting any edge makes it four-colourable: after deleting any edge its
chromatic number is at most four, while adding one edge raises chromatic
number by at most one.  Thus `H` occurs in the complete edge-5-critical
catalog at its order.

Orders below five are impossible.  At order six, every graph of chromatic
number at least five contains `K5`.  Indeed, two disjoint nonedges give a
four-colouring by using them as two two-vertex colour classes.  Three
pairwise-intersecting nonedges that form a triangle give a four-colouring by
using their three common vertices as one colour class.  Otherwise all
nonedges have one common endpoint, and the other five vertices form `K5`.
Since `K5` contains `K2,3` as a subgraph, order six is locally excluded; the
published edge-critical table equivalently has count zero there.  The actual
catalog orders needed are therefore `5,7,8,9,10,11,12,13`.

The hash-pinned McKay/Lalonde catalogs contain 8,463,757 graphs over those
orders.  Exact enumeration gives:

| order | edge-5-critical | `K2,3`-free | also locally bipartite |
|---:|---:|---:|---:|
|5|1|0|0|
|7|1|0|0|
|8|2|0|0|
|9|21|0|0|
|10|162|0|0|
|11|4,008|0|0|
|12|147,753|0|0|
|13|8,311,809|1|0|

The sole `K2,3`-free graph is `LCQRDPqReqFchs`, with 13 vertices and 33
edges.  The neighbours `3,5,12,7,10` of vertex zero form a five-cycle in
that order.  It therefore violates the second condition.  No catalog member
passes both necessary conditions, proving that every planar unit-distance
graph on at most 13 vertices is four-colourable.

The C++ scanner and independent Python checker decode graph6 by different
representations and both replay every catalog record.  `controls.py` directly
checks that the exception is edge-5-critical, verifies its obstruction, and
tests `K4`, `K2,3`, odd-wheel, and realizable regular-hexagon-wheel fixtures.
Catalog completeness and the advertised edge-critical property remain
imported from the cited external primary data source; the code checks the
downloaded identities and classifies every supplied record.
