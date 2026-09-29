# Thirty-site all-mass guard in a planar unit subdivision

The earlier [sparse-mass probe](../planar_two_geodesic_sparse_subdivision_probe/README.md)
gave one 29-unit mass on seventeen marked vertices of a
1,151,795-vertex simple planar unit graph. Here a fixed pair of ambient
geodesics proves **half balance for every nonnegative real mass supported
on a specified set of thirty vertices** in that graph. The set contains
all seventeen earlier marked vertices. The assertion persists in an
unbounded family obtained by scaling every original edge length by an
integer before unit subdivision.

This is a support-restricted positive result for [Barbados 2026 Problem
31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). The
problem counts **every** vertex uniformly. The all-mass theorem here
does not allow positive mass on the other subdivision vertices and is
not a settlement of that question.

## Four-site residual guard

The following elementary lemma applies to any finite graph with
positive edge lengths. Let \(X\) be a designated set of vertices.
Suppose two ambient geodesics \(P,Q\) leave every component of
\(G-(V(P)\cup V(Q))\) containing at most four vertices of \(X\).
Then every nonnegative mass supported on \(X\) has a half-balanced
separator consisting of at most two ambient geodesics.

Indeed, if \(P\cup Q\) fails, there is a unique residual component
\(C\) with mass greater than half the total \(W\). Its positive-mass
support has at most four vertices. Pair these vertices in any way,
allowing singletons, and take shortest paths between paired vertices
in the **original graph**. These at most two paths delete all mass of
\(C\), which exceeds \(W/2\). Every new residual component has mass
at most \(W-w(C)<W/2\). The zero-total case is handled by \(P,Q\)
itself. The replacement paths need not be the original guard paths.

## Explicit planar graph and marked support

Use the [compact predecessor certificate](../planar_two_geodesic_sparse_subdivision_probe/certificate.json):
stellate each face of the icosahedron to form a 32-vertex, 90-edge
triangulation. Give its thirty old edges the listed integer lengths,
each selected parent edge length 189, and each other face edge length
28094. Unit-subdivide every edge. On the sixteen edges listed by the
predecessor's `mass_atoms`, mark the vertex at distance
\(\lfloor L/2\rfloor\) from the edge's first listed endpoint. Label
these sixteen marks 32,...,47 in increasing original-edge index;
the original vertices keep labels 0,...,31. The 48-vertex weighted
compression retains precisely these labels and preserves distances
between them. Its 106 edge chains account for the 1,151,795 unit
vertices.

The [new 236-byte certificate](certificate.json), with SHA-256
`19b49189d7ef8cbed8f62b618b1b831e35c0c90c9a47ee1ea89db4d00383f505`,
gives the two guard geodesics as paths in this compression:

```
P = (9,10,6,39,27),   length 1772
Q = (11,8,4,24),      length 1784.
```

Every edge on these paths lifts to its entire unit chain; the lifted
paths are geodesic in the full unit graph because retained-vertex
distances agree with the compression. Their residual components meet
the designated thirty-site set

```
X = {0,1,4,6,8,9,10,11,24,25,27,28,30,31,
     32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47}
```

in exactly the following sets, omitting components with empty
intersection:

```
{0,1,32,37}       {25,38}          {28,41,42,43}
{30,44,45}        {31,46,47}       {33} {34} {35} {36} {40}.
```

The largest intersection has four vertices, so the residual guard
lemma proves half balance for **every** real mass supported on \(X\),
including masses that defeat all fifteen inherited paths of the
predecessor. No linear-programming or mass sampling premise is used.

## Arbitrarily large unit graphs

For any integer \(k\ge1\), multiply all ninety edge lengths above by
\(k\) and then unit-subdivide. On each marked edge put its marked site
at distance \(k\lfloor L/2\rfloor\) from the first endpoint. The
48-vertex compressed topology is unchanged and every compressed edge
length is multiplied by \(k\). Hence both guard paths remain ambient
geodesics, and their residual site sets are unchanged. Every
nonnegative real mass supported on the corresponding thirty sites is
half-balanced by at most two ambient geodesics. The full unit graph has

\[
 N_k=32+\sum_e(kL_e-1)=1{,}151{,}853k-58
\]

vertices. These are planar simple graphs of unbounded order. This
argument changes the placement of the marks when \(k\) changes; their
labels refer to corresponding positions in each graph.

## Exact check and trust boundary

From the repository root, Python 3.11+ and standard library only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_thirty_site_subdivision_guard/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_thirty_site_subdivision_guard/audit.py
```

Expected output:

```text
core_vertices=32 core_edges=90 compressed_vertices=48 compressed_edges=106
unit_vertices_k1=1151795 unit_vertices_k2=2303648
marked_sites=30 old_sites_contained=17 path_lengths=1772,1784
residual_site_counts=4,4,3,3,2,1,1,1,1,1
PASS
```

The separate audit prints:

```text
faces=20 unit_vertices=1151795 compressed_edges=106 paths=1772,1784 residual_site_max=4 old_sites=17 PASS
```

The checker independently rebuilds the twenty core faces, checks their
edge incidences, vertex links and Euler equation, reconstructs the
weighted compression from the predecessor JSON, verifies its SHA-256,
checks the two paths against integer Dijkstra distances, and computes
the residual site sets. The separate audit enumerates faces as
three-cliques and uses Floyd--Warshall distances; it imports no target
Python code. Stellating the verified sphere triangulation
and unit-subdividing its edges preserve simplicity and planarity. The
universal claims over real masses and integer \(k\) follow from the
written guard and scaling proofs, not from enumeration of weights or
million-vertex graphs. Neither this result nor the [complete endpoint
kernel](../planar_two_geodesic_subdivision_endpoint_kernel/README.md)
asserts a uniform-vertex half separator for these graphs.
