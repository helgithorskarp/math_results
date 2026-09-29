# Four geodesic pairs are the first mass-versus-intersection gap

For a **fixed menu** of vertex separators, two natural certificates differ.
The mass property says that one menu set half-balances every nonnegative
vertex weighting. The intersection-transversal property says that one menu
set meets every member of each pairwise-intersecting family of nonempty
connected vertex sets. The latter was used in the reviewed
[50-vertex planar metric certificate](../planar_weighted_heavy_component_certificate/PROOF.md)
and implies the mass property.

**Sharp theorem.** For any finite graph and any nonempty menu of at most
**three** vertex sets, the two properties are equivalent. At four sets the
converse fails, even when the graph is planar and each menu set is the
union of two shortest paths in the original unit-edge graph. The six-vertex
octahedron gives an explicit example.

This is a statement about the strength of two fixed-menu proof methods for
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
The octahedron itself has two-geodesic half separators for every mass
assignment; it is **not** a counterexample to Problem 31. The result does
not prove the unrestricted planar property.

## Why three menus cannot have a gap

Let `S_1,...,S_t`, `1<=t<=3`, be arbitrary vertex sets. If the
intersection-transversal property holds, apply it to the family of all
connected sets of mass strictly greater than half the total. Any two such
sets intersect, since disjoint sets cannot both carry more than half the
mass. A menu set meeting every heavy connected set leaves no heavy
component. The zero-mass case is immediate.

Conversely suppose the intersection-transversal property fails. There is a
pairwise-intersecting family `F` of nonempty connected sets such that for
each `i` some `B_i in F` misses `S_i`. Let `C_i` be the component of
`G-S_i` containing `B_i`. The `C_i` intersect pairwise. We construct one
mass vector for which each `C_i` is strictly heavier than half.

* For `t=1`, put unit mass on any vertex of `C_1`.
* For `t=2`, put unit mass on a vertex of `C_1 intersect C_2`.
* For `t=3`, if all three sets share a vertex, put unit mass there.
  Otherwise select one vertex from each of the three pairwise
  intersections `C_1 intersect C_2`, `C_1 intersect C_3`, and
  `C_2 intersect C_3`, and give each unit mass. These three vertices are
  distinct because a coincidence would lie in all three sets. Each
  `C_i` then contains at least two of the three unit masses.

In every case `2w(C_i)>w(V(G))`. Thus each menu set fails half balance
for the same nonnegative weighting. This proves the equivalence through
three sets. The argument does not require planarity, geodesics, or positive
mass on every vertex. Equivalently, it is the support-at-most-three case of
the [mass-menu duality](../planar_two_geodesic_mass_menu_duality/README.md),
but the direct proof gives the exact threshold without LP machinery. `□`

## A four-pair planar witness to the gap

Let the six vertices of `G` be the two-element subsets of `{0,1,2,3}`.
Join two vertices when their subsets intersect. This is the line graph
`L(K_4)`, or the octahedron: its three pairs of opposite vertices are the
disjoint pairs of two-element subsets. It has six vertices and twelve
edges. It is planar because it is the one-skeleton of the convex
octahedron with vertices `+/-e_1,+/-e_2,+/-e_3`; the three opposite pairs
map to the three coordinate axes. Its eight triangular faces choose one
vertex from each opposite pair.

For `i in {0,1,2,3}`, let `C_i` be the three graph vertices whose
two-element subsets contain `i`. Each `C_i` induces a triangle. Let
`S_i=V(G)-C_i`, also a triangle. Choose any two edges of the triangle
`G[S_i]` whose union is all three vertices. Each edge is a one-edge
ambient geodesic, so `S_i` is the union of two geodesics. Deleting it
leaves the single connected component `C_i`.

Each graph vertex, a pair `{i,j}`, belongs to exactly two of the four
`C_i`. Therefore, for every nonnegative mass assignment of total `W`,

    sum_(i=0)^3 w(C_i) = 2W.

At least one `C_i` has mass at most `W/2`, so its prescribed two-geodesic
separator `S_i` is half-balanced. This proves the mass property for the
**fixed four-pair menu**, including arbitrary real and zero masses.

Nevertheless `C_i intersect C_j` is the one graph vertex `{i,j}` for
each `i != j`. Thus the four `C_i` form a pairwise-intersecting family
of connected sets. For every `i`, `S_i` misses `C_i`. No menu set meets
every member of that family, so the intersection-transversal property
fails. This proves four is the least possible menu size for such a gap.
`□`

The four components give the integer dual certificate `a_i=1` in the
[finite-menu theorem](../planar_two_geodesic_mass_menu_duality/README.md):
each vertex occurs in two components, so its dual load is exactly
`2/4=1/2`. The equality is sharp for some masses, but half balance allows
equality. There is no claim that every possible four-pair menu on an
octahedron has this gap.

## Independent finite audit

Run from the repository root with Python 3.11 or later, standard library
only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_four_menu_gap/verify.py
```

The checker constructs the line graph directly, then independently
certifies its eight oriented spherical triangular faces and Euler count.
It enumerates **all 30 geodesic paths** by simple-path traversal and BFS
distances, and examines **all 465 unordered path pairs** with repetition
and their full-graph residual components. It checks the four displayed
pairs, the component-intersection pattern, and all `3^6=729` mass vectors
with entries in `{0,1,2}`. These finite checks audit the graph and paths;
the path count also follows directly from six singletons, twelve edges,
and four two-edge geodesics between each of the three opposite pairs.
Thus the audit does not omit alternative shortest paths.
The all-real-mass conclusion is the four-component counting identity,
and the at-most-three theorem is the written proof above. Expected output:

```text
octahedron: vertices=6 edges=12 faces=8
all_geodesics=30 all_pairs=465 prescribed_pairs=4
sampled_mass_vectors=729 fractional_gap=yes PASS
```

No planar counterexample, historical priority, or finite-order census
conclusion is claimed.
