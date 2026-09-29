# Exact boundary test for ambient geodesics in face-patch expansions

The reviewed [face-patch theorem](../planar_two_geodesic_face_patch_transfer/README.md)
uses core isometry to protect six prescribed geodesics. Its
[independent review](../planar_two_geodesic_face_patch_transfer_review1/REVIEW.md)
found that this is stronger than necessary: some genuine core shortcuts
leave all six paths geodesic. Here is an exact boundary-distance test
and sharp single-shortcut thresholds at the published icosahedral center
metric. Combined with the reviewed quotient and heavy-torso arguments,
it gives an unbounded planar positive family with nonisometric cores.
It does not settle
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Exact terminal test

Let `I` be a connected positive-edge core. Replace independent atoms
by patches `K_z` with no edges between patches. Every patch neighbor
outside its patch lies in the core; write `B_z=N(K_z)`. For distinct
`a,b in B_z`, let `tau_z(a,b)` be the length of a shortest `a`--`b`
path with all its internal vertices in `K_z`, or infinity if none.
Form a weighted core multigraph `H` by retaining every core edge and
adding a virtual edge of length `tau_z(a,b)` for each finite boundary
distance.

**Compression lemma.** For any core vertices `s,t`,

    d_G(s,t)=d_H(s,t).                                             (1)

Every full-graph walk splits into core edges and maximal excursions
whose interiors lie in one patch; replace each excursion by a virtual
edge no longer than it. Conversely, realize each virtual edge by its
defining patch path. Taking minima gives (1). Positivity permits
simple shortest paths but is not otherwise needed for the walk argument.

Let `P` be a core path from `s` to `t`, of length `L`. The following are
equivalent:

* `P` is shortest in the **whole expanded graph**;
* `d_H(s,t)=L`;
* there is a potential `pi:V(I)->R` with `pi(t)-pi(s)=L`, satisfying
  `|pi(u)-pi(v)|<=length(uv)` on each core edge and
  `|pi(a)-pi(b)|<=tau_z(a,b)` on every virtual edge.

For necessity of the last condition take `pi(v)=d_H(s,v)`; for
sufficiency sum the edge inequalities along any `s`--`t` walk.
This is an exact finite test on patch boundary distances, even when
`I` is not isometric in `G`. It applies to each member of a fixed path
menu separately, including the menus in the
[fractional patch criterion](../planar_two_geodesic_fractional_patch_transfer/README.md).
The boundary-distance calculation can be large, but
the potential certificate has only core-vertex values once those
distances are known. No novel priority is claimed for shortest-path
duality or virtual-edge compression.

## Sharp one-shortcut formula

Fix core geodesics `P_1,...,P_k`, with endpoints `s_i,t_i` and lengths
`L_i=d_I(s_i,t_i)`. Add a single virtual edge `ab` of positive length
`x`, with no other new finite boundary connection. A shortest core
terminal path uses the shortcut at most once, so every `P_i` remains
ambient geodesic **if and only if** `x>=T(a,b)`, where

    T(a,b) = max(0,
        max_i [L_i-d_I(s_i,a)-d_I(b,t_i)],
        max_i [L_i-d_I(s_i,b)-d_I(a,t_i)]).                  (2)

The formula is exact including ties. Triangle inequalities give
`0<=T(a,b)<=d_I(a,b)`. If `T(a,b)<d_I(a,b)`, every
`x in [T(a,b),d_I(a,b))` simultaneously preserves the displayed paths
and shortens the core distance between `a,b`.

## Icosahedral center metric: fourteen genuine shortcuts

Use the twelve-vertex core, thirty edge prices, twenty faces, and six
paths in the predecessor's
[1,112-byte certificate](../planar_two_geodesic_icosahedron_price_region/certificate.json).
Its SHA-256 is
`070ac17d45f77ad18edb0ac1b9fae642982fc36db7dbd82ed5a1c3c325f1d11d`.
Give core edge `e` length `151*c_e`. The six paths are shortest at this
center metric. For each of the thirty core edges, (2) gives a sharp
threshold. Exactly fourteen have `T<d_I(a,b)`:

| edge | `d_I(a,b)` | `T(a,b)` | saving |
|---|---:|---:|---:|
| 0-1 | 28237 | 15251 | 12986 |
| 0-3 | 17214 | 4228 | 12986 |
| 0-5 | 10570 | 302 | 10268 |
| 1-2 | 27180 | 6946 | 20234 |
| 1-10 | 26274 | 3171 | 23103 |
| 2-3 | 25519 | 5285 | 20234 |
| 2-6 | 18271 | 4530 | 13741 |
| 2-7 | 14647 | 3322 | 11325 |
| 3-4 | 16157 | 3171 | 12986 |
| 3-8 | 14798 | 2265 | 12533 |
| 4-5 | 11627 | 1359 | 10268 |
| 6-10 | 22952 | 604 | 22348 |
| 7-8 | 15402 | 13892 | 1510 |
| 10-11 | 19177 | 4379 | 14798 |

For the review's `0-1` shortcut of length `20000`, the exact threshold
is `15251`: it may be shortened by another `4749` length units before
one of the six paths ceases to be geodesic.

To realize one row planarly, insert a vertex in either triangular face
containing `a,b`. Join it to `a,b` by positive edges whose lengths sum
to `x`, and to the third face corner by an edge longer than the entire
core diameter. This is a face-stellated planar triangulation. Its torso
is `K_4`, hence width three. The expensive third edge cannot improve
any core-to-core distance; the new patch supplies exactly the shortcut
relevant to (2). At `x=T`, all six paths remain ambient geodesics; at
`x=T-1`, at least one fails. Since every listed threshold exceeds one,
both controls use positive integer edge lengths. For `x<d_I(a,b)`, the
core is genuinely nonisometric.

The [three-pair quotient certificate](../planar_two_geodesic_face_patch_transfer/README.md)
still applies because its topology did not change; its heavy-patch
repair still applies because the new torso has width three. Therefore
every nonnegative real vertex mass on each of these thirteen-vertex
metrics has a half-balanced union of at most two ambient geodesics.
Additional mutually independent face patches of arbitrary order may
be inserted in other faces with width-three torsos. Make every new
patch-to-core edge longer than the original core diameter `34579`;
their interior edges may have arbitrary positive lengths. Such patches
cannot shorten any core-to-core path. They preserve the same six paths
by (1), so this yields
unbounded-order planar examples with at least one strict core shortcut.
The family remains of bounded global treewidth; no unrestricted planar
claim follows. This formalizes and quantifies the strict metric
extension noticed in the independent review.

## Reproduction and trust boundary

From the repository root, using Python 3.11+ and only the standard
library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_shortcut_thresholds/verify.py
```

The checker validates the predecessor certificate hash, reconstructs
the spherical core from its faces, uses independent integer
Floyd--Warshall distances, recomputes (2) for all thirty edges, and
builds sixty 13-vertex face-stellated graphs, one at `T` and one at
`T-1` for each edge.
It checks all six paths against whole-graph distances in every graph,
and checks the fourteen strict core-distance reductions. This is a
finite audit of the input geometry and threshold table. Statements
for arbitrary patches and real masses follow from the written
compression, potential, quotient and centroid proofs. The only data
input is the publicly linked predecessor certificate; no solver or
private data is used.

Expected output:

```text
core: vertices=12 edges=30 faces=20 paths=6 diameter=34579
single_shortcut_edges=30 strict_shortcuts=14 threshold_controls=60
max_distance_saving=23103 min_threshold=302 PASS
```
