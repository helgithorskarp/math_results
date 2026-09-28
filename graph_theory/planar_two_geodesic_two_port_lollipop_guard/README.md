# Two-port transfer and weighted lollipop guards

An all-spanning geodesic-cover theorem for a fragment with an attached ear transfers exactly to arbitrary exterior networks meeting that fragment at two ports. Applying this rule to the [reviewed one-ear lollipop classification](../planar_two_geodesic_lollipop_spanning_cover_review1/REVIEW.md) produces a sharp fragment threshold, a weighted guard theorem, and a planar family of unbounded order and treewidth at least four. This is a sufficient result for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not a settlement of that unrestricted question. All edges here have unit length, and vertex masses are arbitrary nonnegative reals.

## Abstract two-port transfer

Let `F` be a finite simple graph on vertex set `C`, with distinct ports `a,b`. For integer `s>=2`, let `F_s` add a fresh `s`-edge path between `a,b`; write `F_infinity=F`. Say that `F_s` has the **all-spanning `k`-cover property** if, for every spanning edge subgraph `J` of `F_s`, each component of `J[C]` is covered by at most `k` `J`-geodesics. Path endpoints may lie anywhere in `F_s`.

For a finite simple host `G` with `G[C]=F` and all edges from `C` to `G-C` meeting `C` at `a` or `b`, let `Lambda(G,C)` be the set of lengths of its simple `a`-to-`b` paths with **at least one** internal vertex, all outside `C`.

**Exact transfer theorem.** The following are equivalent:

1. Every spanning edge subgraph `H` of `G` has the `k`-cover property for each component of `H[C]`, using ambient `H`-geodesics.
2. `F_s` has the all-spanning `k`-cover property for every `s` in `Lambda(G,C) union {infinity}`.

**Proof.** For `2 => 1`, fix `H`. If it has an exterior `a`-to-`b` path, choose a shortest such path `P` of length `s`; otherwise put `J=H[C]`. In the first case put `J=H[C] union P`, a spanning edge subgraph of `F_s`. **`J` is isometric in `H`.** Indeed, any path in `H` between vertices of `J` can be split into segments within `J` and maximal segments whose interiors avoid `J`. Each latter segment has both ends on `P` (the only fragment vertices with outside neighbors are its endpoints). If a segment joining `p_i,p_j` along `P` were shorter than `|i-j|`, splice it into `P` to get an exterior `a`-to-`b` walk shorter than `s`, and then erase loops. This contradicts the choice of `P`. Replace every off-`J` segment by its `P` subpath. If there is no exterior `a`-to-`b` route, a simple path between vertices of `C` cannot leave `C`, so `J=H[C]` is isometric too. Covering geodesics of `J` remain geodesics in `H`, regardless of their endpoints.

For `1 => 2`, take any `s` in `Lambda(G,C)` and choose an exterior path `P` of length `s` in `G`. Any spanning edge subgraph of `F_s` embeds as a spanning edge subgraph of `G` on `C union V(P)` by deleting all other edges; its other vertices are isolated. Thus a failed fragment cover in `F_s` would fail in `G`. The case `s=infinity` follows by deleting every exterior edge. `□`

In particular, if every exterior route has length at least `L>=2` and `F_s` has the property for all `s>=L`, then `G` has it. This remains true for disconnected spanning subgraphs and requires no restriction on the endpoints of the model's covering paths.

## Two-port completion lemma

Let `C` be an **induced** lollipop in a finite simple graph `G`: an `m`-cycle `0-1-...-(m-1)-0`, `m>=5`, and one pendant leaf `t` at `0`. Suppose every edge between `C` and `G-C` is incident in `C` with either `1` or `3`. Let `lambda` be the shortest length of a `1`-to-`3` path with internal vertices outside `C`, or infinity if none exists.

**Sharp lemma.** Every spanning edge subgraph `H` of `G` covers every component of `H[C]` by at most two ambient `H`-geodesics **if and only if** `lambda>=max(2,m-8)`. In the positive case, the geodesics can be chosen with endpoints in `C`, and hence cover any connected subset of a component.

**Proof.** The [one-ear classification](../planar_two_geodesic_lollipop_spanning_cover/README.md) says `F_(m,s)` has the all-spanning two-cover property exactly when `s>=m-8`, for `s>=2`. The bare lollipop `F_infinity` has the property by its tree/whole-cycle case. If `lambda>=max(2,m-8)`, exact transfer applies. Conversely, if `lambda<m-8`, choose a shortest exterior route `P` of length `lambda` and keep only the edges of `C-12` and `P`. This reproduces the classification's failing `F_(m,lambda)-12` witness, with all other host vertices isolated. The original constructive positive covers have endpoints in `C`; the isometric transfer preserves them. `□`

## Four-vertex weighted guard corollary

**Theorem.** Let a finite simple planar graph `G` have a set `S` of at most four vertices. Suppose every component of `G-S` either has at most five vertices or is a two-port lollipop satisfying the lemma in the ambient graph `G`. Then **every** spanning edge subgraph `H` of `G`, with **every** nonnegative vertex-mass assignment, has a half-balanced separator equal to the union of at most two `H`-geodesics.

**Proof.** Let total mass be `W`. If no component of `H` exceeds `W/2`, use the empty union. Otherwise work in its unique heavy component `K`; pair the at most four vertices of `S intersect K` and connect the pairs by at most two `H`-geodesics. If this pair does not balance, its unique heavy residual component `D` lies inside one original component `C` of `G-S`. For a small `C`, pair the vertices of `D` when `|D|<=4`. When `|D|=5`, the connected `H[D]` is noncomplete because planar graphs exclude `K_5`; an induced three-vertex path is an ambient `H`-geodesic, and a second geodesic joins the other two vertices. For a lollipop `C`, apply the lemma to `D`. In each case the replacement paths cover all of `D`. Every component remaining after their deletion has mass at most `W-w(D)<W/2`, even if the first pair's vertices return. This is the same complete-coverage step as the [reviewed four-guard theorem](../planar_two_geodesic_four_guard_review1/REVIEW.md).

## A planar family beyond the earlier fragment types

Start with the octahedron: equator `0-1-2-3-0` and poles `4,5`, each joined to every equator vertex. Inside one face incident with `01`, insert `r>=1` mutually disjoint copies of `C_11`. In each copy join its local cycle vertex `1` to core vertex `0`, and its local vertex `3` to core vertex `1`. The copies can be placed in parallel inside that face; `verify.py` gives a spherical rotation. Call the graph `G_r`. It has `6+12r` vertices, `12+14r` edges, and `8+2r` faces.

For each lollipop copy, the only outside ports are its local vertices `1,3`. The path through core edge `01` has length three, and no shorter outside route exists because those ports have distinct outside neighbors. Thus `lambda=3=11-8`. The guard `S={0,1,2,3}` leaves the poles as singletons and the `r` lollipops as components. The theorem applies to every spanning edge subgraph of `G_r` and every vertex-mass assignment.

The induced octahedron has minimum degree four, so `tw(G_r)>=4`. For `r>=5`, any four-vertex set misses one whole lollipop copy. A remaining component then contains a 12-vertex cycle-with-leaf graph, so no four-vertex guard can leave only components of order at most six, isometric paths or cycles, or isometric trees with at most four leaves. This comparison is with the earlier **guard criteria**, not with every possible proof of balance. The gadgets have pendant vertices; the family is not asserted to be biconnected.

## Reproduction and trust boundary

From the repository root, run with Python 3.11+ and only the standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_two_port_lollipop_guard/verify.py
```

The checker reconstructs the graph and spherical rotation, checks Euler's identity, component structure, two-port boundary and outside distance, and all-pairs fragment isometry. It independently tests isometry of the **entire reduced graph** and geodesic pair coverage after sampled edge deletions, checks all 2,048 spanning subgraphs of a small two-port host with cross-links in its exterior network, and confirms a short-route failure inside a host with two exterior routes. The universal claims rest on the written exact transfer and heavy-component proofs; the finite checks do not replace them.

Expected output:

```text
family r=1 vertices=18 edges=26 faces=10 ports=3 isometric=yes
family r=5 vertices=66 edges=82 faces=18 ports=3 isometric=yes
family r=8 vertices=102 edges=124 faces=24 ports=3 isometric=yes
family r=2 vertices=30 edges=40 faces=12 ports=3 isometric=yes
sampled_subgraphs=100 exact_distance_reductions=200 full_isometries=200 routed=102 component_covers=768 PASS
two_route_host shortest_exterior=2 m=11 deletion=12 two_cover=no PASS
tiny_host_spanning=2048 routed=944 isometric=2048 PASS
PASS
```
