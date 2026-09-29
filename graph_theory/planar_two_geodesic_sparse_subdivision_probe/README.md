# Sparse mass in a large unit subdivision: a certificate transfer test

This note gives an exact test for transferring a finite two-geodesic
separator certificate through edge subdivision. It applies the test to
the team's [32-vertex weighted planar example](../planar_two_geodesic_full_menu_gap/README.md).
The original fifteen prescribed geodesic pairs and the heavy-four-vertex
repair cease to certify half balance after **unit subdivision**: for an
explicit mass of total 29, each pair leaves a component of mass at least
21, while the four heaviest vertices carry only 8. A different pair of
ambient geodesics does half-balance this same mass, with largest residual
component of mass 14. Thus this is a failure of a fixed proof certificate,
**not** a counterexample to [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Sparse-support compression lemma

Let every edge of a finite graph have a positive integer length. Replace
each length-\(L\) edge by a path of \(L\) unit edges. Give nonnegative
mass to a set of vertices in the resulting unit graph. Retain all original
vertices and every positive-mass subdivision vertex, and suppress all
other subdivision vertices, assigning each resulting edge its path
length. Call the smaller weighted graph \(K\).

Distances between vertices of \(K\) agree in the two graphs. Thus a path
in \(K\) is geodesic exactly when its unit-edge lift is geodesic between
the same endpoints. After deleting any union of such lifted paths, the
positive-mass components have the same masses as the components of \(K\)
after deleting the corresponding paths. Indeed, every suppressed vertex
lies internally on one edge chain, has zero mass and offers no branch.
An untouched chain connects its retained endpoints in both graphs. A
traversed chain has both endpoints deleted; its surviving interior, if
any, has zero mass. This proves the claim for any number of paths.

This is an **exact** reduction for candidate paths whose endpoints are
retained in \(K\). It gives a sufficient certificate for the full unit
graph when a balanced pair is found. It does not exclude useful paths
whose endpoints are zero-mass subdivision vertices, so failure of a menu
in \(K\) is not failure of the full two-path property.

## Explicit instance

The compact [certificate](certificate.json) specifies the thirty core
edge lengths, twenty parent corners, fifteen original path pairs, and an
integer mass assignment. Its SHA-256 is
`5e1d780366f885723c6cd9323e3a8a88deb515025d66d356f15bc57ed5dff634`.
Stellate the twenty icosahedral faces as in the
parent example. Give parent edges length 189 and other new face edges
length 28094, then unit-subdivide all ninety edges. The result is a
simple planar graph with **1,151,795 vertices**. Its sparse-mass
compression has just 48 vertices: the 32 original vertices and sixteen
positive-mass edge interiors, each put at distance
\(\lfloor L/2\rfloor\) from the first endpoint in the certificate's
oriented edge list. The seventeenth positive-mass point is original
vertex 28.

The certificate labels an interior point of original edge \(j\) by
\(32+j\); the checker maps these labels to 32,...,47 in increasing edge
order. The two rescuing geodesics, written with the certificate labels,
are

```
(109,27,107,6,110,28,111)
(28,110,6,54,11,60)
```

The first crosses a midpoint of a long face edge. Their ambient
shortestness is verified by exact Dijkstra distances in the compressed
weighted graph, hence also in the 1,151,795-vertex unit graph. All
fifteen original pairs are checked the same way. Exact component masses
establish the menu failure and rescue; no floating optimization is a
premise. The integer mass assignment was discovered by a mixed integer
linear program, but only the small displayed certificate is needed.

## Reproduction and scope

From the repository root, Python 3.11+ and the standard library suffice:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_sparse_subdivision_probe/verify.py
```

Expected output:

```text
planar_unit_subdivision_vertices=1151795 compressed_vertices=48
mass_total=29 top_four=8
menu_largest_components=21,26,23,25,25,26,26,26,21,28,28,28,21,21,21
rescue_component_masses=14,2
PASS
```

The checker verifies the icosahedron's twenty triangular faces, each
edge's two face incidences, every vertex link, Euler's equation, all
specified path lengths against exact shortest distances, and every
residual component mass in the compressed graph. The geometric argument
above transfers these checks to the full unit subdivision. The checker
does not enumerate every ambient geodesic or every path pair in that
graph and makes no all-mass claim for the subdivision.
