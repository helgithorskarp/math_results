# A complete endpoint kernel for sparse masses in unit subdivisions

The [previous sparse-mass probe](../planar_two_geodesic_sparse_subdivision_probe/README.md)
checked candidate geodesics whose endpoints were original or positive-mass
vertices. A geodesic in the full unit subdivision can also end at a
zero-mass subdivision vertex and cut an edge there. The lemma below gives
an **exact** finite representation of those endpoints. It applies to any
number of geodesics, any finite graph, and arbitrary nonnegative masses;
planarity is not needed. It is a testing tool for the weighted and
subdivision routes around [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf),
not a separator theorem for every planar graph.

## Endpoint-kernel theorem

Let \(F\) be a finite graph with positive integer edge lengths, and let
\(U\) replace every length-\(L\) edge by a path of \(L\) unit edges.
Give the vertices of \(U\) arbitrary nonnegative masses. Retain every
original vertex and every positive-mass subdivision vertex. The paths
between consecutive retained vertices on each subdivided edge are
**chains**; their interiors have zero mass and degree two. Let \(r\) be
the number of retained vertices and \(m\) the number of chains.

Build a weighted graph \(K\) by keeping, on each chain, its first
interior vertex next to each end (when present), then suppressing all
remaining interior vertices. A chain of length two has just one interior
vertex, kept once. Each weighted edge receives the length of the unit
path it replaces. Then

\[
 |V(K)|\le r+2m, \qquad |E(K)|\le 3m.
\]

**Theorem.** The catalogs of shortest-path *separator signatures* of
\(U\) and \(K\) are equal. A signature records (i) which retained
vertices a path deletes and (ii) which chains have an interior vertex
deleted. Consequently, for any \(k\ge1\), \(U\) has a union of at most
\(k\) ambient geodesics whose deletion leaves every component with mass
at most \(W/2\) **if and only if** \(K\) has such a union, with the same
vertex masses. More generally, the multisets of **positive** component
masses available from unions of at most \(k\) geodesics are identical
in the two graphs. The numbers of zero-mass components may differ.

The kernel is weighted. Its size is independent of the subdivision
lengths, apart from the bit lengths needed to store the edge weights.
The theorem does not assert that enumerating all geodesics of the kernel
is polynomial time, nor does it compress unit subdivisions whose many
internal vertices all have positive mass.

For an exact finite test, enumerate the weighted geodesics of \(K\),
encode each by its signature, and inspect all unions of at most \(k\)
signatures. For each union, delete its recorded retained vertices and
chain edges from the retained-vertex multigraph, then compute component
masses. This checks every possible endpoint in the full unit graph,
including zero-mass interior endpoints, without constructing its long
chains explicitly.

### Proof

Suppressing a zero-mass path interior preserves distances between all
kept vertices. Hence a geodesic of \(K\) lifts to an ambient geodesic of
\(U\), and the lifted path has the same signature.

For the reverse direction, take a geodesic \(P\) of \(U\). If it contains
no retained vertex, it lies entirely inside one chain. Replace it by a
singleton at that chain's first interior vertex. Both paths delete no
retained vertex and cut precisely that chain; the singleton is geodesic.

Otherwise, consider an endpoint of \(P\) lying inside a chain. The path
must travel from that endpoint to one of the chain's retained ends.
Shorten this terminal segment so the endpoint becomes the first interior
vertex adjacent to that retained end. This vertex lies on \(P\), and
the resulting path is a subpath of a geodesic, hence remains geodesic.
Shorten the other endpoint in the same way if necessary. No retained
vertex is lost, and each affected chain still contains a deleted
interior vertex. Every other chain has exactly the same deletion status.
The shortened path has both endpoints in \(K\), so suppressing its
remaining zero-mass segments gives a geodesic of \(K\) with the same
signature.

For any union of paths, take the union of their signatures. In the
remaining graph, surviving retained vertices are connected exactly when
they can be joined through chains whose interiors are untouched. Each
other component contains only zero-mass vertices. Therefore the
signature determines all positive component masses, proving the claim
for every \(k\).

### Why both ends are kept

Take a triangle on \(u,v,r\), with \(uv\) of length six and \(ur,vr\)
of length one. The path from \(r\) through \(v\) to the first interior
vertex of \(uv\) next to \(v\) is geodesic. Its signature deletes
\(\{r,v\}\) and cuts \(uv\). A kernel retaining only the interior
neighbor next to \(u\) cannot realize this signature: that neighbor is
closer to \(r\) through \(u\). Reversing \(u,v\) gives the symmetric
failure. Thus two end-neighbors can be needed to preserve the **exact
signature catalog**.

## Large planar instance and exact audit

For the [explicit 1,151,795-vertex planar unit subdivision](../planar_two_geodesic_sparse_subdivision_probe/README.md),
there are 48 retained vertices and 106 chains. Every chain has length
at least three. The complete endpoint kernel therefore has only **260
vertices and 318 weighted edges**. Any all-endpoint shortest-path test
for the published 29-unit mass may be performed on this kernel, with no
loss from omitted zero-mass endpoints. The earlier two rescuing
geodesics remain valid; this size reduction makes no claim about other
masses on the large graph.

Run the [checker](verify.py) from the repository root with Python 3.11+
and standard library only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_subdivision_endpoint_kernel/verify.py
```

Expected output:

```text
triangle: unit=8 kernel=5 full_paths=40 kernel_paths=16 signatures=12
triangle_both_one_sided_orientations_miss_a_signature=True
supported_square: unit=38 kernel=23 full_paths=752 kernel_paths=280 signatures=143
supported_path: unit=16 kernel=10 full_paths=136 kernel_paths=55 signatures=28
large_example: unit=1151795 sparse=48 endpoint_kernel=260 kernel_edges=318
PASS
```

For each small example, the checker enumerates **every** shortest path
between every endpoint pair in both the full unit graph and weighted
kernel, independently computes all retained-pair distances, and compares
the exact signature sets. It also checks the two orientation failures
above. For the large example it checks only the kernel dimensions from
the published compact certificate; the universal theorem follows from
the written proof, not from enumeration of the large graph. The
[weighted planar reduction](../planar_two_geodesic_weighted_reduction/README.md)
uses parallel protected subdivisions to carry genuine obstructions into
the uniform problem; ordinary single-edge subdivision alone does not
have that implication. [Diot and Gavoille's path-separability paper](https://emilie-diot.eu/Article/DG10a)
distinguishes ambient shortest paths from paths recomputed after
deletion. All paths in this note are ambient geodesics. No historical
priority claim is made for the elementary compression lemma.
