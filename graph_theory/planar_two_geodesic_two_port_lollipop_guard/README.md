# Two-port transfer and weighted lollipop guards

An all-spanning geodesic-cover theorem for a fragment with an attached ear transfers to arbitrary exterior networks meeting that fragment at two ports. Applying this rule to the [one-ear lollipop classification](../planar_two_geodesic_lollipop_spanning_cover/README.md) produces a weighted guard theorem and a planar family of unbounded order and treewidth at least four. It is a sufficient result for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not a settlement of that unrestricted question. All edges here have unit length, and vertex masses are arbitrary nonnegative reals.

## Abstract two-port transfer

Let `F` be a finite simple graph on vertex set `C`, with distinct ports `a,b`. For integer `s>=2`, let `F_s` add a fresh `s`-edge path between `a,b`. Say that `F_s` has the **anchored all-spanning `k`-cover property** if, for every spanning edge subgraph `J` of `F_s`, each component of `J[C]` is covered by at most `k` `J`-geodesics whose endpoints lie in `C`.

**Transfer lemma.** Suppose `F_s` has this property for every integer `s>=L`, where `L>=2`. Let `G[C]=F`, and suppose every edge from `C` to `G-C` meets `C` at `a` or `b`. If every `a`-to-`b` path with internal vertices outside `C` has length at least `L`, then, for every spanning edge subgraph `H` of `G`, each component of `H[C]` is covered by at most `k` ambient `H`-geodesics with endpoints in `C`.

**Proof.** If `H` has an outside `a`-to-`b` path, choose one of minimum length `s>=L` and set `J=H[C]` plus this path, viewed as a spanning edge subgraph of `F_s`. For every `u,v` in `C`, `d_H(u,v)=d_J(u,v)`: one inequality is immediate, and in the other direction a simple `H`-path between fragment vertices has at most one outside excursion, necessarily between distinct ports. Replace it by the chosen shortest outside path, obtaining a `J`-walk no longer than the original path. If no outside route exists, choose any `s>=L` and let `J` contain just `H[C]` and isolated ear vertices. Then a simple `H`-path between vertices of `C` cannot leave `C`, so the same distance identity holds. The anchored cover in `J` transfers path by path to `H` by this distance identity. This includes disconnected `H` and `J`. `□`

## Two-port completion lemma

Let `C` be an **induced** lollipop in a finite simple graph `G`: an `m`-cycle `0-1-...-(m-1)-0`, `m>=5`, and one pendant leaf `t` at `0`. Suppose every edge between `C` and `G-C` is incident in `C` with either `1` or `3`. Let `lambda` be the shortest length of a `1`-to-`3` path whose internal vertices lie outside `C`, or infinity if none exists. Assume `lambda>=max(2,m-8)`.

**Lemma.** For every spanning edge subgraph `H` of `G`, every connected vertex set `D` in `H[C]` is contained in the union of at most two ambient `H`-geodesics. The geodesics can be chosen with their endpoints in `C`.

**Proof.** The all-spanning classification applies to every ear length `s>=max(2,m-8)`. Its constructive case proof chooses the endpoints of each covering path in `C`: tree leaves, cycle vertices, or the pendant leaf. Thus it proves the anchored all-spanning two-cover property required by the transfer lemma. Apply that lemma with `a=1,b=3,L=max(2,m-8)` to the component of `H[C]` containing `D`. The exterior network can have arbitrary order and many alternate routes; only its shortest two-port length matters. `□`

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

The checker reconstructs the graph and spherical rotation, checks Euler's identity, component structure, two-port boundary and outside distance, and all-pairs fragment isometry. It independently tests the exact distance reduction and geodesic pair coverage after sampled edge deletions. The universal weighted result is the written lemma plus the heavy-component argument; the finite checks do not replace them.

Expected output:

```text
family r=1 vertices=18 edges=26 faces=10 ports=3 isometric=yes
family r=5 vertices=66 edges=82 faces=18 ports=3 isometric=yes
family r=8 vertices=102 edges=124 faces=24 ports=3 isometric=yes
family r=2 vertices=30 edges=40 faces=12 ports=3 isometric=yes
sampled_subgraphs=100 exact_distance_reductions=200 component_covers=768 PASS
PASS
```
